from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Membership, NewsletterSubscriber
import csv
from django.http import HttpResponse
from django.core.mail import send_mass_mail

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
    actions = ["send_newsletter", "unsubscribe_selected", "export_emails"]

    def send_newsletter(self, request, queryset):
        # Example mass email - customize as needed
        subject = "💪 Your Gym Weekly Newsletter"
        message = (
            "Hey Champ,\n\nHere’s what’s new this week at the gym: \n"
            "- New classes\n- Workout tips\n- Nutrition guide\n\nStay strong!"
        )
        from_email = "no-reply@gymfreak.com"

        emails = [subscriber.email for subscriber in queryset if subscriber.is_active]

        if not emails:
            self.message_user(request, "No active emails selected.", level="warning")
            return

        messages = [(subject, message, from_email, [email]) for email in emails]

        try:
            send_mass_mail(messages, fail_silently=False)
            self.message_user(request, f"Newsletter sent to {len(emails)} subscribers.")
        except Exception as e:
            self.message_user(request, f"Failed to send: {str(e)}", level="error")

    send_newsletter.short_description = "📧 Send weekly newsletter"

    def unsubscribe_selected(self, request, queryset):
        count = queryset.update(is_active=False)
        self.message_user(request, f"{count} subscriber(s) unsubscribed.")
    
    unsubscribe_selected.short_description = "❌ Mark as unsubscribed"

    def export_emails(self, request, queryset):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="newsletter_subscribers.csv"'

        writer = csv.writer(response)
        writer.writerow(["Email", "Subscribed At", "Is Active"])

        for sub in queryset:
            writer.writerow([sub.email, sub.subscribed_at, sub.is_active])

        return response

    export_emails.short_description = "📥 Export selected to CSV"
