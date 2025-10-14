---
layout: default
title: 主题标签
permalink: /tags/
---

# 主题标签

{% assign themes = site.data.theme_tags.theme_tags %}

<ul>
{% for theme in themes %}
  {% comment %}统计含同义标签的文章数量{% endcomment %}
  {% assign count = 0 %}
  {% for post in site.posts %}
    {% assign matched = false %}
    {% for syn in theme.synonyms %}
      {% if post.tags contains syn %}
        {% assign matched = true %}
      {% endif %}
    {% endfor %}
    {% if matched %}
      {% assign count = count | plus: 1 %}
    {% endif %}
  {% endfor %}
  <li>
    <a href="/tags/{{ theme.slug }}/">{{ theme.name }}</a>（{{ count }} 篇）
  </li>
{% endfor %}
</ul>