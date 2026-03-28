from django.contrib import admin
from django.utils.html import format_html
from .models import Order, Category, Product

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    # 1. Vizual ko'rinish uchun funksiya
    def status_colored(self, obj):
        if obj.status == 'Yetkazildi':
            color = '#2ecc71'  # Yashil
            text = 'Topshirildi ✅'
        elif obj.status == 'Bekor qilindi':
            color = '#e74c3c'  # Qizil
            text = 'Bekor qilindi ❌'
        else:
            color = '#f1c40f'  # Sariq
            text = 'Kutilmoqda ⏳'
            
        return format_html(
            '<span style="color: white; background-color: {}; padding: 4px 10px; border-radius: 12px; font-weight: bold; font-size: 11px;">{}</span>',
            color, text
        )

    status_colored.short_description = 'Vizual Holat'

    # 2. Jadvallarni sozlash
    # DIQQAT: 'status' bu yerda bo'lishi SHART, aks holda list_editable xato beradi
    list_display = ('id', 'product', 'customer', 'status', 'status_colored', 'created_at')
    
    # 3. Sahifaning o'zida tahrirlash imkoniyati
    list_editable = ('status',) 
    
    # 4. Qo'shimcha qulayliklar
    list_filter = ('status', 'created_at')
    search_fields = ('customer__username', 'product__name', 'phone', 'address')
    date_hierarchy = 'created_at'
    
    # Tartiblash (oxirgi buyurtmalar tepada)
    ordering = ('-created_at',)


admin.site.register(Category)
admin.site.register(Product)