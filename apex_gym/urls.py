

from django.urls import path
from .views import JoinMembershipView, NewsletterSubscribeView

urlpatterns = [
    path("join/", JoinMembershipView.as_view(), name="join-membership"),
    path("subscribe/", NewsletterSubscribeView.as_view(), name="newsletter-subscribe"),
]
