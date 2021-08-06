from logging import RootLogger
from django.shortcuts import render
from django.core.files.storage import default_storage
from django.contrib import messages
from markdown2 import Markdown

from . import util


markdowner = Markdown()

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry):
    data = util.get_entry(entry)
    if data != None:
        return render(request, "encyclopedia/entry.html", {
            "entry" : markdowner.convert(data),
            "title" : entry
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "entry" : "Sorry requested page not found"
        })

def search(request):
    
    if request.method == "POST" and request.POST.get("q"):
        
        query = request.POST.get("q")
        data = util.get_entry(query)
        #check if a title matches the search query
        if data != None:
            return render(request, "encyclopedia/entry.html", {
                "entry" : markdowner.convert(data),
                "title" : query
            })

        #search fn parsing for substring
        entries = util.list_entries()
        results = []
        for entry in entries:
            if query.lower() in entry.lower():
                #print("found")
                results.append(entry)

        #print(results)
        #print(len(results))
        
        return render(request,"encyclopedia/search.html", {
            "query" : query,
            "results" : results
        })

    return render(request, "encyclopedia/index.html")


def newpage(request):
    if request.method == "POST":

        title = request.POST.get("title")
        
        #check if inputs are empty
        if not title:
            messages.error(request, "Please provide a title")
            return render(request, "encyclopedia/newpage.html")

        content = request.POST.get("content")
        #print(content)
        if not content:
            messages.error(request, "Please provide some content")
            return render(request, "encyclopedia/newpage.html")

        #returns error if title is already in use
        if util.get_entry(title) != None:
            messages.error(request, "Title already taken")
            return render(request, "encyclopedia/newpage.html")

        #this removes duplicate newlines
        content = content.replace("\r","  ")
        #writes inputs to new file
        util.save_entry(title,content)
        #f = open("entries/"+str(title)+".md", "a")
        #f.write(content)
        #f.close()
        
        #displays new entry
        data = util.get_entry(title)
        #print(data)
        return render(request, "encyclopedia/entry.html", {
            "entry": markdowner.convert(data),
            "title" : title
        })

    #for error checking
    #print("method is not post")
    return render(request, "encyclopedia/newpage.html")


def edit(request):

    title = request.GET.get("title")
    #print(title)
    content = util.get_entry(title)
    
    if request.method == "POST":

        
        title = request.POST.get("title")
        
        #print(title)

        #check if inputs are empty
        content = request.POST.get("content")
        
        #print(content)
        if not content:
            #print("content empty")
            messages.error(request, "Please provide some content")
            return render(request, "encyclopedia/newpage.html")

        #this removes duplicate newlines
        content = content.replace("\r","  ")
        #writes inputs to new file
        util.save_entry(title,content)
        #f = open("entries/"+str(title)+".md", "w")
        #f.write(content)
        #f.close()
        
        #displays new entry
        data = util.get_entry(title)
        return render(request, "encyclopedia/entry.html", {
            "entry": markdowner.convert(data),
            "title" : title
        })

    #for error checking
    #print("method is not post")
    return render(request, "encyclopedia/edit.html", {
        "title" : title,
        "content" : content
    })

def random(request):

    import random

    
    entries = util.list_entries()
    entry = random.choice(entries)
    

    #print("Random: "+ entry)
    
    data = util.get_entry(entry)
    return render(request, "encyclopedia/entry.html", {
        "entry": markdowner.convert(data),
        "title" : entry
    })