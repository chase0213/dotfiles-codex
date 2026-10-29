# dotfiles-codex

Codex のユーザー向けグローバル設定のうち、公開して安全な指示・custom agent・skill を管理するリポジトリです。

## 構成

| パス | 配置先 | 内容 |
| --- | --- | --- |
| `AGENTS.md` | `~/.codex/AGENTS.md` | 全リポジトリ共通の作業・レビュー・Git 方針 |
| `config.example.toml` | 初回のみ `~/.codex/config.toml` へコピー | 公開可能な初期設定。実際の設定は端末ローカルで管理 |
| `agents/*.toml` | `~/.codex/agents/` | custom agent 定義 |
| `skills/*/SKILL.md` | `~/.agents/skills/` | 再利用可能なワークフロー |
| `install.sh` | 任意 | 競合を事前検査してからシンボリックリンクを作成 |
| `scripts/verify.py` | 任意 | TOML、agent 制約、skill frontmatter の構造検証 |
| `scripts/test_install.py` | 任意 | 一時ディレクトリでインストール・旧設定リンク移行を検証 |

## Claude 設定からの主な変更

- `CLAUDE.md` を Codex が自動検出する `AGENTS.md` に変更。
- `settings.json` は移植せず、Codex の `config.example.toml` に置換。
- `agents/*.md` の Claude 用 frontmatter を、Codex custom agent の standalone TOML に変換。
- `commands/fix-github-issue.md` は custom slash command として持たず、明示・暗黙に呼び出せる `fix-github-issue` skill に変更。
- `sonnet` / `opus` / `haiku` の固定指定、Claude 固有の `Agent`・`AskUserQuestion`・`Read/Grep/Glob/Bash` 設定を削除。
- review agent は `sandbox_mode = "read-only"`、実装・テスト agent は `workspace-write` を明示。
- Git 操作は毎回自動実行せず、ユーザーが依頼した範囲だけで行う方針に変更。

## ワークフローの使い分け

常設指示は作業・検証・Git の基本方針に絞り、詳細は必要な skill だけ読みます。

- `feature-dev`: 大きい・曖昧な機能の設計と統合。承認・委任・モデル切り替えを一律に要求しません。
- `multi-review`: 変更の挙動とリスクに関係する観点を選択。固定人数での起動はしません。
- `red-team`: 実際の信頼境界に沿った攻撃シナリオを検証。件数ノルマは設けません。
- `human-review`: レビュー資料の依頼時、または人間の判断を伴う引き渡し時に、意思決定の経緯を含む HTML を作成。通常の完了報告では不要です。

## Reviewability の方針

内部の思考過程を忠実に再生できるとはみなさず、人間が技術判断を検証できる証拠と経緯を残します。

- 非自明な作業では、開始時の問題・前提・完了条件と、方針を変えた重要な観測を簡潔に記録します。全コマンドの逐語的な作業日誌にはしません。
- `feature-dev` は、観測した証拠、変わった判断、次の方針を開発中のチェックポイントとして残します。
- `human-review` は、問題認識、調査結果、選択、試行、方針転換、到達点を重要な転換点に絞って時系列に再構成します。
- 同時点のメッセージ、コード差分、テスト結果、実行ログに基づく事実と、最終成果物から事後的に推定した説明を区別します。記録にない比較検討や失敗を創作しません。
- `multi-review` は説明を証拠そのものとは扱わず、重要な主張をコードや検証結果と照合します。

## Setup

このディレクトリを共有設定の source of truth とし、`AGENTS.md`、custom agent、skill を Codex が参照する場所へシンボリックリンクで配置します。リポジトリを移動するとリンクが切れるため、最初に永続的な場所へ配置してください。

`~/.codex/config.toml` だけはリンクしません。Codex がプロジェクトの trust、marketplace、plugin、UI 状態など端末固有情報を書き込むため、通常ファイルとしてローカル管理します。

```sh
git clone <repository-url> ~/dotfiles-codex
cd ~/dotfiles-codex
```

### 推奨: `install.sh` を使う

最初に構造を検証します:

```sh
python3 scripts/verify.py
```

続いて、このディレクトリから `~/.codex` と `~/.agents/skills` へリンクを作成します。`~/.codex/config.toml` が存在しない場合だけ、`config.example.toml` から通常ファイルを作成します。既存の通常ファイルは変更しません。旧版が作成した、このリポジトリの `config.toml` への読み取り可能なリンクは、内容を保持した通常ファイルへ移行します:

```sh
./install.sh
```

