from django.urls import path
from . import views

urlpatterns = [
    path('register',views.register,name='register'),
    path('login/',views.login , name='login'),
    path('',views.index,name='index'),
    path('profile/',views.profile,name='profile'),
    path('view_profile/<int:pk>/',views.view_profile,name='view_profile'),
    path('edit_profile/<int:pk>/',views.edit_profile,name='edit_profile'),
    path('add_movie/',views.add_movie,name='add_movie'),
    path('view_movie/<int:movie_id>/',views.view_movie,name='view_movie'),
    path('edit_movie/<int:movie_id>/',views.edit_movie,name='edit_movie'),
    path('delete_movie/<int:movie_id>/',views.delete_movies,name='delete_movies'),
    path('review_movie/<int:movie_id>/',views.submit_review,name='submit_review'),
    path('movie/<int:movie_id>/reviews/', views.view_reviews, name='view_reviews'),
    # path('movie_list/',views.movie_list,name='movie_list'),
    path('logout',views.logout_view,name='logout'),
    path('search/', views.search_movies, name='search_movies'),
    path('genres/', views.genres_list, name='genres_list'),
    path('genre/<int:category_id>/', views.movies_by_genre, name='movies_by_genre'),


    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admins/add_genre/', views.add_genre, name='add_genre'),
    path('admins/add_movie/', views.add_movies, name='add_movies'),
    path('admins/delete_movie/<int:movie_id>/', views.delete_movie, name='delete_movie'),
    path('admins/delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
]