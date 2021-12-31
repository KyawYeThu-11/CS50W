from django.shortcuts import render
from markdown2 import Markdown
from random import choice
from . import util
from django.urls import reverse
from django.http import HttpResponseRedirect


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    markdowner = Markdown()
    content = util.get_entry(title)
    #if there is such entry
    if content:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": markdowner.convert(content)
        })
    else:
        return render(request, "encyclopedia/error.html", {
            "link": "See All Available Entries"
        })

def search(request):
    query = request.GET.get("q")
    entries = util.list_entries()
    #if the query is exactly the same as one of the existing entries
    if query in entries:
        return HttpResponseRedirect(f"wiki/{ query }")
    results = []
    for entry in entries:
        if entry.upper().startswith(query.upper()):
            results.append(entry)
    
    return render(request, "encyclopedia/index.html", {    
        "entries": results
    })

def create(request):
    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')
        entries = util.list_entries()
        #if the added title already exists
        if title in entries:
            return render(request, "encyclopedia/create.html", {
                "message":"The title already exists! Please enter another title.",
                "content":content
            })
        else:
            util.save_entry(title, content)
            return HttpResponseRedirect(f"wiki/{title}")
    else:  
        return render(request, "encyclopedia/create.html")


def edit(request):
    if request.method =="POST":
        title = request.POST.get('title')
        content = request.POST.get('content')
        util.save_entry(title, content)
        return HttpResponseRedirect(f"wiki/{ title }")
        
    else:    
        title = request.GET.get('title')
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content": content
        })

def random(request):
    entries = util.list_entries()
    entry = choice(entries)
    return HttpResponseRedirect(f"wiki/{ entry }")




