from django.core.paginator import Paginator

def get_paginator(request, posts):
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number) # paginator.get_page(None) is the same as paginator.get_page(1)
    return page_obj