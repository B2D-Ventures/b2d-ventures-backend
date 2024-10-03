from django.urls import path
from . import views

urlpatterns = [
    path("", views.list_stub_endpoints, name="list-stub-endpoints"),
    path("auths/", views.auth_create, name="auth-create"),
    path("auths/update/", views.auth_update, name="auth-update"),
    path("startup/<str:pk>/profile/", views.startup_profile, name="startup-profile"),
    path("startup/<str:pk>/deals/", views.startup_deals, name="startup-deals"),
    path("investor/<str:pk>/profile/", views.investor_profile, name="investor-profile"),
    path(
        "investor/<str:pk>/investments/",
        views.investor_investments,
        name="investor-investments",
    ),
    path("admin/users/", views.admin_list_users, name="admin-list-users"),
    path("admin/deals/", views.admin_list_deals, name="admin-list-deals"),
]
