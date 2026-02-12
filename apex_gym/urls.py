

from django.urls import path
from .views import JoinOrUpdateMembershipView, NewsletterSubscribeView

urlpatterns = [
    path("join/", JoinOrUpdateMembershipView.as_view(), name="join-membership"),
    path("subscribe/", NewsletterSubscribeView.as_view(), name="newsletter-subscribe"),
]
