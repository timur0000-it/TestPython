from django.urls import path,include

from .views import signup,signin,signout,kod
app_name = 'users'

urlpatterns = [
    path('signup/', signup,name='signup'),
    path('signin/', signin, name='signin'),
    path('signout/', signout, name='signout'),
    path('kod/<str:username>', kod, name='kod'),
    
    

]
