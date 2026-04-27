from django.contrib import admin

from .models import ProductImages,Product,Category,Cart
# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    model = Category
    list_display=('category_name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    model = Product
    # что показываем в списке товаров
    list_display=('title','category_id','stock_units','price',)
    # По каким полям на можно кликнуть , чтобы перейти в редактированию
    list_display_links = ('title',)
    # Поля , которые можно редактировать ПРЯМО В СПИСКЕ
    list_editable = ('price','stock_units',)
    # Боковые фильтры
    list_filter = ('category_id',)
    # Поиск по тексту
    search_fields = ('title',)
    # Групировка полей внутри карточки товара при создании товара
    fieldsets = (
        ('Основная информация',{
            'fields':('title','category_id')
        }),
         ('Ценообразование и склад',{
            'fields':('price','stock_units','discount'),
            'classes':('collapse',) # Эту секцию можно сворачивать
        }),
         ('Продавец и описание',{
            'fields':('description','seller_id'),
            'classes':('collapse',) # Эту секцию можно сворачивать
        })
    )
    
@admin.register(ProductImages)
class ProductImagesAdmin(admin.ModelAdmin):
    model = ProductImages
    list_display=('product_id','is_main')
    search_fields = ('product_id',)
    list_editable = ('is_main',)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    model = Cart
    list_display=('user_id','product_id','quantity')
    search_fields = ('user_id',)
    list_editable = ('quantity',)
    list_display_links = ('product_id','user_id')


