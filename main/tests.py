from django.test import TestCase, Client
from main.models import users
import json

class testing(TestCase):
	all_data = json.load(open('users.json'))
	custom_user = {"first_name": "new", "last_name": "user", "company_name": "testing, testing sq", "city": "testers", "state": "TE", "zip": 1337, "email": "tester@example.com", "web": "http://www.example.com", "age": 69}
	custom_user1 = {"first_name": "new2", "last_name": "user2", "company_name": "testing, testing sq", "city": "testers", "state": "TE", "zip": 1337, "email": "tester@example.com", "web": "http://www.example.com", "age": 69}
	def setUp(self):
		for i in json.load(open('users.json')):
			users.objects.create(**i)
		users.objects.create(**self.custom_user)

	def test_get_list(self):
		'''
		Get the paginated list of all users
		'''
		c = Client()
		r1 = c.get('/api/users/').json()
		self.assertEqual(r1,self.all_data[:5])
	def test_page(self):
		'''
		Get the second page
		'''
		c = Client()
		r2 = c.get('/api/users/?page=2').json()
		self.assertEqual(r2,self.all_data[5:10])
	def test_limit(self):
		'''
		Change the number of items per page using custom input
		'''
		c = Client()
		r3 = c.get('/api/users/?page=2&limit=4').json()
		self.assertEqual(r3,self.all_data[4:8])
	def test_name(self):
		'''
		Case-insensitive search for given string in first_name and last_name
		'''
		c = Client()
		name = 'es'
		searched = []
		for i in self.all_data:
			if name.lower() in i['first_name'].lower() or name.lower() in i['last_name'].lower() :
				searched.append(i)
		r4 = c.get(f'/api/users/?page=1&limit=4&name={name}').json()
		self.assertEqual(r4,searched[:4])
	def test_sort(self):
		'''
		Sort according to the given parameter
		'''
		c = Client()
		sort = 'age'
		searched = sorted(self.all_data[:4],key = lambda ss:ss[sort])
		r5 = c.get(f'/api/users/?page=1&limit=4&sort='+sort).json()
		self.assertEqual(r5,searched)
	def test_sort_reverse(self):
		'''
		Reverse sorting
		'''
		c = Client()
		sort = '-age'
		searched = sorted(self.all_data[:4],key = lambda ss:ss['age'], reverse = True)
		r6 = c.get(f'/api/users/?page=1&limit=4&sort='+sort).json()
		self.assertEqual(r6,searched)

	def test_create(self):
		'''
		Create a new user
		'''
		c = Client()
		data = self.custom_user1
		self.assertEqual(c.post('/api/users/',json.dumps(data),content_type="application/json").json(),{})
		r7 = c.get('/api/users/?limit=505').json()[-1]
		r7.pop('id')
		self.assertEqual(self.custom_user1,r7)

	def test_fetch(self):
		'''
		Fetch one user
		'''
		c = Client()
		r8 = c.get('/api/users/501').json()
		r8.pop('id')
		self.assertEqual(r8,self.custom_user)

	def test_edit(self):
		'''
		Edit an existing user
		''' 
		c = Client()
		url = '/api/users/501'
		r9b = c.get(url).json()
		self.assertEqual(c.put(url,data={"first_name":"changed"}, content_type="application/json").json(),{})
		r9a = c.get(url).json()
		r9b["first_name"] = "changed"
		self.assertTrue(r9a,r9b)

	def test_delete(self):
		'''
		Delete a user
		'''
		c = Client()
		url = '/api/users/501'
		r10b = c.get(url).status_code
		self.assertEqual(r10b,200)
		c.delete(url)
		r10a = c.get(url).status_code
		self.assertEqual(r10a,404)

