from logging import RootLogger
from django.shortcuts import render
from django.core.files.storage import default_storage
from django.contrib import messages
from markdown2 import Markdown

from . import util

# markdowner allows markdown to be converted to html back and forth
markdowner = Markdown()

def index(request):
    # this page will list all entries
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry):
    # this creates a page to display the entry
    data = util.get_entry(entry)

    # if page exists
    if data != None:
        return render(request, "encyclopedia/entry.html", {
            "entry" : markdowner.convert(data),
            "title" : entry
        })

    # if page doesn't exist
    else:
        return render(request, "encyclopedia/entry.html", {
            "entry" : "Sorry requested page not found"
        })

def search(request):
    # This fn allows the user to search for a page using a string.
    if request.method == "POST" and request.POST.get("q"):
        
        query = request.POST.get("q")
        data = util.get_entry(query)

        # check if a title matches the search query
        if data != None:
            return render(request, "encyclopedia/entry.html", {
                "entry" : markdowner.convert(data),
                "title" : query
            })

        # search function parsing all entries for substring
        # This adds all entries that contain the string to a results list
        entries = util.list_entries()
        results = []
        for entry in entries:
            if query.lower() in entry.lower():
                results.append(entry)

        
        return render(request,"encyclopedia/search.html", {
            "query" : query,
            "results" : results
        })

    return render(request, "encyclopedia/index.html")


def newpage(request):
    if request.method == "POST":

        title = request.POST.get("title")
        
        # check if inputs are empty
        if not title:
            messages.error(request, "Please provide a title")
            return render(request, "encyclopedia/newpage.html")

        content = request.POST.get("content")

        if not content:
            messages.error(request, "Please provide some content")
            return render(request, "encyclopedia/newpage.html")

        # returns error if title is already in use
        if util.get_entry(title) != None:
            messages.error(request, "Title already taken")
            return render(request, "encyclopedia/newpage.html")

        # this removes duplicate newlines
        content = content.replace("\r","  ")

        # writes inputs to new file
        util.save_entry(title,content)
        
        
        # displays new entry
        data = util.get_entry(title)
        return render(request, "encyclopedia/entry.html", {
            "entry": markdowner.convert(data),
            "title" : title
        })

    return render(request, "encyclopedia/newpage.html")


def edit(request):

    # autofill previous values
    title = request.GET.get("title")
    content = util.get_entry(title)
    
    if request.method == "POST":

        # take in posted values
        title = request.POST.get("title")
        
        content = request.POST.get("content")
        
        # check if inputs are empty
        if not content:
            messages.error(request, "Please provide some content")
            return render(request, "encyclopedia/newpage.html")

        # this removes duplicate newlines
        content = content.replace("\r","  ")

        # writes inputs to new file
        util.save_entry(title,content)
        
        data = util.get_entry(title)
        return render(request, "encyclopedia/entry.html", {
            "entry": markdowner.convert(data),
            "title" : title
        })


    return render(request, "encyclopedia/edit.html", {
        "title" : title,
        "content" : content
    })

def random(request):
    # This allows the user to go to a random wiki entry

    import random
    
    entries = util.list_entries()
    entry = random.choice(entries)
    
    data = util.get_entry(entry)
    return render(request, "encyclopedia/entry.html", {
        "entry": markdowner.convert(data),
        "title" : entry
    })