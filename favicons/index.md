---
layout: default
title: 站点 Favicon 预览
permalink: /favicons/
---

<h1>选择站点 Favicon</h1>
<p>下方为 6 个候选图标（PNG 预览），你可以浏览并告诉我选用编号。</p>

<style>
.fav-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(180px, 1fr)); gap: 16px; }
.fav-item { border: 1px solid #e5e5e5; padding: 12px; border-radius: 8px; background: #fafafa; }
.fav-item h3 { margin: 6px 0 10px; font-size: 16px; }
.fav-item img { width: 128px; height: 128px; image-rendering: crisp-edges; }
.file-links { font-size: 12px; color: #777; margin-top: 8px; }
</style>

<div class="fav-grid">
  {% assign options = (1..6) %}
  {% for i in options %}
    <div class="fav-item">
      <h3>选项 {{ i }}</h3>
      <img alt="favicon 预览 {{ i }}" src="/assets/favicons/fav{{ i }}.png" />
      <div class="file-links">
        PNG: <code>/assets/favicons/fav{{ i }}.png</code><br/>
        ICO: <code>/assets/favicons/fav{{ i }}.ico</code>
      </div>
    </div>
  {% endfor %}
  </div>

<p>请在这里告诉我你最终选择的编号（1~6）。我会将对应的 <code>.ico</code> 文件复制到站点根目录并命名为 <code>favicon.ico</code>。</p>