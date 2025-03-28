from django.urls import path
from Admin_App import views

urlpatterns = [
    path('home',views.admin_home,name ="admin_home"),
    path('add',views.add_film,name ="add_film"),
    path('manage',views.manage_film,name ="manage_film"),
    path('view',views.view_film,name ="view_film"),
    path('film_delete/<int:f_id>',views.film_delete,name ="film_delete"),
    path('film_update/<int:c_id>',views.film_update,name="film_update"),
    path('update_movie/<int:l_id>',views.update_movie,name="update_movie"),
    path('genre_add',views.genre_add,name ="genre_add"),
    path('manage_genre',views.manage_genre,name ="manage_genre"),
    path('genre_view',views.genre_view,name ="genre_view"),
    path('genre_delete/<int:gd_id>',views.genre_delete,name="genre_delete"),
    path('genre_update/<int:u_id>',views.genre_update,name="genre_update"),
    path('update_gernre/<int:p_id>',views.update_genre,name="update_genre"),
    path('view_user',views.view_user,name="view_user"),
    path('add_cast',views.add_cast,name="add_cast"),
    path('add_plan',views.add_plan,name="add_plan"),
    path('view_comment/<m_id>',views.view_comment,name="view_comment"),
    path('manage_plan',views.manage_plan,name="manage_plan"),
    path('delete_plan/<int:p_id>',views.delete_plan,name="delete_plan"),
    path('update_plan/<int:u_id>',views.update_plan,name="update_plan"),
    path('plan_update/<int:b_id>',views.plan_update,name="plan_update"),
    path('view_plan',views.view_plan,name="view_plan"),
    path('view_cast',views.view_cast,name="view_cast"),
    path('manage_cast',views.manage_cast,name="manage_cast"),
    path('cast_delete/<int:c_id>',views.cast_delete,name="cast_delete"),
    path('update_cast/<int:s_id>',views.update_cast,name="update_cast"),
    path('cast_update/<int:cast_id>',views.cast_update,name="cast_update"),
    path('view_subscription',views.view_subscription,name="view_subscription"),
    path('admin_logout',views.admin_logout,name='admin_logout'),
    path('view_payment/<int:sub_id>/', views.view_payment, name='view_payment'),
    path('admin_profile/', views.admin_profile, name='admin_profile'),
    path('admin_update', views.admin_update, name='admin_update'),
    path('profile_update', views.profile_update, name='profile_update'),
    
    
  
   
   
        ]