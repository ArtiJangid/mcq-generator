import csv
import json

from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import (
    ListView,
)
from .models import Post
# Create your views here.

def home(request):
    context = {
        'posts':Post.objects.all()
    }
    return render(request,'qgen/home.html',context)

class PostListView(ListView):
    model = Post
    template_name = 'qgen/home.html' #<app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']

from .autosearch import autosearch
from .OurMcqGen import excecute
def mcqview(request):
    context = dict()
    if request.method == "POST":
        if "mcq_content_form" in request.POST:
            compression_ratio = int(request.POST.get("compression_ratio"))/100
            print("compression_ratio: ",compression_ratio)
            str = request.POST.get("full_text")
            print("Text:", str)
            mcqs = excecute(str,compression_ratio)
            print("MCQs: ", mcqs)
            context = {'mcqs':mcqs}
            context['full_text'] = str
            return render(request,'qgen/Mcq_Steps.html',context)
        elif "mcq_search_bar_form" in request.POST:
            str = request.POST.get("search_bar")
            result = autosearch(str)
            searched = {'result':result}
            return render(request,'qgen/Mcq_Steps.html',searched)
        elif "download" in request.POST:
            mcqs_str = request.POST.get('mcqs')
            return download_mcqs(request, mcqs_str)
    else:
        return render(request,'qgen/Mcq_Steps.html')

def summaryview(request):
    if request.method == "POST":
        if "mcq_content_form" in request.POST:
            compression_ratio = int(request.POST.get("compression_ratio"))/100
            print("compression_ratio: ",compression_ratio)
            str = request.POST.get("full_text")
            summary = excecute(str,compression_ratio,True)
            context = {'summary':summary}
            return render(request,'qgen/Summary.html',context)
        elif "mcq_search_bar_form" in request.POST:
            str = request.POST.get("search_bar")
            result = autosearch(str)
            searched = {'result':result}
            return render(request,'qgen/Summary.html',searched)
    else:
        return  render(request,'qgen/Summary.html')


def download_mcqs(request, mcqs_str):
    # Create the HttpResponse object with the appropriate CSV header.
    if mcqs_str:
        response = HttpResponse(content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename="mcqs.txt"'
        response.write(mcqs_str)
        return response
    else:
        return HttpResponse("No MCQs to download.", content_type='text/plain')
