from django.urls import path
from myapp import views

app_name = 'myapp'

urlpatterns = [
    path('', views.index, name="index"),
    path('login/', views.login, name="login"),
    path('signup/', views.signup, name="signup"),
    path('user_login/', views.user_login, name="user_login"),
    path('user_signup/', views.user_signup, name="user_signup"),
    path('dashboard/', views.profile, name="dashboard"),
    path('property_view/', views.property_view, name="property_view"),
    path('logout/', views.logout, name="logout"),
    path('dashboard/history/', views.history, name="history"),
    path('dashboard/new_post/', views.new_post, name="new_post"),
    path('dashboard/profile/', views.profile, name="profile"),
    path('property_post/', views.property_post, name="property_post"),
    path('property_view/details/<str:p_id>/delete',
         views.property_delete, name="property_delete"),
    path('property_view/details/<str:p_id>/edit',
         views.property_edit, name="property_edit"),
    path('property_view/details/<str:p_id>',
         views.property_details, name="property_details"),
    # path('table_view/', views.table_view, name = "table_view"),
]
