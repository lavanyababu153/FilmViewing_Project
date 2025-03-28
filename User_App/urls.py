from django.urls import path
from User_App import views

urlpatterns = [
    path('user_home/', views.user_home, name="user_home"),  # <-- Add a trailing slash here
    path('signup', views.signup, name="signup"),
    path('signup_error', views.signup_error, name="signup_error"),
    path('login', views.user_login, name="user_login"),
    path('login_error', views.login_error, name="login_error"),
    path('movie_search', views.movie_search, name="movie_search"),
    path('user_logout', views.user_logout, name='user_logout'),
    path('profile_update', views.profile_update, name='profile_update'),
    path('update_profile', views.update_profile, name="update_profile"),
    path('movie_details/<int:m_id>/', views.movie_details, name='movie_details'),
    path('add_comment/<int:v_id>/', views.add_comment, name='add_comment'),
    path('plan_details', views.plan_details, name="plan_details"),
    path('add_subscription/<int:plan_id>/', views.add_subscription, name='add_subscription'),
    path('user_reaction/<int:m_id>/<str:action>/', views.user_reaction, name='user_reaction'),
    path('plan_history', views.plan_history, name='plan_history'),
    path("view_profile", views.view_profile, name="view_profile"),
    path('add_favourite/<int:f_id>/<str:add>', views.add_favourite, name="add_favourite"),
    path('confirm_subscription/<int:plan_id>', views.confirm_subscription, name="confirm_subscription"),
    path('user_favourites', views.user_favourites, name="user_favourites"),
    path('liked_movies', views.liked_movies, name="liked_movies"),
    path('confirm/<int:plan_id>/', views.confirm, name='confirm'),
    path('process_payment/<int:subscription_id>/', views.process_payment, name='process_payment'),
    path('Films', views.Films, name='Films'),
]
