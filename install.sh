#!/bin/sh
set -eu

usage() {
  printf '%s\n' "Usage: $0 [--force]"
  printf '%s\n' "  --force  back up conflicting destinations before linking"
}

force=false
case "${1-}" in
  "") ;;
  --force) force=true ;;
  -h|--help) usage; exit 0 ;;
  *) usage >&2; exit 2 ;;
esac

repo_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
backup_suffix=".bak.$(date '+%Y%m%d-%H%M%S').$$"
conflicts=0

is_current_link() {
  [ -L "$2" ] && [ "$(readlink "$2")" = "$1" ]
}

preflight() {
  source_path=$1
  destination=$2

  if is_current_link "$source_path" "$destination"; then
    return
  fi
  if [ -e "$destination" ] || [ -L "$destination" ]; then
    if [ "$force" = false ]; then
      printf '%s\n' "Conflict: $destination" >&2
      conflicts=$((conflicts + 1))
    fi
  fi
}

preflight "$repo_dir/AGENTS.md" "$HOME/.codex/AGENTS.md"
preflight "$repo_dir/config.toml" "$HOME/.codex/config.toml"
for source_path in "$repo_dir"/agents/*.toml; do
  preflight "$source_path" "$HOME/.codex/agents/$(basename "$source_path")"
done
for source_path in "$repo_dir"/skills/*; do
  preflight "$source_path" "$HOME/.agents/skills/$(basename "$source_path")"
done

if [ "$conflicts" -gt 0 ]; then
  printf '%s\n' "Nothing was changed. Re-run with --force to back up conflicts." >&2
  exit 1
fi

mkdir -p "$HOME/.codex/agents" "$HOME/.agents/skills"

link_path() {
  source_path=$1
  destination=$2

  if is_current_link "$source_path" "$destination"; then
    return
  fi
  if [ -e "$destination" ] || [ -L "$destination" ]; then
    backup_path="${destination}${backup_suffix}"
    mv "$destination" "$backup_path"
    printf '%s\n' "Backed up $destination -> $backup_path"
  fi
  ln -s "$source_path" "$destination"
  printf '%s\n' "Linked $destination -> $source_path"
}

link_path "$repo_dir/AGENTS.md" "$HOME/.codex/AGENTS.md"
link_path "$repo_dir/config.toml" "$HOME/.codex/config.toml"
for source_path in "$repo_dir"/agents/*.toml; do
  link_path "$source_path" "$HOME/.codex/agents/$(basename "$source_path")"
done
for source_path in "$repo_dir"/skills/*; do
  link_path "$source_path" "$HOME/.agents/skills/$(basename "$source_path")"
done

printf '%s\n' "Installed Codex configuration from $repo_dir"

