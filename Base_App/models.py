from django.db import models
from django.contrib.auth.models import User

# CATEGORY MODEL
class ItemList(models.Model):
    Category_name = models.CharField(max_length=50)

    def __str__(self):
        return self.Category_name

# DEFAULT CATEGORY FUNCTION FOR MIGRATIONS AND EMPTY CASES
def get_default_category():
    return ItemList.objects.get_or_create(Category_name='')[0].id

# ITEM MODEL
class Items(models.Model):
    Item_name = models.CharField(max_length=40)
    description = models.TextField(blank=False)
    Category = models.ForeignKey(ItemList, related_name='items', on_delete=models.CASCADE, default=get_default_category)
    Price = models.DecimalField(max_digits=10, decimal_places=2)
    Image = models.ImageField(upload_to='items/')

    def __str__(self):
        return self.Item_name

# ABOUT US SECTION
class AboutUs(models.Model):
    Description = models.TextField()

class Delivery(models.Model):
    name = models.CharField(max_length=255, default='Unknown')
    address = models.TextField(default='default address')
    payment_method = models.CharField(
        max_length=50,
        choices=[('Cash on Delivery', 'Cash on Delivery'), ('GCash', 'GCash')],
        default='Cash on Delivery'
    )
    items = models.TextField(null=True, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2) 
   

    def __str__(self):
        return f"Order by {self.name} - {self.payment_method}"


# CART
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

# CART ITEMS
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    item = models.ForeignKey(Items, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # SET DEFAULT TO A VALID DECIMAL VALUE LIKE 0.00

class Order(models.Model):
    customer_name = models.CharField(max_length=255)
    address = models.CharField(max_length=500)
    items = models.TextField()  # Assuming items are stored as a string, or you could use a foreign key to another model
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order {self.id} by {self.customer_name}"