from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

'''
def search(request):
	key = "polls"
	items = ['bengaluru traffic problem', 'vijag city development',
	 'delhi polution and development' ,'election treds in punjab' ,
	 'latest on goa polls']

	matched = ["<li><a>"+item+"</a></li>" for item in items if key in item]

	html = "<ul>"+str("").join(matched)+"</ul>"
	##
	## debug 
	print(html)

	return HttpResponse(html)
'''

@csrf_exempt
def search(request):
	key = "polls"
	items = {'status':200, 'data': ['bengaluru traffic problem',
			'vijag city development',
			'delhi pollution',
			'election treds in punjab',
			'latest on goa polls']}

	##
	## debug
	print(items)

	return JsonResponse(items)