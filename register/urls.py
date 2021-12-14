from django.urls import path, include,re_path
from . import views
from django.contrib.auth import views as auth_views #import this
# urlpatterns = [
#     path('', views.index, name = 'index'),
#     path('', include("django.contrib.auth.urls")),
#     # path('login/', views.show_users, name = 'show_users'),
#     path('register/', views.register, name='register'),
#     path('show_users/', views.show_users, name = 'show_users'),
#     path('create/', views.create_user, name='create'),
#     path('show_users/delete/<int:pk>/',views.delete_user, name='delete'),
#     path('search/',views.search_user, name='search'),
# ]


urlpatterns = [
    path('',views.login_view, name='login'),
    # path('login/',views.login, name='login'),
    path('register/', views.register, name='register'),
    path('show_users/', views.show_users, name = 'show_users'),
    path('show_users/delete/<int:pk>/',views.delete_user, name='delete'),
    path('logout/',views.logout_view, name='logout'),
    path("password_reset", views.password_reset_request, name="password_reset"),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='register/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="register/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='register/password_reset_complete.html'), name='password_reset_complete'),      
    

]
