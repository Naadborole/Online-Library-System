from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('login', views.LoginForm.as_view(), name='login'),
    path('signup', views.SignUp.as_view(), name='signup'),
    path('main/<str:id>/', views.mainPage.as_view(), name='main'),
    path('getlist/<str:objid>/', views.getList.as_view(), name='getlist'),
    path('getuser/<str:id>/', views.getuser.as_view(), name='getuser'),
    path('getCatalogue/', views.getCatalogue.as_view(), name='catalogue'),
    path('search/<str:title>/', views.searchTitle.as_view(), name='search'),
    path('getbook/<str:id>/<str:email>', views.getBook.as_view(), name='getbook'),
    path('addbook/<str:id>/<str:email>', views.addTolist.as_view(), name='addbook'),
    path('removebook/<str:id>/<str:email>', views.removeFromList.as_view(), name='removebook'),
]
