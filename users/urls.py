from django.urls import path,include

from .views import signup,signin,signout,parol,get_all_users
app_name = 'users'

urlpatterns = [
    path('', signup,name='signup'),
    path('signin/', signin, name='signin'),
    path('signout/', signout, name='signout'),
    path('get_all_users/', get_all_users, name='get_all_users'),
    path('parol/<str:username>', parol, name='parol'),
    
    

]
