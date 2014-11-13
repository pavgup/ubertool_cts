from django.conf import settings # This urls.py file is looking for the ChemAxon_PROXY_URL variable in the project settings.py file.
from django.shortcuts import render
from django.http import HttpResponse
import urllib2

# TODO: this function is strongly generic, it may be worth considering to use this as a component of the larger ubertool project for CTS/upstream. 
def simple_proxy(request,path):
  ChemAxon_URL = settings.ChemAxon_PROXY_URL + path
  try:
    async_request = urllib2.urlopen(ChemAxon_URL)
    async_data = async_request.read()
  except urllib2.HTTPError as e:
    return HttpResponse(ChemAxon_URL+e.msg, status=e.code, content_type='text/plain')
  else: 
    return HttpResponse(async_data, status=async_request.code, content_type=async_request.headers.typeheader) 
      
def index(request,model):
  return render(request, 'test_cts/index')

def calc_kow(request):
  return render(request, 'calc_kow.html')
