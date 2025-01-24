from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from .models import notice

import markdown
# Create your views here.

@login_required
def report_page(request):
    if request.method == 'POST':
        return HttpResponse("ad")
    
    return render(request, "report_page.html")

def index(request):
    all_notice = notice.objects.all()
    Notice_list = []
    for notice_detail in all_notice:
        notice_detail.content = markdown.markdown(
        notice_detail.content,
        extensions = [
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
            'markdown.extensions.abbr',
            'markdown.extensions.attr_list',
            'markdown.extensions.def_list',
            'markdown.extensions.fenced_code',
            'markdown.extensions.footnotes',
            'markdown.extensions.md_in_html',
            'markdown.extensions.tables',
            'markdown.extensions.admonition',
            'markdown.extensions.legacy_attrs',
            'markdown.extensions.legacy_em',
            'markdown.extensions.meta',
            'markdown.extensions.nl2br',
            'markdown.extensions.sane_lists',
            'markdown.extensions.smarty',
            'markdown.extensions.toc',
            'markdown.extensions.wikilinks'
            ]
        )
        Notice_list.append({'title': notice_detail.title,'detail': notice_detail})
    for i in Notice_list:
        print(i['title'])
    return render(request, "index.html", context={'Notice': Notice_list})