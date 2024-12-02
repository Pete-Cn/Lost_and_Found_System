from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime

from .models import Item, Campus, Building, Item_type

# Create your views here.
def item(request):
    if request.method == "POST":
        campus_chosen = request.POST.get('campus_chosen')
        building_chosen = request.POST.get('building_chosen')
        type_chosen = request.POST.get('type_chosen')  
        status = request.POST.get('status')
        begindate = request.POST.get('begin_date')

        if begindate == '':
            begindate = datetime(2022, 2, 2).strftime("%Y-%m-%d")

        
        if status == None:
            status = 0
        else:
            status = 1
        
        return redirect(reverse("items:search", kwargs={'campus_id': campus_chosen, 'building_id': building_chosen, 'type_id': type_chosen, 'status': status, 'date': str(begindate) }))
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

def search(request, campus_id, building_id, type_id, status, date):
    
    campus_chosen = campus_id
    building_chosen = building_id
    type_chosen = type_id

    q = Q()
    q.connector = "and"      
    if status == 1:
        q.children.append(('status', False))

    if campus_chosen != 0 :
        q.children.append(('campus_found', campus_chosen))

    if building_chosen != 0:
        q.children.append(('building_found', building_chosen))
    
    if type_chosen != 0:
        q.children.append(('type', type_chosen))     


    if date is not None:
        begin_date = datetime.strptime(date, "%Y-%m-%d")
        q.children.append(Q(("found_date__gte", begin_date)))
#       qualified_items = Item.objects.filter(Q(found_date__gte=begin_date) | q) 
#    else:
    qualified_items = Item.objects.filter(q)
    
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
        "Item_Types": Item_type.objects.all,
        "status": bool(status),
        "default_Campus": Campus.objects.filter(pk=campus_chosen),
        "default_Building": Building.objects.filter(pk=building_chosen),
        "default_Type": Item_type.objects.filter(pk=type_chosen),
        "default_date": date,
    }
    return render(request, "item.html", context)
    
@login_required    
def post_page(request):
    if request.method == "POST":
        CP = request.POST.get("current_position")
        img_uploaded = request.FILES.get("newimg")
        name=request.FILES.get('newimg').name
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
            founder=request.user.username,
            image=img_uploaded,
        )
        print(newitem)
        print(CP)

        try: 
            newitem.save()
            return redirect(reverse("items:item"))
        except:
            return HttpResponse("发布失败")
    else:
        context = {
            "Campuss": Campus.objects.all,
            "Buildings": Building.objects.all,
            "Item_Types": Item_type.objects.all,
        }
        return render(request, "post_page.html", context)
