from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from main.models import users
from django.utils.datastructures import MultiValueDictKeyError
import json

'''
GET parameters
- page (pagination)
- limit (default 5)
- name (case sensitive name searching in first name and last name)
- sort (sort by the given parameter, ascending by default, descending if '-' is prepended)
'''
@csrf_exempt
def index(request, methods = ["GET","POST"]):
	if request.method == "GET":
		'''
		Returns a list of users based on the get parameters	as discussed above
		'''
		try:
			page = int(request.GET["page"])
		except MultiValueDictKeyError:
			page = 1
		except ValueError:
			return JsonResponse({"error":'Invalid value for "page"'},status = 400)
		try:
			limit = int(request.GET["limit"])
		except MultiValueDictKeyError: 
			limit = 5
		except ValueError:
			return JsonResponse({"error":'Invalid value for "limit"'},status = 400)
		try:
			name = request.GET["name"]
		except MultiValueDictKeyError:
			name = None
		try:
			sort = request.GET["sort"]
		except MultiValueDictKeyError:
			sort = None
		if name != None:
			fn = users.objects.raw(f'select * from main_users where lower(first_name) glob lower("*{name}*") or lower(last_name) glob lower("*{name}*")')
		else:
			fn = users.objects.all()
		if sort != None:
			if sort[0] == '-':
				sort = sort[1:]
				reverse = True
			else:
				reverse = False
		final=[]
		for i in fn:
			i.__dict__.pop('_state')
			final.append(i.__dict__)
		try:
			final = final[(page-1)*limit:page*limit]
		except IndexError:
			return JsonResponse([],safe = False)
		if sort	!= None and sort not in users.objects.get(id=1).__dict__.keys:
			return JsonResponse({'error':'Given sorting parameter does not exist'})
		if sort	!= None:
			final = sorted(final, key = lambda ff:ff[sort],reverse = reverse)
		return JsonResponse(final, safe = False)
	elif request.method == "POST":
		'''
		Adds new user to the database, returns 201 {}
		'''
		data = json.loads(request.body)
		if "first_name" not in data.keys():
			return JsonResponse({'error':'"first_name" parameter required'},status=400)
		if "last_name" not in data.keys():
			return JsonResponse({'error':'"last_name" parameter required'},status=400)
		if "company_name" not in data.keys():
			return JsonResponse({'error':'"company_name" parameter required'},status=400)
		if "city" not in data.keys():
			return JsonResponse({'error':'"city" parameter required'},status=400)
		if "state" not in data.keys():
			return JsonResponse({'error':'"state" parameter required'},status=400)
		if "zip" not in data.keys():
			return JsonResponse({'error':'"zip" parameter required'},status=400)
		if "email" not in data.keys():
			return JsonResponse({'error':'"email" parameter required'},status=400)
		if "web" not in data.keys():
			return JsonResponse({'error':'"web" parameter required'},status=400)
		if "age" not in data.keys():
			return JsonResponse({'error':'"age" parameter required'},status=400)
		u = users(**data)
		u.save()
		return JsonResponse({},status=201)

@csrf_exempt
def specific(request,id, methods = ["DELETE","PUT","GET"]):
	try:
		u = users.objects.filter(id=id)[0]
	except IndexError:
		return JsonResponse({},status=404)
	if request.method == "GET":
		'''
		returns all details of the specific user
		'''
		u.__dict__.pop('_state')
		return JsonResponse(u.__dict__)
	elif request.method == "PUT":
		'''
		Change details of the specified user
		'''
		data = json.loads(request.body)
		for i in data.keys():
			setattr(u,i,data[i])
		u.save()
		return JsonResponse({}, status = 200)			
	elif request.method == "DELETE":
		'''
		Delete the specified user
		'''
		u.delete()
		return JsonResponse({}, status = 200)

def add_data(request):
	data = json.load(open('users.json','r'))
	for i in data:
		u = users(**i)
		u.save()
	return JsonResponse({"saved":True}, safe = False)



