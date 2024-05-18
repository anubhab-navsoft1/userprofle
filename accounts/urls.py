from django.urls import path
from .import views

urlpatterns = [
    path("user/signup/", views.UserRegisrationView.as_view() ),
    path("user/signin/", views.UserSignInView.as_view() ),
    path("user/delete/", views.DeleteAllUsersView.as_view() ),
    path("user/delete/<int:id>/", views.DestroyById.as_view() ),
    #  path("user/update/<int:pk>/", views.UpdateUser.as_view() ),
    path("user/", views.UserListView.as_view() )
]
