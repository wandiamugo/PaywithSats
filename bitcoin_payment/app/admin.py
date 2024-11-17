from django.contrib import admin
# from models import User, ServiceProvider, Service, Payment
from .models import User, Service, ServiceProvider,Payment
# Register your models here.

admin.site.register(User)
admin.site.register(ServiceProvider)
admin.site.register(Service)
admin.site.register(Payment)