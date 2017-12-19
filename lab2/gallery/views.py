from django.shortcuts import render
from gallery.database import Database
from django.http import JsonResponse


class Object(object):
    pass


db = Database()


def hello(request):
    if request.method == "POST":
        if request.POST.get("q", "") == "load":
            db.fill_tables()
            print("SUCCESS LOAD")
        elif request.POST.get("q", "") == "save":
            db.create_fact(request.POST.get("artist"),
                           request.POST.get("paint"),
                           request.POST.get("visitor"))
            print("SUCCESS SAVE")
        objects = db.read_all_entities()
        return render(request, "gallery/hello.html", {'facts': objects})
    else:
        objects = db.read_all_entities()
        return render(request, "gallery/hello.html", {'facts': objects})


def showfacts(request):
    if request.method == "GET":
        return render(request, "gallery/showfacts.html", {"facts": db.read_facts()})
    else:
        db.delete_fact(request.POST.get("id", ""))
        return render(request, "gallery/showfacts.html", {"facts": db.read_facts()})


def update(request):
    if request.method == "GET":
        # objects = Object()
        objects = db.read_all_entities()
        objects.entities = db.read_facts()
        return render(request, "gallery/update.html", {"facts": objects})
    else:
        db.update_fact(request.POST.get("id", ""),
                       request.POST.get("artist"),
                       request.POST.get("paint"),
                       request.POST.get("visitor"))
        return render(request, "gallery/showfacts.html", {"facts": db.read_facts()})


def visitors(request):
    objects = Object()
    objects.technique = db.get_technique()
    if request.method == "POST":
        if request.POST.get("text_search", "") == "y":
            objects.search_result = text_search(request)
        if request.POST.get("visitor_search", "") == "search":
            objects.visitors = db.visitor_search(request.POST.get("bool_f"))
        if request.POST.get("paint_search", "") == "technique":
            objects.paints = db.get_tech_entities(request.POST.get("tech_select"))

    return render(request, "gallery/visitors.html", {"objects": objects})


def text_search(request):
    s_type = request.POST.get("text_select")
    word = request.POST.get("words")
    if word != "":
        if s_type == "phrase":
            objects = db.boolean_search("artists", "WHERE MATCH (biography) AGAINST ('\"" + word + "\"' IN BOOLEAN MODE); ")
        elif s_type == "word":
            objects = db.boolean_search("artists", "WHERE NOT MATCH (biography) AGAINST ('+" + word + "' IN BOOLEAN MODE);")
    else:
        objects = db.boolean_search("artists", "")
    return objects