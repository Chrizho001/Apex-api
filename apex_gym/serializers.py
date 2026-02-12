from .models import Membership, NewsletterSubscriber
from rest_framework import serializers
from django.utils import timezone



class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = [
            "membership_type",
            "join_date",
            "is_active",
        ]  # Only include fields user should control
        read_only_fields = ["join_date", "is_active"]

    def create(self, validated_data):
        user = self.context["request"].user
        return Membership.objects.create(user=user, **validated_data)


class NewsletterSubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsletterSubscriber
        fields = ["email"]

    def validate_email(self, value):
        value = value.lower().strip()
        if NewsletterSubscriber.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already subscribed.")
        return value
    
    def update(self, instance, validated_data):
        instance.membership_type = validated_data.get("membership_type", instance.membership_type)
        instance.join_date = timezone.now()  # reset date on change
        instance.save()
        return instance

