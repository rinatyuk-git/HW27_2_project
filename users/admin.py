from django.contrib import admin

from users.models import User, Payments

admin.site.register(User)


@admin.register(Payments)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "payment_date",
    )
