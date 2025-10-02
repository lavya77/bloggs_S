from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('create-account/',views.signup_view,name="create-account"),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('create/', views.create_post, name='post_create'),
    path('profile/<str:username>/', views.profile_view, name='profile'),
    #path("post/create/", views.post_create, name="post_create"),
    #path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/<int:pk>/like/', views.like_post, name='like_post'),
    path('post/<int:post_id>/share/', views.share_post, name='share_post'),
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path("search/", views.search_results, name="search_results"),
    path('notifications/', views.notifications_view, name='notifications'),
]
