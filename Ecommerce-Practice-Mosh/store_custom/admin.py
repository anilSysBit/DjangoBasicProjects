from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from tags.models import TaggedItem
from store.admin import ProductImageInline, ProdutAdmin
from store.models import Product
# Register your models here.



#  Make the Core app specific to all other apps
# to do that make a new app which kepps the realtion between the both apps
# later on if the company has mindset to remove one app there will be no effect on the database


class TagInline(GenericTabularInline):
    autocomplete_fields = ['tag']
    model = TaggedItem
    extra = 1


class CustomProductAdmin(ProdutAdmin):
    inlines = [TagInline,ProductImageInline]


admin.site.unregister(Product)
admin.site.register(Product,CustomProductAdmin)