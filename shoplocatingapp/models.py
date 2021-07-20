from django.db import models  
class Shopdata(models.Model):  
    sid = models.AutoField(primary_key=True)
    shopname = models.CharField(max_length=200) 
    shopimage  = models.CharField(max_length=50) 
    shopdesc = models.CharField(max_length=300)
    shopcontact = models.CharField(max_length=100) 
    shopemail = models.CharField(max_length=50) 
    shopaddress = models.CharField(max_length=400) 
    shoparea = models.CharField(max_length=50) 
    shopcity = models.CharField(max_length=50)
    shopdistrict = models.CharField(max_length=50)
    shopstate = models.CharField(max_length=50)
    holiday = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    class Meta:  
        db_table = "shopdata"  

class Area(models.Model):  
    id = models.AutoField(primary_key=True)
    state = models.CharField(max_length=50) 
    district  = models.CharField(max_length=50)    
    city = models.CharField(max_length=50)
    area = models.CharField(max_length=100) 
   
    class Meta:  
        db_table = "area"  
        
class Item(models.Model):  
    id = models.AutoField(primary_key=True)
    shopid = models.IntegerField(default=0) 
    itemname = models.CharField(max_length=50) 
    itemcategory  = models.CharField(max_length=50) 
   
    class Meta:  
        db_table = "item"  