既存の `~/.codex/AGENTS.md` または同名 agent/skill がある場合、通常実行は競合を表示し、何も変更せず終了します。既存の管理対象を退避してリンクへ置き換える場合だけ `--force` を指定してください。退避名には日時とプロセス ID が付きます。`--force` でも既存の通常ファイルの `config.toml` は置き換えません。切れた設定リンクや他の場所を参照する設定リンクは、`--force` にかかわらず変更前に停止します:

```sh
./install.sh --force
```

作成されるリンク:

```text
~/.codex/AGENTS.md       -> <repo>/AGENTS.md
~/.codex/agents/*.toml   -> <repo>/agents/*.toml
~/.agents/skills/<name>  -> <repo>/skills/<name>

~/.codex/config.toml     通常ファイル（シンボリックリンクにしない）
```

### Migrating legacy config links

旧版は `~/.codex/config.toml -> <repo>/config.toml` を作成していました。新しい版ではリポジトリ内の実設定を削除するため、旧リンクを使っているPCは **更新前に設定のバックアップ** を取ってください。Codex を終了してから実行すると、移行中の設定書き込みとの競合を避けられます。

```sh
if [ -L "$HOME/.codex/config.toml" ] && [ -f "$HOME/.codex/config.toml" ]; then
  config_backup="$HOME/.codex/config.toml.before-update.$(date '+%Y%m%d-%H%M%S').$$"
  (umask 077; cat "$HOME/.codex/config.toml" > "$config_backup")
fi

git pull --ff-only
python3 scripts/verify.py
./install.sh
```

- 旧リンク先が読める場合: 内容を権限 `600` の一時ファイルへコピーしてから通常ファイルに置き換えます。元のリンクは日時付きで退避し、元のファイルは変更しません。再実行では移行済みの通常ファイルを保持します。
- 旧リンク先が消えている場合: 設定を推測して初期化せず、何も変更する前にエラーで停止します。リンクを退避し、バックアップを `~/.codex/config.toml` の通常ファイルとして復元（権限 `600`）してから再実行してください。
- 他の場所へのリンク、ディレクトリ等の場合: 自動移行しません。参照先と設定内容を確認し、通常ファイルとして用意してください。

設定の復元が不要で、サンプルの初期値に戻してよいと判断した場合だけ、切れたリンクを退避して再実行できます。この操作では以前の設定は復元されません。

```sh
mv "$HOME/.codex/config.toml" "$HOME/.codex/config.toml.broken.$(date '+%Y%m%d-%H%M%S').$$"
./install.sh
```

開発時の回帰テスト:

```sh
python3 scripts/test_install.py
```

テストは一時コピーの配置先参照だけをテスト用変数に置き換え、実際のホーム設定には触れません。

### 手動でリンクする

以下は新規配置用です。旧設定リンクの移行には上記の手順または `install.sh` を使ってください。`install.sh` を使わずに設定する場合は、このリポジトリのルートで次を実行します。以下のコマンドは既存ファイルを上書きしないため、同名ファイルがある場合は事前にバックアップまたは統合してください。

```sh
mkdir -p "$HOME/.codex/agents" "$HOME/.agents/skills"

ln -s "$PWD/AGENTS.md" "$HOME/.codex/AGENTS.md"

if [ ! -e "$HOME/.codex/config.toml" ] && [ ! -L "$HOME/.codex/config.toml" ]; then
  install -m 600 "$PWD/config.example.toml" "$HOME/.codex/config.toml"
fi

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
find "$HOME/.codex/agents" "$HOME/.agents/skills" -type l -print
test -f "$HOME/.codex/config.toml" && test ! -L "$HOME/.codex/config.toml"
```

`config.example.toml` は新しい端末用の初期値です。model、approval、sandbox、MCP、通知、プロジェクト trust、plugin 状態などは `~/.codex/config.toml` で端末ごとに管理し、このリポジトリにはコミットしません。

Codex は skill の変更を通常は自動検出します。表示されない場合や `config.toml` を変更した場合は Codex を再起動してください。

## 管理しないもの

実際の `config.toml`、資格情報 (`auth.json` や OS keychain)、会話履歴、ログ、キャッシュ、セッション状態、端末固有の override はコミットしません。MCP や connector の認証状態もこのリポジトリには含めません。

## 追加候補

- GitHub issue/PR を頻繁に扱う場合は GitHub connector を有効化すると、サインイン済みの private repository にも安全にアクセスしやすくなります。
- チーム配布したくなったら、複数 skill と依存関係をまとめた Codex plugin へ昇格させるのが適切です。
- リポジトリ固有のコマンドや検証手順は、グローバル `AGENTS.md` ではなく各リポジトリの `AGENTS.md` に置いてください。
