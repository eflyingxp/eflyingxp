---
layout: default
title: 首页
---

## 最新文章

{% for post in site.posts limit:5 %}
- [{{ post.title }}]({{ post.url }}) - {{ post.date | date: "%Y-%m-%d" }}
{% endfor %}

## 分类

- [技术笔记](/tech/)
- [生活随笔](/life/)  
- [旅游攻略](/travel/)

## 关于我

一个热爱技术和生活的程序员，喜欢记录和分享。

---

本博客使用 [Jekyll](https://jekyllrb.com/) 构建，托管在 [GitHub Pages](https://pages.github.com/) 上。