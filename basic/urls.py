from . import views
from django.urls import path,include
urlpatterns=[
    path('room/<str:room>/', views.room, name='room'),
    path('home',views.index),
    path('login',views.login),
    path('login_submit',views.login_submit),
    path('form_submit',views.submit),
    path('gift_form',views.gift_form),
    path('gift',views.gift),
    path('recieve',views.recieve),
    path('req',views.req),
    path('deny',views.deny),
    path('logout',views.logout_view),
    path('accept',views.accept),
    path('inbox',views.inbox),
    path('checkview', views.checkview),
    path('send', views.send, name='send'),
    path('getMessages/<str:room>/', views.getMessages, name='getMessages'),

]