from django.contrib import admin
from nurseryapp.models import Contact,Product,User
admin.site.register(Contact)
admin.site.register(Product)
class UserAdmin(admin.ModelAdmin):
     list_display=('name','email','password','role')
admin.site.register(User,UserAdmin)  


# Register your models here.
