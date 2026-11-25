from django.contrib import admin

from .models import Order, OrderItem, Payment, DeliveryBoy, Rider


class OrderItemInline(admin.TabularInline):

    model = OrderItem
    extra = 0


@admin.register(Order) 

class OrderAdmin(admin.ModelAdmin): 
    list_display = ( 
        "id", 
        "customer_name", 
        "total_price", 
        "status", 
        "created_at" 
    ) 
    list_filter = ( 
        "status", 
    ) 
    search_fields = ( 
        "customer_name", 
    )

admin.site.register(DeliveryBoy)

admin.site.register(Rider)