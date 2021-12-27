from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User,on_delete =models.CASCADE)
    full_name = models.CharField(max_length= 100)
    address = models.CharField(max_length=100, null= True ,blank= True)
    joined_on = models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return self.full_name

class Category(models.Model):
    title = models.CharField(max_length = 100)
    slug = models.SlugField(unique = True)

    def __str__(self):
        return self.title

class Product(models.Model):
    title = models.CharField(max_length= 100)
    slug = models.SlugField(unique= True)
    category = models.ForeignKey(Category, on_delete = models.CASCADE)
    image = models.ImageField(upload_to = 'products')
    marked_price = models.PositiveIntegerField()
    selling_price = models.PositiveIntegerField()
    description = models.TextField()

    def __str__(self):
        return self.title

class Cart(models.Model):
    customer = models.ForeignKey(Customer,on_delete = models.SET_NULL, null = True, blank = True)
    total = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return 'Cart:'+ str(self.id)

class CartProduct(models.Model):
    cart = models.ForeignKey(Cart,on_delete = models.CASCADE)
    product = models.ForeignKey(Product,on_delete = models.CASCADE)
    rate = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    subtotal = models.PositiveIntegerField()

    def __str__(self):
        return 'Cart:' + str(self.cart.id) + 'CartProduct'+ str(self.id)

ORDER_STATUS = (
    ('order received','order received'),
    ('order processing','order processing'),
    ('order completed','order completed'),
    ('order on the way','order on the way'),
    ('order cancelled','order cancelled'),
)
class Order(models.Model):
    cart = models.OneToOneField(Cart,on_delete = models.CASCADE)
    ordered_by = models.CharField(max_length= 100)
    shipping_address = models.CharField(max_length=100)
    contact_no = models.PositiveIntegerField()
    email = models.EmailField(null = True,blank= True)
    subtotal = models.PositiveIntegerField()
    discount = models.PositiveIntegerField()
    total = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add= True)
    order_status = models.CharField( max_length = 50,choices = ORDER_STATUS)

    def __str__self():
        return 'Order:' + str(self.id)


