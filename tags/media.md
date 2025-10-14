---
layout: default
title: 影视与推荐
permalink: /tags/media/
tag_slug: media
---

{% assign theme = site.data.theme_tags.theme_tags | where: "slug", page.tag_slug | first %}
{% assign synonyms = theme.synonyms %}

# {{ theme.name }}

<ul>
{% for post in site.posts %}
  {% assign matched = false %}
  {% for syn in synonyms %}
    {% if post.tags contains syn %}
      {% assign matched = true %}
    {% endif %}
  {% endfor %}
  {% if matched %}
    <li><a href="{{ post.url }}">{{ post.title }}</a> - {{ post.date | date: "%Y-%m-%d" }}</li>
  {% endif %}
{% endfor %}
</ul>