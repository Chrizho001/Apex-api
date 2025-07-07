from .models import Membership, NewsletterSubscriber
from rest_framework import serializers




class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = ['membership_type']  # Only include fields user should control

    def create(self, validated_data):
        user = self.context['request'].user
        return Membership.objects.create(user=user, **validated_data)


class NewsletterSubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsletterSubscriber
        fields = ['email']
        

    def validate_email(self, value):
        value = value.lower().strip()
        if NewsletterSubscriber.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already subscribed.")
        return value
