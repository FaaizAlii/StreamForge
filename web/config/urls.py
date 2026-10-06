"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.contrib.auth.decorators import login_required

from content import views


urlpatterns = [
    path("admin/", admin.site.urls),

    # Authentication
    path("accounts/", include("accounts.urls")),

    # subscriptions
    path("subscriptions/", include("subscriptions.urls")),

    path("chat/", include("chat.urls")),

    # Protected application
    path(
        "",
        login_required(views.home),
        name="home",
    ),

    path(
        "movies/<int:movie_id>/",
        login_required(views.movie_detail),
        name="movie_detail",
    ),

    path(
        "shows/<int:show_id>/",
        login_required(views.show_detail),
        name="show_detail",
    ),

    # APIs
    path(
        "api/",
        login_required(include("content.urls")),
    ),
]