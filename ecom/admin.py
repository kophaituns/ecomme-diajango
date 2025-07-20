from django.contrib import admin
from .models import Customer, Product, Orders, Feedback, ChatMessage
# Register your models here.
class CustomerAdmin(admin.ModelAdmin):
    pass
admin.site.register(Customer, CustomerAdmin)

class ProductAdmin(admin.ModelAdmin):
    pass
admin.site.register(Product, ProductAdmin)

class OrderAdmin(admin.ModelAdmin):
    pass
admin.site.register(Orders, OrderAdmin)

class FeedbackAdmin(admin.ModelAdmin):
    pass
admin.site.register(Feedback, FeedbackAdmin)

class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['customer', 'message', 'timestamp', 'is_read']
    list_filter = ['is_read', 'timestamp']
    search_fields = ['message', 'response']
admin.site.register(ChatMessage, ChatMessageAdmin)
# Register your models here.
