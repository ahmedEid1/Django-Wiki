from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse

import random
import markdown2

from . import util
from .forms import EntryForm, EditForm


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    content = util.get_entry(title)

    if content is None:
        response = render(request, "encyclopedia/404.html")
        response.status_code = 404
        return response

    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": markdown2.markdown(content)
    })


def search(request):
    query = request.GET["q"].upper()
    entry_list = util.list_entries()

    for i in range(len(entry_list)):
        entry_list[i] = entry_list[i].upper()

    if query in entry_list:
        return redirect(reverse("entry", args=[query]))

    result = []
    for title in entry_list:
        if query in title:
            result.append(title)

    return render(request, 'encyclopedia/result.html', {"entries": result})


def new_entry(request):
    if request.method == "POST":
        form = EntryForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            new_title = data['title'].upper()

            for title in util.list_entries():
                if new_title == title.upper():
                    return render(request, "encyclopedia/new_entry.html", {'form': form, 'error': True})

            util.save_entry(data['title'], data['content'])
            return redirect(reverse('entry', args=[new_title]))

        else:
            return render(request, "encyclopedia/new_entry.html", {'form': form, 'error': False})

    return render(request, "encyclopedia/new_entry.html", {'form': EntryForm(), 'error': False})


def edit(request, title):
    content = util.get_entry(title)

    if content is None:
        response = render(request, "encyclopedia/404.html")
        response.status_code = 404
        return response

    if request.method == "POST":
        form = EditForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            util.save_entry(title, data['content'])
            return redirect(reverse("entry", args=[title]))

        else:
            return render(request, "encyclopedia/edit.html", {
                "title": title,
                "form": EditForm({"content": content})
            })

    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "form": EditForm({"content": content})
    })


def random_entry(request):
    entries_list = util.list_entries()
    title = entries_list[random.randint(0, len(entries_list)) - 1]

    return redirect(reverse('entry', args=[title]))