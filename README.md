# dotfiles-codex

Codex のユーザー向けグローバル設定のうち、公開して安全な指示・custom agent・skill を管理するリポジトリです。

## 構成

| パス | 配置先 | 内容 |
| --- | --- | --- |
| `AGENTS.md` | `~/.codex/AGENTS.md` | 全リポジトリ共通の作業・レビュー・Git 方針 |
| `config.toml` | `~/.codex/config.toml` | Codex のユーザー設定。ここでは subagent の並列数だけを設定 |
| `agents/*.toml` | `~/.codex/agents/` | custom agent 定義 |
| `skills/*/SKILL.md` | `~/.agents/skills/` | 再利用可能なワークフロー |
| `install.sh` | 任意 | 競合を事前検査してからシンボリックリンクを作成 |
| `scripts/verify.py` | 任意 | TOML、agent 制約、skill frontmatter の構造検証 |

## Claude 設定からの主な変更

- `CLAUDE.md` を Codex が自動検出する `AGENTS.md` に変更。
- `settings.json` は移植せず、Codex の `config.toml` に置換。
- `agents/*.md` の Claude 用 frontmatter を、Codex custom agent の standalone TOML に変換。
- `commands/fix-github-issue.md` は custom slash command として持たず、明示・暗黙に呼び出せる `fix-github-issue` skill に変更。
- `sonnet` / `opus` / `haiku` の固定指定、Claude 固有の `Agent`・`AskUserQuestion`・`Read/Grep/Glob/Bash` 設定を削除。
- review agent は `sandbox_mode = "read-only"`、実装・テスト agent は `workspace-write` を明示。
- Git 操作は毎回自動実行せず、ユーザーが依頼した範囲だけで行う方針に変更。

## Setup

このディレクトリを設定の source of truth とし、Codex が参照する場所へシンボリックリンクを張ります。リポジトリを移動するとリンクが切れるため、最初に永続的な場所へ配置してください。

```sh
git clone <repository-url> ~/dotfiles-codex
cd ~/dotfiles-codex
```

### 推奨: `install.sh` を使う

最初に構造を検証します:

```sh
python3 scripts/verify.py
```

続いて、このディレクトリから `~/.codex` と `~/.agents/skills` へリンクを作成します:

```sh
./install.sh
```

既存の `~/.codex/AGENTS.md`、`~/.codex/config.toml`、同名 agent/skill がある場合、通常実行は競合を表示し、何も変更せず終了します。既存ファイルを退避してリンクへ置き換える場合だけ `--force` を指定してください。退避名には日時とプロセス ID が付きます:

```sh
./install.sh --force
```

作成されるリンク:

```text
~/.codex/AGENTS.md       -> <repo>/AGENTS.md
~/.codex/config.toml     -> <repo>/config.toml
~/.codex/agents/*.toml   -> <repo>/agents/*.toml
~/.agents/skills/<name>  -> <repo>/skills/<name>
```

### 手動でリンクする

`install.sh` を使わずに設定する場合は、このリポジトリのルートで次を実行します。以下のコマンドは既存ファイルを上書きしないため、同名ファイルがある場合は事前にバックアップまたは統合してください。

```sh
mkdir -p "$HOME/.codex/agents" "$HOME/.agents/skills"

ln -s "$PWD/AGENTS.md" "$HOME/.codex/AGENTS.md"
ln -s "$PWD/config.toml" "$HOME/.codex/config.toml"

for file in "$PWD"/agents/*.toml; do
  ln -s "$file" "$HOME/.codex/agents/$(basename "$file")"
done

for dir in "$PWD"/skills/*; do
  ln -s "$dir" "$HOME/.agents/skills/$(basename "$dir")"
done
```

リンクを確認するには:

```sh
readlink "$HOME/.codex/AGENTS.md"
readlink "$HOME/.codex/config.toml"
find "$HOME/.codex/agents" "$HOME/.agents/skills" -type l -print
```

`config.toml` 全体をすでに個別管理している場合は、このリポジトリのファイルへ置き換える前に既存設定を統合してください。特に model、approval、sandbox、MCP、通知などのローカル設定は自動マージされません。

Codex は skill の変更を通常は自動検出します。表示されない場合や `config.toml` を変更した場合は Codex を再起動してください。

## 管理しないもの

資格情報 (`auth.json` や OS keychain)、会話履歴、ログ、キャッシュ、セッション状態、端末固有の override はコミットしません。MCP や connector の認証状態もこのリポジトリには含めません。

## 追加候補

- GitHub issue/PR を頻繁に扱う場合は GitHub connector を有効化すると、サインイン済みの private repository にも安全にアクセスしやすくなります。
- チーム配布したくなったら、複数 skill と依存関係をまとめた Codex plugin へ昇格させるのが適切です。
- リポジトリ固有のコマンドや検証手順は、グローバル `AGENTS.md` ではなく各リポジトリの `AGENTS.md` に置いてください。
