from django.contrib import admin

from .models import PremiumOrder, PremiumPlan, Coupon


admin.site.register(Coupon)


@admin.register(PremiumPlan)
class PremiumPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'longtime', 'price', )


@admin.register(PremiumOrder)
class PremiumOrder(admin.ModelAdmin):
    list_display = ('plan', 'paid', 'user', 'paid_count', 'datetime_created', )
