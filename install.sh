#!/bin/sh
set -eu

usage() {
  printf '%s\n' "Usage: $0 [--force]"
  printf '%s\n' "  --force  back up conflicting managed links before replacing them"
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
for source_path in "$repo_dir"/agents/*.toml; do
  preflight "$source_path" "$HOME/.codex/agents/$(basename "$source_path")"
done
for source_path in "$repo_dir"/skills/*; do
  preflight "$source_path" "$HOME/.agents/skills/$(basename "$source_path")"
done

config_destination="$HOME/.codex/config.toml"
config_action=keep
config_source="$repo_dir/config.example.toml"
if [ -L "$config_destination" ]; then
  if ! is_current_link "$repo_dir/config.toml" "$config_destination"; then
    printf '%s\n' "Config link is not managed by this repository: $config_destination" >&2
    printf '%s\n' "Preserve its contents and replace it with a regular local file before retrying; --force does not replace config links." >&2
    conflicts=$((conflicts + 1))
  elif [ ! -f "$config_destination" ] || [ ! -r "$config_destination" ]; then
    printf '%s\n' "Legacy config link has no readable regular target: $config_destination" >&2
    printf '%s\n' "Restore the old config from backup before retrying. To explicitly start from defaults, move the broken link aside, then rerun. See README: Migrating legacy config links." >&2
    conflicts=$((conflicts + 1))
  else
    config_action=migrate
    config_source="$config_destination"
  fi
elif [ -e "$config_destination" ]; then
  if [ ! -f "$config_destination" ]; then
    printf '%s\n' "Config destination is not a regular file: $config_destination" >&2
    conflicts=$((conflicts + 1))
  fi
else
  config_action=create
  if [ ! -f "$config_source" ] || [ ! -r "$config_source" ]; then
    printf '%s\n' "Missing or unreadable config template: $config_source" >&2
    conflicts=$((conflicts + 1))
  fi
fi

if [ "$conflicts" -gt 0 ]; then
  printf '%s\n' "Nothing was changed. Resolve conflicts first; --force only backs up AGENTS, agent, and skill destinations." >&2
  exit 1
fi

mkdir -p "$HOME/.codex/agents" "$HOME/.agents/skills"

if [ "$config_action" = keep ]; then
  printf '%s\n' "Kept machine-local config: $config_destination"
else
  config_temp=$(mktemp "$HOME/.codex/.config.toml.XXXXXX")
  trap 'rm -f "$config_temp"' 0
  trap 'exit 1' 1 2 3 15
  cat "$config_source" > "$config_temp"
  chmod 600 "$config_temp"
  if [ "$config_action" = migrate ]; then
    config_backup="${config_destination}${backup_suffix}"
    mv "$config_destination" "$config_backup"
    if ! mv "$config_temp" "$config_destination"; then
      mv "$config_backup" "$config_destination"
      exit 1
    fi
    printf '%s\n' "Migrated legacy config to a local file; old link backed up at $config_backup"
  else
    mv "$config_temp" "$config_destination"
    printf '%s\n' "Created machine-local config from config.example.toml: $config_destination"
  fi
  trap - 0 1 2 3 15
fi

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
for source_path in "$repo_dir"/agents/*.toml; do
  link_path "$source_path" "$HOME/.codex/agents/$(basename "$source_path")"
done
for source_path in "$repo_dir"/skills/*; do
  link_path "$source_path" "$HOME/.agents/skills/$(basename "$source_path")"
done

printf '%s\n' "Installed Codex configuration from $repo_dir"
