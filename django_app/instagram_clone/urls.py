"""instagram_clone URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from restapi.views import  *
from rest_framework import routers

from rest_auth.views import (
    LoginView, LogoutView, UserDetailsView, PasswordChangeView,
    PasswordResetView, PasswordResetConfirmView
)

router = routers.DefaultRouter()
router.register(r'content', ContentViewSet)
router.register(r'subscriptions', SubscriptionsView)
# router.register(r'subscriptions/subscribers/', SubscribersView)
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^tags/', TagsView.as_view()),
    url(r'^account/', include('rest_auth.urls')),
    url(r'^account/register/', include('rest_auth.registration.urls')),
    url(r'^subscriptions/subscribers/user/(?P<pk>[0-9]+)', SubscribersView.as_view()),
    # url(r'^subscriptions/subscribers/tag/', TagSubscribersView.as_view()),
    url(r'^subscriptions/subscribers/tag/(?P<tag>[0-9]+)', TagSubscribersView.as_view()),
]

urlpatterns += router.urls
