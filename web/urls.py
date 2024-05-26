from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('topic/<int:topic_id>/', views.topic_detail, name='topic_detail'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('explanation/<int:explanation_id>/upvote/', views.upvote_explanation, name='upvote_explanation'),
    path('explanation/<int:explanation_id>/downvote/', views.downvote_explanation, name='downvote_explanation'),
    path('explanation/<int:explanation_id>/favorite/', views.favorite_explanation, name='favorite_explanation'),
    path('explanation/<int:explanation_id>/edit/', views.edit_explanation, name='edit_explanation'),
    path('explanation/<int:explanation_id>/delete/', views.delete_explanation, name='delete_explanation'),
    path('profile/', views.profile, name='profile'),
    path('new_topic/', views.new_topic, name='new_topic'),
    path('topic/<int:topic_id>/add_explanation/', views.add_explanation, name='add_explanation'),
    path('favorites/', views.favorites, name='favorites'),
    path('explanations/', views.user_explanations, name='user_explanations'),
    path('search/', views.search, name='search'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'),
         name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
         name='password_reset_complete'),
]
