from django.contrib import admin
from .models import *

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Vendor)
admin.site.register(Metal)
admin.site.register(Color)
admin.site.register(Size)