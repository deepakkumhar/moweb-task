from django.db import models

# Create your models here.

class Category(models.Model):
    title=models.CharField(max_length=50,null=False)
    order=models.IntegerField(null=True,blank=True)
    subcategory=models.ForeignKey('self',on_delete=models.CASCADE,related_name='subcategories',null=True,blank=True)

class Product(models.Model):
    name=models.CharField(max_length=50,null=False)
    price=models.FloatField(null=False)
    category=models.ManyToManyField(Category,related_name='product')