from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.
#id(integer), firstname, lastname, created_at(timestamp), password_hash, email(varchar)

"""
The table Vendors that store the information about the Vendors who are the users of the app.
"""
class Vendors(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} has the email {self.user.email}, and was created at {self.created_at}"

"""
The Table Menu that represents a menu that has been created by a Vendor
"""
class Menu(models.Model):
    vendor_id = models.ForeignKey(Vendors, on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    menu_name = models.CharField(max_length=255)
    menu_url = models.CharField(max_length=255)
    image_field = models.ImageField(upload_to='images/')

    def __str__(self):
        return f"{self.vendor_id.user.username} created the menu {self.menu_name} at {self.created_at}"

"""
The Table Category that represents a category within a menu
"""
class Category(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    category_name = models.CharField(max_length=255)
    category_url = models.CharField(max_length=255)
    category_image = models.ImageField(upload_to='images/')
    menu_id = models.ForeignKey(Menu, on_delete = models.CASCADE)

    def __str__(self):
        return f"{self.category_name} belongs to the menu {self.menu_id.menu_name}"

"""
The Table Item that represents an item within a category that is further a menu
"""
class Item(models.Model):
    item_name = models.CharField(max_length=255)
    pricing = models.FloatField()
    item_image = models.ImageField(upload_to='images/')
    description = models.TextField()

    def __str__(self):
        return f"{self.description}"

"""
The Table Category_Item that represents the categories and items that have a many-to-many relationship
with each other.
"""
class Category_Item(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.category.category_name} - {self.item.item_name}"

"""
The Table Table that represents a table where the customer is seated and places an order.
"""
class Tables(models.Model):
    table_number = models.IntegerField()
    qr_code_url = models.URLField(max_length=255)
    menu_id = models.ForeignKey(Menu, on_delete = models.CASCADE)

    def __str__(self):
        return f"{self.table_number} has the menu {self.menu_id.menu_name}"

"""
The Table Cart that represents a Cart that has the items.
"""
class Cart(models.Model):
    table_id = models.ForeignKey(Tables, on_delete = models.CASCADE )
    session_key = models.CharField(max_length=40, null=True, blank=True) 
    is_active = models.BooleanField(default=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"The cart was created at {self.created_at} and has the following notes that needs to be taken into account {self.notes}"

"""
The Table Cart_Item that represents a many-to-many relationship with each other.
"""
class Cart_Item(models.Model):
    cart_id = models.ForeignKey(Cart, on_delete = models.CASCADE)
    item_id = models.ForeignKey(Item, on_delete = models.CASCADE)
    quantity = models.IntegerField()

"""
The Table Orders that represents the order that has placed by a customer seated at a table
"""
class Orders(models.Model):
    cart_id = models.OneToOneField(Cart, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=255)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=20)
    total_price = models.IntegerField()
    order_status = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer_name} submitted the order at {self.created_at} and made the payment of {self.total_price}"

"""
The subscription of the Software as a Service
"""
class Subscription(models.Model):
    vendor = models.OneToOneField(Vendors, on_delete=models.CASCADE, related_name='subscription')
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)
    is_archived = models.BooleanField(default=False)  # False = user is subscribed

    def __str__(self):
        return f"{self.vendor.user.username} - {'Subscribed' if not self.is_archived else 'Unsubscribed'}"

