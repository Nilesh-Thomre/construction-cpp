from django.db import models
from django.contrib.auth.models import User
category_choice = (
    ('Tools and Equipment', 'Tools and Equipment'),
    ('Safety Gear', 'Safety Gear'),
    ('Materials', 'Materials'),
    ('Site Supplies','Site Supplies'),
    ('Machinery Maintenance and Fuel','Machinery Maintenance and Fuel'),
    ('Office Supplies','Office Supplies'),

)



class Stock(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	category = models.CharField(max_length=50, blank=False, null=True,choices=category_choice)
	item_name = models.CharField(max_length=50, blank=False, null=True)
	quantity = models.IntegerField(default='0', blank=False, null=True)
	receive_quantity = models.IntegerField(default='0', blank=True, null=True)
	receive_by = models.CharField(max_length=50, blank=True, null=True)
	issue_quantity = models.IntegerField(default='0', blank=True, null=True)
	issue_by = models.CharField(max_length=50, blank=True, null=True)
	issue_to = models.CharField(max_length=50, blank=True, null=True)
	phone_number = models.CharField(max_length=50, blank=True, null=True)
	created_by = models.CharField(max_length=50, blank=True, null=True)
	reorder_level = models.IntegerField(default='0', blank=True, null=True)
	last_updated = models.DateTimeField(auto_now_add=False, auto_now=True)
	time_stamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	#date = models.DateTimeField(auto_now_add=False, auto_now=False)
	export_to_CSV = models.BooleanField(default=False)

	def __str__(self):
		return self.item_name + " " + str(self.quantity)

