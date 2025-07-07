from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Membership, NewsletterSubscriber

@admin.register(Membership)
class MembershipAdmin(ModelAdmin):
    list_display = ("user", "membership_type", "join_date", "is_active")
    list_filter = ("membership_type", "is_active", "join_date")
    search_fields = ("user__email", "user__first_name", "user__last_name")
    autocomplete_fields = ("user",)
    readonly_fields = ("join_date",)

@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(ModelAdmin):
    list_display = ("email", "subscribed_at", "is_active")
    list_filter = ("is_active", "subscribed_at")
    search_fields = ("email",)
    readonly_fields = ("subscribed_at",)
