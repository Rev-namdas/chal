from django.contrib import admin
from addstock.models import stockModel, productsModel, sellStockModel, remainingModel

# Register your models here.
class stockModelTable(admin.ModelAdmin):
    list_display = ['stockedby', 'rice', 'amount', 'bosta']


class productModelTable(admin.ModelAdmin):
    list_display = ['product', 'productamount', 'productbosta']


class sellStockModelTable(admin.ModelAdmin):
    list_display = ['customer', 'rice', 'amount', 'bosta', 'time', 'price']


class remaingModelTable(admin.ModelAdmin):
    list_display = ['product', 'ramount', 'rbosta']


admin.site.register(stockModel, stockModelTable)
admin.site.register(productsModel, productModelTable)
admin.site.register(sellStockModel, sellStockModelTable)
admin.site.register(remainingModel, remaingModelTable)