"""fileshell URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf.urls import url, include
from fileshell import views

urlpatterns = [
    url('admin/', admin.site.urls),

    url(r'^$', views.home, name='home'),
    url('search/(?P<search_name>.+)', views.search, name='search'),

    url('profile/', views.profile, name='profile'),  ## 프로필 화면
    url(r'^accounts/', include('django.contrib.auth.urls')),  ## 기본 유저
    url('account_login/', views.account_login, name='account_login'), ## 로그인 화면

    url(r'^download/(?P<bucketPath>.+)//(?P<filename>.+)//(?P<dir>.+)$', views.download, name='download'),  ## 다운로드 기능
    url(r'^delete/(?P<bucketPath>.+)//(?P<filename>.+)//(?P<dir>.+)$', views.delete, name='delete'),  ## 삭제 기능
    url(r'^delete_folder/(?P<foldername>.+)$', views.delete_folder, name='delete_folder'),
    url(r'^changeFavor/(?P<bucketPath>.+)/(?P<filename>.+)$', views.changeFavor, name='changeFavor'),  ## 즐겨찾기 on/off 기능
    url('add_folder/', views.add_folder, name='add_folder'),  ## 폴더 추가 기능
    url('signup/', views.signup, name='signup'),  ## 회원가입 기능
    url('upload/', views.upload, name='upload'),  ## 파일 업로드 기능

    url('home/', views.file, name='file'),  ## 모든 file 경로 화면 (home/으로 시작하는 모든 경로)

    url(r'^', views.home, name='home'),  ## 이외의 모든 화면 홈으로 이동
]
