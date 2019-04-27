from django.contrib import admin
from .models import Lvl1Category,Lvl2Category,Product,OrderDetail,Customer,Order
# Register your models here.
# admin.site.register(Lvl1Category)
class Lvl2CategoryInline(admin.TabularInline):
    model = Lvl2Category


@admin.register(Lvl1Category)
class Lvl1CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    inlines = [
        Lvl2CategoryInline,
    ]

admin.site.register(Lvl2Category)



@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display=  ('name','brand','color','lvl2category', 'price','description')

# @admin.register(OrderDetail)
# class OrderProductAdmin(admin.ModelAdmin):
#     list_display=  ('order','product','quantity')

class OrderDetailInline(admin.TabularInline):
    model = OrderDetail
    readonly_fields = ['get_product_price','get_total_price']

    # fields= ['product','quantity','get_product_price']
    fields= ['product','quantity','get_product_price','get_total_price']

    def get_product_price(self,obj):
        return obj.product.price

    def get_total_price(self,obj):
        return obj.product_total


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display=  ('customer','totalprice','creationtime','subtotal')
    fields = ('customer','totalprice','creationtime','subtotal')
    readonly_fields = ['subtotal','creationtime']
    inlines = [
        OrderDetailInline,
    ]
    def get_product_price(self,obj):
        return obj.product.price

    def get_total_price(self,obj):
        return obj.product.price*obj.quantity

    def subtotal(self,obj):
        return sum([item.product_total for item in obj.orderdetail_set.all()])


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display =  ('name','sex','tel','location')