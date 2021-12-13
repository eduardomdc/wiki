from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django import forms
import random
import markdown2
from . import util

class SearchForm(forms.Form):
    query = forms.CharField(label="query")

class ArticleForm(forms.Form):
    content = forms.CharField(label="content")
    title = forms.CharField(label="title")

class EditForm(forms.Form):
    content = forms.CharField(label="content")

def search(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data["query"]
            if query in util.list_entries():
                return render(request, "encyclopedia/article.html",{
                    "article": markdown2.markdown(util.get_entry(query)),
                    "title": query,
                    })
            else:
                results = []
                for article in util.list_entries():
                    if query in article:
                        results.append(article)
                return render(request, "encyclopedia/search.html",{
                    "results": results,
                    "query": query,
                    })
        else:
            return render(request, "encyclopedia/index.html", {
                "entries": util.list_entries()
                })
    else:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries()
            })

def newpage(request):
    if request.method == "GET":
        return render(request, "encyclopedia/newpage.html")
    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data["content"]
            title = form.cleaned_data["title"]
            if title in util.list_entries():
                messages.error(request, 'ERROR: There already is an article with that title.')
                return render(request, "encyclopedia/newpage.html")
            else:
                util.save_entry(title, content)
                return redirect('wiki',title)

        else:
            return render(request, "encyclopedia/newpage.html")

def editpage(request, title):
    if request.method == "GET":
        return render(request, "encyclopedia/editpage.html",{
            "title": title,
            "content": util.get_entry(title),
            })
    if request.method == "POST":
        form = EditForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            return redirect('wiki',title)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
        })

def article(request, title):
    if title in util.list_entries():
        return render(request, "encyclopedia/article.html",{
            "article": markdown2.markdown(util.get_entry(title)),
            "title": title,
            })
    else:
        return render(request, 'encyclopedia/missingpage.html')

def randompage(request):
    return redirect('wiki', random.choice(util.list_entries()))