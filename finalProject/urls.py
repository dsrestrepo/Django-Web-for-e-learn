from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("course/<str:cname>", views.course, name="course"),
    path("social_web", views.social_web, name="social_web"),
    path("make_test", views.make_test, name="make_test"),
    path("profile/<str:username>", views.profile, name="profile"),
    #API
    path("test", views.test, name="test"),
    path("newPost", views.newPost, name="newPost"),
    path("newMessage", views.newMessage, name="newMessage"),
    path("read", views.read, name="read"),
    path("editUser", views.editUser, name="editUser"),
    path("load_csv_file", views.load_csv_file, name="load_csv_file"),
    path("get_recommendation", views.get_recommendation, name="get_recommendation"),
    path("ratings/<int:movie_id>", views.ratings, name="ratings")
    
    
]