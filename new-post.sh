#!/usr/bin/env bash
set -euo pipefail

# Quick Jekyll post creator
# Usage:
#   ./new-post.sh "Post Title" [date] [category]
# - date format: YYYY-MM-DD (default: today)
# - category optional; will be added to front matter categories

TITLE=${1:-}
DATE=${2:-}
CATEGORY=${3:-}

if [[ -z "$TITLE" ]]; then
  echo "Usage: $0 \"Post Title\" [date] [category]"
  exit 1
fi

if [[ -z "$DATE" ]]; then
  DATE=$(date +%Y-%m-%d)
fi

# slugify title: lowercase, spaces to hyphens, remove non-alphanum except hyphen
SLUG=$(echo "$TITLE" | iconv -t ascii//TRANSLIT | tr '[:upper:]' '[:lower:]' | sed -E 's/[^a-z0-9]+/-/g; s/^-+|-+$//g')

POST_DIR="_posts"
mkdir -p "$POST_DIR"

FILENAME="$POST_DIR/${DATE}-${SLUG}.md"

if [[ -f "$FILENAME" ]]; then
  echo "File already exists: $FILENAME"
  exit 1
fi

cat > "$FILENAME" <<EOF
---
layout: post
title: "$TITLE"
date: ${DATE} 00:00:00 +0800
categories: [${CATEGORY}]
tags: []
---

> 写作提示：在这里开始你的正文内容。

## 小节标题

正文内容……

EOF

echo "Created: $FILENAME"
echo "You can edit it now. To preview:"
echo "  bundle exec jekyll serve --host 0.0.0.0 --port 4000"