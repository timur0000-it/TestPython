from django.urls import path,include

from .views import verify_code,signup,signin,signout,get_all_users,re_send_code
app_name = 'users'

urlpatterns = [
    path('', signup,name='signup'),
    path('signin/', signin, name='signin'),
    path('signout/', signout, name='signout'),
    path('verify_code/', verify_code, name='verify_code'),
    path('re_send_code/', re_send_code, name='re_send_code'),
    path('get_all_users/', get_all_users, name='get_all_users'),
   
    
    

]
