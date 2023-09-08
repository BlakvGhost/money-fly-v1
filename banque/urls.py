
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.default, name='default'), 
    path('ajax-depot', views.depot, name='depot'),
    path('ajax-retrait', views.retrait, name='retrait'),
    path('ajax-retrait-confirm', views.confirm_retrait, name='confirm_retrait'),
    path('ajax-retrait-cancel', views.cancel_retrait, name='cancel_retrait'),
    path('ajax-create-user', views.createUser, name='createUser'),
    path('ajax-get-state', views.getState, name='getState'),
]