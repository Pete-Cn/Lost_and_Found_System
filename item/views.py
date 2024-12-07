from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime
from pathlib import os
from .models import Item, Campus, Building, Item_type, Building_Type

import csv
# Create your views here.
def search_url(campus_chosen, building_list, type_chosen, status, begindate, key, wordTag):
    return "?" + "campus=" + campus_chosen + "&building=" + building_list + "&type=" + type_chosen + "&status=" + status + "&date=" + begindate + "&key=" + key + "&wordTag=" + wordTag

def item(request):
    if request.method == "POST":
        campus_chosen = request.POST.get('campus_chosen')
        type_chosen = request.POST.get('type_chosen')  
        status = request.POST.get('status')
        begindate = request.POST.get('begin_date')
        building_list = request.POST.getlist('building_chosen')
        key = request.POST.get('key')
        wordTag = request.POST.get('wordTag')
        print(key)
        if begindate == '':
            begindate = datetime(2022, 2, 2).strftime("%Y-%m-%d")

        if key is None:
            key = ''
        
        if status is None:
            status = '0'

        building_list_str = ','.join(building_list)
        url = reverse("items:search") + search_url(campus_chosen, building_list_str, type_chosen, str(status), begindate, key, wordTag)
        return redirect(url)
    else:
        Item_list = Item.objects.all()

        paginator = Paginator(Item_list, 9)

        page = request.GET.get('page')

        try:
            Items = paginator.page(page)
        except PageNotAnInteger:
            Items = paginator.page(1)
        except EmptyPage:
            Items = paginator.page(paginator.num_pages)

        context = {
            "Items": Items,
            #Item.objects.order_by("-found_date")[:5],
            "Campuss": Campus.objects.all,
            "Building_Types": Building_Type.objects.all,
            "Buildings": Building.objects.all,
            "Item_Types": Item_type.objects.all,
            "default_Campus": '',
            "default_Building": '',
            "default_Type": '',
        }
        return render(request, "item.html", context)

@login_required
def detail(request, item_id): 
    current_item = get_object_or_404(Item, pk=item_id)
    if request.method == "POST":
        current_item.status = True
        current_item.owner = request.user.username
        current_item.save()

    return render(request, "detail.html", {"item": current_item})

def search(request):
    
    campus_chosen = request.GET.get('campus')
    building_list_str = request.GET.get('building')
    type_chosen = request.GET.get('type')
    status = request.GET.get('status')
    date = request.GET.get('date')
    key = request.GET.get('key')
    wordTag = request.GET.get('wordTag')

    building_list = building_list_str.split(',')
    building_name_list = ['']

    q = Q() 
    q2 = Q()
    q3 = Q()
    q.connector = "and"
    q2.connector = "or"
    q3.connector = "or"      
    if status == '1':
        q.children.append(('status', False))

    if campus_chosen != '0' :
        q.children.append(('campus_found', int(campus_chosen)))

    if building_list[0] == '0':
        building_name_list.append("全部建筑")
    else:
        for building_chosen in building_list:
            q2.children.append(('building_found', int(building_chosen)))
            building_name_list.append(Building.objects.get(pk=int(building_chosen)).building_name)
    
    if type_chosen != '0':
        q.children.append(('type', int(type_chosen)))     

    begin_date = datetime.strptime(date, "%Y-%m-%d")
    q.children.append(Q(("found_date__gte", begin_date)))

    if key is not None:
        if wordTag == '1':
            q3.children.append(("exact_position__icontains", key))
        elif wordTag == '2':
            q3.children.append(("note__icontains", key))
            q3.children.append(("name__icontains", key))
        else:
            q3.children.append(("note__icontains", key))
            q3.children.append(("name__icontains", key))
            q3.children.append(("exact_position__icontains", key))

    qualified_items = Item.objects.filter((q | q2) & q3)
    
    if qualified_items.exists:
        paginator = Paginator(qualified_items, 9)
        page = request.GET.get('page')

        try:
            Items = paginator.page(page)
        except PageNotAnInteger:
            Items = paginator.page(1)
        except EmptyPage:
            Items = paginator.page(paginator.num_pages)
    else:
        Items = None
    
    context = {
        "Items": Items,
        "Campuss": Campus.objects.all,
        "Buildings": Building.objects.all,
        "Building_Types": Building_Type.objects.all,
        "Item_Types": Item_type.objects.all,
        "status": status,
        "default_Campus": Campus.objects.filter(pk=campus_chosen),
        "default_Building": building_name_list,
        "default_Type": Item_type.objects.filter(pk=type_chosen),
        "default_date": date,
        "default_key": key,
        "default_tag": wordTag,
    }
    return render(request, "item.html", context)
    
@login_required    
def post_page(request):
    if request.method == "POST":
        CP = request.POST.get("current_position")
        img_uploaded = request.FILES.get("newimg")
        print(img_uploaded)

        newitem = Item(
            found_date=datetime.now(), 
            note=request.POST.get("note"), 
            status=False,
            exact_position=request.POST.get("exact_position"),
            current_position=CP,
            type=Item_type.objects.get(pk=request.POST.get("type")),
            campus_found=Campus.objects.get(pk=request.POST.get("campus_found")),
            building_found=Building.objects.get(pk=request.POST.get("building_found")),
            name=request.POST.get("name"),
            founder=request.user.username,
            image=img_uploaded,
        )

        if newitem.building_found.campus != newitem.campus_found:
            return HttpResponse("请选择正确的校区和建筑")
        else:
            try: 
                newitem.save()
                return redirect(reverse("items:item"))
            except:
                return HttpResponse("发布失败")
    else:
        context = {
            "Campuss": Campus.objects.all,
            "Buildings": Building.objects.all,
            "Building_Types": Building_Type.objects.all,
            "Item_Types": Item_type.objects.all,
        }
        return render(request, "post_page.html", context)

def loaddata(request):
    path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data.csv')
    data = []
    with open(path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            data.append(row)
    dict1 = {}
    dict2 = {}
    for i in range(1, 6):
        dict1[str(i)] = Campus.objects.get(pk=i)

    for i in range(1, 7):
        dict2[str(i)] = Building_Type.objects.get(pk=i)   
    for row in data:
        newbuilding = Building(building_name = row[1], campus = dict1[row[0]], type = dict2[row[2]])
        newbuilding.save()
        print(row[0])
    return HttpResponse(data)