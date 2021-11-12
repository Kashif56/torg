from django.urls import path
from . import views

from post import views as post_views

app_name = 'account'
urlpatterns = [
    path('<user>/profile/', views.UserProfileView, name='UserProfile'),
    path('complete-profile/', views.Complete_Profile, name='Complete_Profile'),
    path('<user>/update-profile/', views.Update_Profile, name='Update_Profile'),

    path('create-account/', views.Signup, name='Signup'),
    path('login/', views.Login, name='Login'),
    path('logout/', views.Logout, name='Logout'),

    # Post URLS
    path('<int:post_id>/delete-post/', post_views.Delete_Post, name='DeletePost'),
    path('create-post/', post_views.CreatePost, name='CreatePost'),
    path('<int:post_id>/edit-post/', post_views.EditPost, name='EditPost'),
    path('<int:post_id>/like-post/', post_views.LikePost, name='LikePost'),


    # Follow
    path('follow-user/<to_user>/', views.FollowUser, name='FollowUser'),
    path('followback-user/<requestID>/',
         views.Follow_back_user, name='FollowBackUser'),

    path('ignore/<int:requestID>/', views.delete_request, name='IgnoreUser'),

]
