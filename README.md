# 飞翔的博客

欢迎来到我的个人博客！这里记录着我的生活感悟、技术学习和各种思考。

## 最新文章

{% for post in site.posts limit:5 %}
- [{{ post.title }}]({{ post.url }}) - {{ post.date | date: "%Y-%m-%d" }}
{% endfor %}

## 分类

- [技术笔记](/blog/tech/)
- [生活随笔](/blog/life/)
- [旅游攻略](/blog/travel/)

## 关于我

一个热爱技术和生活的程序员，喜欢记录和分享。

---

本博客使用 [Jekyll](https://jekyllrb.com/) 构建，托管在 [GitHub Pages](https://pages.github.com/) 上。
