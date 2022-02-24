from django.db import models

# Create your models here.

class users(models.Model):
	id = models.AutoField(primary_key=True)
	first_name = models.CharField(max_length = 50)
	last_name = models.CharField(max_length = 50)
	company_name = models.CharField(max_length = 100)
	city = models.CharField(max_length = 50)
	state = models.CharField(max_length = 50)
	zip = models.IntegerField()
	email = models.EmailField(max_length = 50)
	web = models.CharField(max_length = 200)
	age = models.IntegerField()
