from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status

from .models import Membership, NewsletterSubscriber
from .serializers import MembershipSerializer, NewsletterSubscriberSerializer


class JoinMembershipView(CreateAPIView):
    serializer_class = MembershipSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user

        # Prevent duplicate memberships
        if Membership.objects.filter(user=user).exists():
            return Response(
                {"detail": "You already have an active membership."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()  # user is assigned in serializer
        return Response(
            {
                "detail": f"Welcome, {user.first_name}. You’ve successfully joined the membership!",
                "membership": serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )


class NewsletterSubscribeView(CreateAPIView):
    serializer_class = NewsletterSubscriberSerializer
    permission_classes = [IsAuthenticated]  # Public can subscribe

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
