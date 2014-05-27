# coding: utf-8
from django.http import HttpResponse, Http404
from django.shortcuts import render


def ajax_sso(request):
    if not request.is_ajax():
        raise Http404
    return render(request, 'disqus/ajax_sso.js')


def ajax_show_comments(request):
    if not request.is_ajax():
        raise Http404
    return render(request, 'disqus/ajax_show_comments.js')
