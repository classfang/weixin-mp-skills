#!/usr/bin/env bash
set -Eeuo pipefail

REPO_URL="${WEIXIN_MP_SKILLS_REPO_URL:-https://github.com/classfang/weixin-mp-skills.git}"
BRANCH="${WEIXIN_MP_SKILLS_BRANCH:-main}"
CACHE_ROOT="${XDG_CACHE_HOME:-$HOME/.cache}"
DEFAULT_REPO_DIR="${WEIXIN_MP_SKILLS_REPO_DIR:-$CACHE_ROOT/weixin-mp-skills}"
DEST_DIR="${CODEX_HOME:-$HOME/.codex}/skills"
REPO_DIR=""
PULL_REPO=1
DRY_RUN=0
RSYNC_EXCLUDES=(
  --exclude '.DS_Store'
  --exclude '__pycache__/'
  --exclude '*.pyc'
  --exclude '*.pyo'
  --exclude '.pytest_cache/'
  --exclude '.mypy_cache/'
  --exclude '.ruff_cache/'
  --exclude '.env'
)

usage() {
  cat <<EOF
Usage: scripts/update-skills.sh [options]

Clone or update this repository, then sync every top-level skill directory into
your Codex skills directory.

Options:
  --repo DIR       Local repository path. Defaults to the current repo when the
                   script is run from a checkout; otherwise $DEFAULT_REPO_DIR.
  --repo-url URL   Git repository URL. Default: $REPO_URL
  --branch NAME    Branch used when cloning a missing repo. Default: $BRANCH
  --dest DIR       Target skills directory. Default: $DEST_DIR
  --no-pull        Do not run git clone/pull; sync from the existing local repo.
  --dry-run        Print the planned git/rsync actions without writing files.
  -h, --help       Show this help.

Environment:
  CODEX_HOME, WEIXIN_MP_SKILLS_REPO_URL, WEIXIN_MP_SKILLS_BRANCH,
  WEIXIN_MP_SKILLS_REPO_DIR, XDG_CACHE_HOME
EOF
}

log() {
  printf '==> %s\n' "$*"
}

die() {
  printf 'error: %s\n' "$*" >&2
  exit 1
}

expand_path() {
  case "$1" in
    "~")
      printf '%s\n' "$HOME"
      ;;
    "~/"*)
      printf '%s/%s\n' "$HOME" "${1#~/}"
      ;;
    *)
      printf '%s\n' "$1"
      ;;
  esac
}

has_skill_dirs() {
  [[ -n "$(find "$1" -mindepth 2 -maxdepth 2 -type f -name SKILL.md -print -quit 2>/dev/null)" ]]
}

script_repo_dir() {
  local source_path script_dir repo_root
  source_path="${BASH_SOURCE[0]:-}"

  if [[ -z "$source_path" || ! -e "$source_path" ]]; then
    return 1
  fi

  script_dir="$(cd -- "$(dirname -- "$source_path")" >/dev/null 2>&1 && pwd -P)" || return 1
  repo_root="$(cd -- "$script_dir/.." >/dev/null 2>&1 && pwd -P)" || return 1

  if [[ -f "$repo_root/README.md" ]] && has_skill_dirs "$repo_root"; then
    printf '%s\n' "$repo_root"
    return 0
  fi

  return 1
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --repo)
      [[ $# -ge 2 ]] || die "--repo requires a path"
      REPO_DIR="$(expand_path "$2")"
      shift 2
      ;;
    --repo-url)
      [[ $# -ge 2 ]] || die "--repo-url requires a URL"
      REPO_URL="$2"
      shift 2
      ;;
    --branch)
      [[ $# -ge 2 ]] || die "--branch requires a branch name"
      BRANCH="$2"
      shift 2
      ;;
    --dest)
      [[ $# -ge 2 ]] || die "--dest requires a path"
      DEST_DIR="$(expand_path "$2")"
      shift 2
      ;;
    --no-pull)
      PULL_REPO=0
      shift
      ;;
    --dry-run)
      DRY_RUN=1
      shift
      ;;
    -h | --help)
      usage
      exit 0
      ;;
    *)
      die "unknown option: $1"
      ;;
  esac
done

if [[ -z "$REPO_DIR" ]]; then
  if REPO_DIR="$(script_repo_dir)"; then
    :
  else
    REPO_DIR="$DEFAULT_REPO_DIR"
  fi
fi

command -v rsync >/dev/null 2>&1 || die "rsync is required"

if [[ ! -d "$REPO_DIR" ]]; then
  command -v git >/dev/null 2>&1 || die "git is required to clone the repo"

  if [[ "$PULL_REPO" -eq 0 ]]; then
    die "local repo does not exist: $REPO_DIR"
  fi

  if [[ "$DRY_RUN" -eq 1 ]]; then
    log "[dry-run] git clone --branch $BRANCH $REPO_URL $REPO_DIR"
    exit 0
  fi

  log "Cloning repository into $REPO_DIR"
  mkdir -p "$(dirname -- "$REPO_DIR")"
  git clone --branch "$BRANCH" "$REPO_URL" "$REPO_DIR"
elif [[ ! -d "$REPO_DIR/.git" ]]; then
  if has_skill_dirs "$REPO_DIR"; then
    if [[ "$PULL_REPO" -eq 1 ]]; then
      log "Local path is not a git repo; skipping git pull for $REPO_DIR"
    fi
  else
    die "path exists but is not a git repository or skill bundle: $REPO_DIR"
  fi
elif [[ "$PULL_REPO" -eq 1 ]]; then
  command -v git >/dev/null 2>&1 || die "git is required to update the repo"

  if [[ -n "$(git -C "$REPO_DIR" status --porcelain --untracked-files=normal)" ]]; then
    if [[ "$DRY_RUN" -eq 1 ]]; then
      log "[dry-run] repo has uncommitted changes; a real run would stop before git pull"
    else
      die "repo has uncommitted changes. Commit/stash them, or rerun with --no-pull."
    fi
  elif [[ "$DRY_RUN" -eq 1 ]]; then
    log "[dry-run] git -C $REPO_DIR pull --ff-only"
  else
    log "Updating repository at $REPO_DIR"
    git -C "$REPO_DIR" pull --ff-only
  fi
fi

skill_dirs=()
while IFS= read -r skill_file; do
  skill_dirs+=("${skill_file%/SKILL.md}")
done < <(cd "$REPO_DIR" && find . -mindepth 2 -maxdepth 2 -type f -name SKILL.md | sort)

if [[ "${#skill_dirs[@]}" -eq 0 ]]; then
  die "no top-level skill directories found in $REPO_DIR"
fi

if [[ "$DRY_RUN" -eq 0 ]]; then
  mkdir -p "$DEST_DIR"
fi

log "Syncing ${#skill_dirs[@]} skill(s) into $DEST_DIR"

for skill_dir in "${skill_dirs[@]}"; do
  skill_dir="${skill_dir#./}"
  source_dir="$REPO_DIR/$skill_dir/"
  target_dir="$DEST_DIR/$(basename -- "$skill_dir")/"

  if [[ "$DRY_RUN" -eq 1 ]]; then
    log "[dry-run] rsync -a --delete $source_dir $target_dir"
    rsync -a --delete --dry-run --itemize-changes \
      "${RSYNC_EXCLUDES[@]}" \
      "$source_dir" "$target_dir" || true
  else
    log "Installing $skill_dir"
    mkdir -p "$target_dir"
    rsync -a --delete \
      "${RSYNC_EXCLUDES[@]}" \
      "$source_dir" "$target_dir"
  fi
done

log "Done. Restart Codex or open a new session to refresh available skills."
