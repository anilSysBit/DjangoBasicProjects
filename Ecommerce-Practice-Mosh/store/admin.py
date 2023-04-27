from django.contrib import admin,messages
from . import models
from django.db.models import Count
from django.utils.html import format_html,urlencode
from django.urls import reverse
# Register your models here.

class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'

    def lookups(self, request, model_admin):
        return [
            ('<10','Low'),
            ('>80','High')
            # we can add as many items we want
        ]
    def queryset(self, request, queryset):
        if self.value() == '<10':
            return queryset.filter(inventory__lt = 10)
        elif self.value() == '>80':
            return queryset.filter(inventory__gt=80)
            
class ProductImageInline(admin.TabularInline):
    model = models.ProductImage
    extra = 1
    readonly_fields = ['thumbnail']

    def thumbnail(self,instance):
        if instance.image.name != '':
            return format_html(f'<img src="{instance.image.url}" class="thumbnail"/>')
        return ''

# add media class on Your Main Module Where you wanna apply css 
    # class Media:
    #     css = {
    #         'all':['styles.css']
    #     }
    # use different names if you wanna use different stylesheet on different application cause' it gonna overwrite and eager data will not applied

@admin.register(models.Product)
class ProdutAdmin(admin.ModelAdmin):
    autocomplete_fields = ['collection']
    prepopulated_fields = {
        'slug':['title']
    }
    inlines = [ProductImageInline]
    list_display = ['title','unit_price','collection_title','inventory_status']
    list_editable = ['unit_price']
    list_filter = ['collection','last_update',InventoryFilter]
    list_per_page = 10
    list_select_related = ['collection']
    search_fields = ['title']


    @admin.display(ordering='inventory')
    def inventory_status(self,product):
        if product.inventory < 10:
            return 'Low'
        return '0K'
    
    def collection_title(self,product):
        return product.collection.title
    

    actions = ['clear_inventory']
    @admin.action(description='Clear inventory')
    def clear_inventory(self,request,queryset):
        updated_count = queryset.update(inventory = 0)
        self.message_user(
            request,
            f'{updated_count} products were sucessfully updated',
            messages.ERROR #type of message
        )

    class Media:
        css = {
            'all':['styles.css']
        }


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin): 
    list_display = ['first_name','last_name','membership']
    list_editable = ['membership']  
    list_per_page = 10
    list_select_related = ['user']
    ordering = ['user__first_name','user__last_name']
    search_fields = ['first_name__istartswith','last_name__istartswith']


class OrderItemInline(admin.TabularInline):
    autocomplete_fields = ['product']
    model = models.OrderItem
    min_num = 1 #at least one OrderItem requred
    max_num = 10 #at most 10 OrderItem 
    extra = 0 #don't give extra inlines of 

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    autocomplete_fields = ['customer']
    inlines = [OrderItemInline]
    exclude = ['placed_at']
    list_display = ['id','placed_at','customer']

@admin.register(models.OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order','product','quantity']

@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin  ):
    list_display = ['title','products_count']
    search_fields = ['title']
    @admin.display(ordering='products_count')
    def products_count(self,collection):
        # adding urls to the list
        url = (
            reverse('admin:store_product_changelist') #'admin:app_model_page
            + '?'
            + urlencode({
                'collection__id':str(collection.id)
            }) 
        )
        return format_html('<a href="{}">{}</a>',url,collection.products_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            products_count = Count('products')
        )


class CartItemInline(admin.TabularInline):
    model = models.CartItem
    min = 1

@admin.register(models.Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id','created_at']
    inlines = [CartItemInline]


@admin.register(models.CartItem)
class CartAdmin(admin.ModelAdmin):
    list_display = ['cart','product','quantity']
    list_editable = ['quantity']