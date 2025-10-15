#!/usr/bin/env bash
set -euo pipefail

# Cross-platform publish script for macOS/Linux
# Usage:
#   bash ./publish.sh "sync: 更新博客"

msg_input="${1:-${PUBLISH_MSG:-sync: 更新博客}}"
timestamp="$(date '+%Y-%m-%d %H:%M')"
commit_msg="${msg_input} (${timestamp})"

# Commit local changes if any
changed="$(git status --porcelain || true)"
if [[ -n "$changed" ]]; then
  git add -A
  git commit -m "$commit_msg"
fi

# Sync with remote and push
git fetch --all --prune
# Rebase to keep history linear
git pull --rebase origin master || true
git push origin master

# Print site URL from CNAME if present
if [[ -f CNAME ]]; then
  domain="$(head -n1 CNAME | tr -d '\r\n')"
else
  domain="blogwego.com"
fi
echo "✅ 已推送到 master，GitHub Pages 将在 1–3 分钟内完成部署"
echo "🔗 访问：https://${domain}/"