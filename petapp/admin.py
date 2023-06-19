from __future__ import unicode_literals

from django.contrib import admin
from .models import  *
# Register your models here.
admin.site.register(Profile)
admin.site.register(Photo)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
admin.site.register(DoctorVent)
admin.site.register(session)
admin.site.register(Vent_Photo)
admin.site.register(Bookedsession)
