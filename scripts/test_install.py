"""Exercise install.sh against synthetic repositories and local settings.

Only the test copy of install.sh replaces literal $HOME with
$INSTALL_TEST_ROOT. The real script and HOME environment variable are never
changed, and no real user settings or config contents are read. Run from the
repository with `python3 scripts/test_install.py`; INSTALL_SOURCE_ROOT can
select the source repository while developing this test outside scripts/.
"""

from pathlib import Path
import os
import stat
import subprocess
import tempfile
import unittest


SOURCE = Path(os.environ.get("INSTALL_SOURCE_ROOT", Path(__file__).resolve().parents[1]))
EXAMPLE = b'model = "fixture-default"\n'
LOCAL_CONFIG = b'model = "fixture-local"\n# Preserve local choices.\n'


def snapshot(root):
    """Record entries without following links, including dangling symlinks."""
    result = {}
    for current, directories, files in os.walk(root, followlinks=False):
        for name in directories + files:
            path = Path(current) / name
            info = path.lstat()
            mode = stat.S_IMODE(info.st_mode)
            if path.is_symlink():
                value = ("link", mode, os.readlink(path))
            elif path.is_dir():
                value = ("directory", mode)
            else:
                value = ("file", mode, path.read_bytes())
            result[str(path.relative_to(root))] = value
    return result


class InstallerTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="codex-install-test-")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name).resolve()
        self.repo = self.root / "repo"
        self.local = self.root / "local"
        (self.repo / "agents").mkdir(parents=True)
        (self.repo / "skills" / "demo").mkdir(parents=True)
        self.local.mkdir()
        script = (SOURCE / "install.sh").read_text()
        (self.repo / "install.sh").write_text(
            script.replace("$HOME", "$INSTALL_TEST_ROOT")
        )
        (self.repo / "AGENTS.md").write_text("# Fixture instructions\n")
        (self.repo / "agents" / "demo.toml").write_text('name = "fixture"\n')
        (self.repo / "skills" / "demo" / "SKILL.md").write_text("# Fixture skill\n")
        (self.repo / "config.example.toml").write_bytes(EXAMPLE)
        self.config = self.local / ".codex" / "config.toml"
        self.agents = self.local / ".codex" / "AGENTS.md"

    def install(self, *args):
        env = dict(os.environ, INSTALL_TEST_ROOT=str(self.local))
        return subprocess.run(
            ["sh", str(self.repo / "install.sh"), *args],
            env=env, text=True, capture_output=True, timeout=15,
        )

    def prepare_config_parent(self):
        self.config.parent.mkdir(parents=True, exist_ok=True)

    def assert_success(self, result):
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def assert_rejected_without_writes(self, *args):
        before = snapshot(self.root)
        result = self.install(*args)
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(snapshot(self.root), before, result.stdout + result.stderr)

    def assert_managed_links(self):
        for source, destination in (
            (self.repo / "AGENTS.md", self.agents),
            (self.repo / "agents" / "demo.toml", self.local / ".codex" / "agents" / "demo.toml"),
            (self.repo / "skills" / "demo", self.local / ".agents" / "skills" / "demo"),
        ):
            self.assertTrue(destination.is_symlink(), str(destination))
            self.assertEqual(os.readlink(destination), str(source))

    def assert_regular_config(self, content, mode=0o600):
        self.assertFalse(self.config.is_symlink())
        self.assertTrue(stat.S_ISREG(self.config.lstat().st_mode))
        self.assertEqual(self.config.read_bytes(), content)
        self.assertEqual(stat.S_IMODE(self.config.stat().st_mode), mode)

    def test_fresh_install_creates_private_regular_config(self):
        self.assert_success(self.install())
        self.assert_regular_config(EXAMPLE)
        self.assert_managed_links()

    def test_fresh_install_is_idempotent(self):
        self.assert_success(self.install())
        before = snapshot(self.root)
        inode = self.config.stat().st_ino
        self.assert_success(self.install())
        self.assertEqual(snapshot(self.root), before)
        self.assertEqual(self.config.stat().st_ino, inode)

    def test_regular_config_is_preserved_with_and_without_force(self):
        self.prepare_config_parent()
        self.config.write_bytes(LOCAL_CONFIG)
        self.config.chmod(0o640)
        inode = self.config.stat().st_ino
        for args in ((), ("--force",)):
            with self.subTest(args=args):
                self.assert_success(self.install(*args))
                self.assert_regular_config(LOCAL_CONFIG, 0o640)
                self.assertEqual(self.config.stat().st_ino, inode)
                self.assertFalse(list(self.config.parent.glob("config.toml.bak.*")))

    def test_owned_live_link_migrates_and_backs_up_original_link(self):
        self.prepare_config_parent()
        target = self.repo / "config.toml"
        target.write_bytes(LOCAL_CONFIG)
        target.chmod(0o644)
        original_target = target.stat()
        self.config.symlink_to(target)
        self.assert_success(self.install())
        self.assert_regular_config(LOCAL_CONFIG)
        backups = list(self.config.parent.glob("config.toml.bak.*"))
        self.assertEqual(len(backups), 1)
        self.assertTrue(backups[0].is_symlink())
        self.assertEqual(os.readlink(backups[0]), str(target))
        self.assertEqual(target.read_bytes(), LOCAL_CONFIG)
        self.assertEqual(target.stat().st_mode, original_target.st_mode)
        self.assertEqual(target.stat().st_ino, original_target.st_ino)
        self.assert_managed_links()
        before = snapshot(self.root)
        self.assert_success(self.install())
        self.assertEqual(snapshot(self.root), before)

    def test_owned_dangling_link_is_rejected_even_with_force(self):
        self.prepare_config_parent()
        self.config.symlink_to(self.repo / "config.toml")
        for args in ((), ("--force",)):
            with self.subTest(args=args):
                self.assert_rejected_without_writes(*args)

    def test_foreign_live_link_is_rejected_even_with_force(self):
        self.prepare_config_parent()
        target = self.root / "foreign.toml"
        target.write_bytes(LOCAL_CONFIG)
        self.config.symlink_to(target)
        for args in ((), ("--force",)):
            with self.subTest(args=args):
                self.assert_rejected_without_writes(*args)

    def test_foreign_dangling_link_is_rejected_even_with_force(self):
        self.prepare_config_parent()
        self.config.symlink_to(self.root / "foreign-missing.toml")
        for args in ((), ("--force",)):
            with self.subTest(args=args):
                self.assert_rejected_without_writes(*args)

    def test_relative_link_to_owned_target_is_foreign(self):
        self.prepare_config_parent()
        target = self.repo / "config.toml"
        target.write_bytes(LOCAL_CONFIG)
        self.config.symlink_to(os.path.relpath(target, self.config.parent))
        for args in ((), ("--force",)):
            with self.subTest(args=args):
                self.assert_rejected_without_writes(*args)

    def test_nonregular_config_directory_is_rejected_even_with_force(self):
        self.config.mkdir(parents=True)
        (self.config / "keep.txt").write_text("fixture\n")
        for args in ((), ("--force",)):
            with self.subTest(args=args):
                self.assert_rejected_without_writes(*args)

    def test_agents_conflict_prevents_config_creation(self):
        self.prepare_config_parent()
        self.agents.write_text("Local instructions\n")
        self.assert_rejected_without_writes()

    def test_agents_conflict_prevents_config_migration(self):
        self.prepare_config_parent()
        self.agents.write_text("Local instructions\n")
        target = self.repo / "config.toml"
        target.write_bytes(LOCAL_CONFIG)
        self.config.symlink_to(target)
        self.assert_rejected_without_writes()

    def test_force_backs_up_managed_conflict_and_preserves_regular_config(self):
        self.prepare_config_parent()
        self.agents.write_text("Local instructions\n")
        self.config.write_bytes(LOCAL_CONFIG)
        self.config.chmod(0o640)
        inode = self.config.stat().st_ino
        self.assert_success(self.install("--force"))
        self.assert_regular_config(LOCAL_CONFIG, 0o640)
        self.assertEqual(self.config.stat().st_ino, inode)
        backups = list(self.agents.parent.glob("AGENTS.md.bak.*"))
        self.assertEqual(len(backups), 1)
        self.assertEqual(backups[0].read_text(), "Local instructions\n")
        self.assert_managed_links()

    def test_missing_example_fails_before_installation_writes(self):
        (self.repo / "config.example.toml").unlink()
        self.assert_rejected_without_writes()

    def test_missing_example_with_force_fails_before_installation_writes(self):
        (self.repo / "config.example.toml").unlink()
        self.assert_rejected_without_writes("--force")


if __name__ == "__main__":
    unittest.main(verbosity=2)
