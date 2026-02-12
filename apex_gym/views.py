from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status

from .models import Membership, NewsletterSubscriber
from .serializers import MembershipSerializer, NewsletterSubscriberSerializer


class JoinOrUpdateMembershipView(GenericAPIView):
    serializer_class = MembershipSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        data = request.data

        membership_type = request.data.get(
            "membership_type", "Basic"
        )  # default to 'monthly' if none given

        membership, created = Membership.objects.get_or_create(
            user=user, defaults={"membership_type": membership_type}
        )

        # If user is already on this plan, stop here
        if not created and membership.membership_type == membership_type:
            return Response(
                {"detail": f"You’re already on the {membership_type} plan."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.get_serializer(
            membership,
            data=data,
            context=self.get_serializer_context(),
            partial=True,  # allow updates without needing all fields
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        if created:
            message = f"Welcome, {user.first_name}. You’ve successfully joined the membership!"
            status_code = status.HTTP_201_CREATED
        else:
            message = f"Hi {user.first_name}, your membership plan has been updated successfully!"
            status_code = status.HTTP_200_OK

        return Response(
            {
                "detail": message,
                "membership": serializer.data,
            },
            status=status_code,
        )


class NewsletterSubscribeView(CreateAPIView):
    serializer_class = NewsletterSubscriberSerializer
    permission_classes = []  # Public can subscribe

    def post(self, request, *args, **kwargs):
        email = request.data.get("email", "").strip().lower()

        if not email:
            return Response(
                {"error": "Email field is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Check if already subscribed
        existing = NewsletterSubscriber.objects.filter(email=email).first()

        if existing:
            if existing.is_active:
                return Response(
                    {"detail": "This email is already subscribed."},
                    status=status.HTTP_200_OK,
                )
            else:
                # Reactivate previously unsubscribed email
                existing.is_active = True
                existing.save()
                return Response(
                    {"detail": "Subscription reactivated. Welcome back!"},
                    status=status.HTTP_200_OK,
                )

        # New subscription
        serializer = self.get_serializer(data={"email": email})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {"detail": "You’ve successfully subscribed to our newsletter."},
            status=status.HTTP_201_CREATED,
        )
