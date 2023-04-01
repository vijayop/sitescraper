from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from .models import Link
from django.http import HttpResponseRedirect

# Create your views here.

def scrape(request):
    if request.method == "POST":
        site = request.POST.get('site','') # site is the id of input field in form , so get the entered website here in the site variable 
        page = requests.get(site) # This will take the whole html page data from the mentioned link
        soup = BeautifulSoup(page.text,'html.parser') # This will convert the page data into text and then parse it as html page ,soup object will have the whole html coded page

        for link in soup.find_all('a'):  # find all the lines containing <a> tag
            link_address = link.get('href') # this will collect only the link mentioned in href tag 
            link_text = link.string # this will get the name of the link 
            Link.objects.create(address = link_address,name = link_text)   # making and object of link model calss and saving all the data in it 
        return HttpResponseRedirect('/')    
    else:
        data = Link.objects.all()
    
    return render(request,'myapp/result.html',{'data':data})

def delete(request):
    Link.objects.all().delete()
    return render(request,'myapp/result.html')