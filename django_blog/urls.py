"""django_blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from blog.views import post_list,post_create,post_details,post_uptade,post_delete,add_comment
from django.conf import settings
from django.conf.urls.static import static
from users.views import register,userlogin,userlogout,userprofile,user_settings,user_about,user_password_change

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/',post_list,name='post_list'),
    path('post-create/', post_create, name='post_create'),
    path("blog/<int:id>",post_details, name ="post_details"),
    path("blog-uptade/<int:id>",post_uptade, name ="post_uptade"),
    path("blog-delete/<int:id>",post_delete, name ="post_delete"),
    path("add-comment/<int:id>",add_comment, name ="add_comment"),
    path('register/', view=register, name='register'),
    path('userlogin/', view=userlogin, name='userlogin'),
    path('userlogout/', view=userlogout, name='userlogout'),
    path("userprofile/<str:username>",view=userprofile, name ="userprofile"),
    path('usersetting/', view=user_settings, name='usersetting'),
    path('aboutme/<str:username>', view=user_about, name='userabout'),
    path('passchange/', view=user_password_change, name='passchange'),







]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_URL)

