from django.db import models
from django.contrib.auth.models import User


from django.utils.text import slugify
# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User , null=True, blank=True, on_delete=models.CASCADE)
    email = models.EmailField(null=True , blank=True)
    business_name = models.TextField(max_length=30, null=True , blank=True)
    about = models.TextField(null=True , blank=True)
    address = models.TextField(null=True,blank=True)
    phone = models.TextField(max_length=11,null=True , blank=True)
    business_phone = models.TextField(max_length=11 , null=True , blank=True)
    device = models.CharField(null=True , blank= True , max_length=200)
    def __str__(self):
        if self.user:
            return self.user.username
        else:
            return self.device
    
class Product(models.Model):
    x = [
        ('Food','Food') , ('Clothes','Clothes'),
        ('accessories','accessories') , ('Medicine','Medicine'),
        ('Toys','Toys') , ('Cages','Cages') , ('none','none')
    ]
    pet = [
        ('Cat','Cat') , ('Dog','Dog'),
        ('Bird','Bird') , ('Fish','Fish')
    ]
    user=models.ForeignKey(User , null=True, blank=True,on_delete=models.CASCADE)
    product_name = models.TextField(max_length=50)
    product_shot_des = models.TextField(max_length=100)
    product_description = models.TextField(max_length=2000)
    product_price = models.FloatField()
    product_discount_price = models.FloatField(null=True , blank=True)
    product_img = models.FileField(null=False, blank=False)
    product_sell_price = models.FloatField()
    product_stock = models.IntegerField()
    product_type = models.TextField(choices=pet)
    product_Catecory = models.TextField(choices = x)
    discount = models.BooleanField(default=False)
    slug = models.SlugField(max_length=100)
    
    def __str__(self):
        return self.product_name
        
        
class Photo(models.Model):
    class Meta:
        verbose_name = 'Photo'
        verbose_name_plural = 'Photos'
    
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, null=True, blank=True)
    product_img = models.FileField(null=False, blank=False)

    def __str__(self):
        return self.product.product_name
    

class Order(models.Model):
	customer = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
	date_ordered = models.DateTimeField(auto_now_add=True)
	complete = models.BooleanField(default=False)
	transaction_id = models.CharField(max_length=100, null=True)

	def __str__(self):
		return str(self.id)
		
	@property
	def shipping(self):
		shipping = False
		orderitems = self.orderitem_set.all()
		for i in orderitems:
			if i.product.product_stock == 0 or i.product.product_stock == '0':
				shipping = True
		return shipping

	@property
	def get_cart_total(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.get_total for item in orderitems])
		return total 

	@property
	def get_cart_items(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.quantity for item in orderitems])
		return total 

class OrderItem(models.Model):
	product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	quantity = models.IntegerField(default=0, null=True, blank=True)
	date_added = models.DateTimeField(auto_now_add=True)

	@property
	def get_total(self):
		total = self.product.product_price * self.quantity
		return total

class ShippingAddress(models.Model):
	customer = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	address = models.CharField(max_length=200, null=False)
	city = models.CharField(max_length=200, null=False)
	state = models.CharField(max_length=200, null=False)
	zipcode = models.CharField(max_length=200, null=False)
	date_added = models.DateTimeField(auto_now_add=True)


class DoctorVent(models.Model):
    user = models.OneToOneField( User , on_delete=models.CASCADE)
    name = models.CharField(null = True , blank=True , max_length=30)
    email = models.EmailField(null=True , blank=True)
    phone = models.TextField(max_length=11,null=True , blank=True)
    vent_phone = models.TextField(max_length=11 , null=True , blank=True)
    address = models.TextField(blank=True , null=True)
    profile_pic = models.ImageField()
    about = models.TextField(null=True , blank=True)
    slug = models.SlugField(max_length=100 )
    # Generate the slug from the name field
    def save(self, *args, **kwargs):
        # slugname=self.name +str(random.randint(0,9))
        self.slug = slugify(self.slug)
        super().save(*args, **kwargs)
    def __str__(self):
        return self.user.username
    
class Vent_Photo(models.Model):
    DoctorVent = models.ForeignKey(
        DoctorVent, on_delete=models.CASCADE, null=True, blank=True)
    vent_img = models.FileField(null=False, blank=False)

    def __str__(self):
        return self.DoctorVent.name
    

class session(models.Model):
    doctor = models.ForeignKey(DoctorVent , on_delete=models.SET_NULL , null=True)
    startsession = models.DateTimeField(auto_now=False)
    endsession = models.DateTimeField(auto_now=False)
    duration = models.PositiveIntegerField(null=True , blank=True)

    def __str__(self):
        return str(self.doctor.email)

class Bookedsession(models.Model):
    patient = models.ForeignKey(Profile , on_delete=models.CASCADE)
    doctor = models.ForeignKey(DoctorVent ,on_delete=models.CASCADE)
    sessionData = models.DateTimeField(auto_now=False)