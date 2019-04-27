from django.db import models

# Create your models here.
class Lvl1Category(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name


class Lvl2Category(models.Model):
    name = models.CharField(max_length=40)
    lvl1category = models.ForeignKey('Lvl1Category',on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=40)
    brand = models.CharField(max_length=40)
    color = models.CharField(max_length=30,blank=True)
    lvl2category =  models.ForeignKey('Lvl2Category',on_delete=models.CASCADE)
    price = models.DecimalField(decimal_places=2,max_digits=7)
    description= models.TextField(blank=True)
    image = models.ImageField(default='static/empty.jpg')
    def __str__(self):
        return self.name


class Order(models.Model):
    products = models.ManyToManyField(Product,through = 'OrderDetail')
    totalprice = models.DecimalField(decimal_places=2,max_digits=7)
    creationtime = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey('Customer',on_delete=models.CASCADE)
    def __str__(self):
        return self.customer.name+ ' purchased at '+str(self.creationtime)

    @property
    def subtotal(self):
        return sum([item.product_total for item in self.orderdetail_set.all()])

class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)


    @property
    def product_total(self):
        return self.product.price*self.quantity
    # def get_product_price(self):
    #     return self.product.price

SEX_CHOICES = (
    ('1','male'),
    ('2','female'),
    ('3','unknown')
)
class Customer(models.Model):
    name = models.CharField(max_length=40)
    sex = models.CharField(max_length=40,choices=SEX_CHOICES)
    tel = models.CharField(max_length=11)
    location = models.CharField(max_length=50)

    def __str__(self):
        return self.name