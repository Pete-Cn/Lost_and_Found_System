from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime

from .models import Report
# Create your views here.

@login_required
def report_page(request):
    if request.method == 'POST':
        return HttpResponse("ad")
    
    return render(request, "report_page.html")