{% load disqus_tags %}

{% if user.is_authenticated %}
    {% disqus_sso javascript_only=True %}
{% else %}
    /* user not authenticated */
{% endif %}
