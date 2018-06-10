from django.db.models import Case, Value, When
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.http import *
from .storages import *
from .forms import *
from .models import *
import time
import datetime


def home(request):

    # user가 로그인 되어 있을 때
    if request.user.is_authenticated:
        # user가 갖고 있는 파일 중 즐겨찾기 True인 파일 필터링
        favorList = File.objects.filter(isFavor=True, user=request.user.username)

        # user가 갖고 있는 파일 중 일주일 안에 다운로드 된 파일 필터링
        endTime = datetime.datetime.now()
        startTime = endTime - datetime.timedelta(days=3)  # 최근 날짜 기준 (현재: 3일)
        recentList = File.objects.filter(last_view_TM__range=[startTime, endTime], user=request.user.username)

        return render(request, 'home.html', {'favorList': favorList, 'recentList': recentList})
    # user가 로그인 되어 있지 않을 때 로그인 화면 출력
    else:
        return render(request, 'login.html')

def file(request):

    # user가 로그인 되어 있을 때
    if request.user.is_authenticated:
        pass
    # user가 로그인 되어 있지 않을때 home으로 이동(로그인 화면 출력)
    else:
        return redirect('/')


    this_path = request.path
    dir = this_path[1:]

    type = this_path.split('/')
    type.pop(0)
    type = type.pop(0)

    # user가 갖고 있는 폴더 중 현재 url을 parent로 갖는 폴더 필터링
    folderList = Folder.objects.filter(parent__dir_name=dir, user=request.user.username)
    # user가 갖고 있는 파일 중 현재 url을 폴더 dir로 갖는 폴더 필터링
    fileList = File.objects.filter(folder__dir_name=dir, user=request.user.username)

    return render(request, 'file.html', {'folderList': folderList, 'fileList': fileList})

def search(request, search_name):

    # user가 로그인 되어 있을 때
    if request.user.is_authenticated:
        pass
    # user가 로그인 되어 있지 않을때 home으로 이동(로그인 화면 출력)
    else:
        return redirect('/')


    this_path = request.path
    dir = this_path[1:]

    type = this_path.split('/')
    type.pop(0)
    type = type.pop(0)
    print(type)


    name = request
    print(name)
    # user가 갖고 있는 폴더 중 현재 url을 parent로 갖는 폴더 필터링
    folderList = Folder.objects.filter(dir_name__contains=search_name, user=request.user.username)
    # user가 갖고 있는 파일 중 현재 url을 폴더 dir로 갖는 폴더 필터링
    fileList = File.objects.filter(title__contains=search_name, user=request.user.username)

    return render(request, 'search.html', {'folderList': folderList, 'fileList': fileList})

def profile(request):

    # 유저 정보 출력
    return render(request, 'profile.html')

def account_login(request):

    # 로그인 화면 출력
    return render(request, 'login.html')

def signup(request):

    # requst가 POST일 때
    if request.method == "POST":
        # user 폼 지정
        form = UserForm(request.POST)

        # form이 유효할 때
        if form.is_valid():
            # 로컬 DB에 user 저장
            new_user = User.objects.create_user(**form.cleaned_data)
            # 유저 정보로 로그인
            login(request, new_user)

            # 로컬 DB에 디폴트 경로 저장
            Folder.objects.create(dir_name='home/', user=request.user.username)

            # s3 main bucket에 userid/ 디렉토리와 userid/home/ 디렉토리 생성
            MediaStorage.create_dir(new_user.username)
            MediaStorage.create_dir(new_user.username + '/home')

            # home 화면으로 이동
            return redirect('/')

        # form이 유효하지 않을 때
        else:
            ########################### 사용자 폼 부적합 알림 #######################
            print("사용자 폼 부적합")

            # home 화면으로 이동(로그인 화면)
            return redirect('/')

def add_folder(request):

    # requst가 POST일 때
    if request.method == 'POST':

        ## 파일 model 변수 초기화
        user = request.user.username
        dir_name = request.POST.get('dir_name')
        temp = request.META.get('HTTP_REFERER', '/')
        dir = url_convert(temp)
        parent = Folder.objects.get(dir_name=dir, user=user)

        # 로컬 DB에 저장
        Folder.objects.create(dir_name=dir+dir_name+'/', parent=parent, user=user)
        # s3 main bucket에 dir/ 디렉토리에 dir_name/ 디렉토리 생성
        MediaStorage.create_dir(user + '/' +dir + dir_name)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def upload(request):
    if request.method == 'POST':
        print(request.FILES)
        ## 파일 model 변수 초기화
        filedata = request.FILES.get('file')  # request.Files['file'] 함수 썻을 때 오류 발생할 수 있음!!
        title = request.FILES.get('file')
        user = request.user
        user_name = request.user.username
        now = time.localtime()
        uploadde_TM = "%04d-%02d-%02d %02d:%02d:%02d" % (
            now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
        filesize = filedata.size
        temp = request.META.get('HTTP_REFERER', '/')
        dir = url_convert(temp)
        folder = Folder.objects.get(dir_name=dir, user=request.user.username)

        # 로컬 DB에 저장
        File.objects.create(title=title, user=user, isFavor=False, bucketPath=user_name+'/'+dir,
                            fileSize=filesize, folder=folder)
        # s3 버킷에 저장
        MediaStorage.upload_file(filedata, user, dir)
    else:
        pass
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def download(request, bucketPath, filename, dir):

    # 경로와 이름이 같은 파일을 필터링
    #### 같은 이름을 가진 파일에 경우 겹칠 수 있음 ####

    # 필터링 된 파일 최근 열람 시간 갱신
    File.objects.filter(title=filename, bucketPath=dir).update(last_view_TM=datetime.datetime.now())
    """
    # s3에서 해당 파일을 정해진 경로로 다운로드
    MediaStorage.download_file(filename, bucketPath)
    """

    url = MediaStorage.down(filename, bucketPath)

    return HttpResponseRedirect(url)

def delete(request, bucketPath, filename, dir):

    # 경로와 이름이 같은 파일을 필터링
    #### 같은 이름을 가진 파일에 경우 겹칠 수 있음 ####

    # 필터링 된 파일 로컬 DB에서 삭제
    File.objects.filter(title=filename, bucketPath=dir).delete()

    # s3에서 해당 파일을 정해진 경로로 삭제
    MediaStorage.delete_file(filename, bucketPath)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def changeFavor(request, bucketPath, filename):

    # 경로와 이름이 같은 파일을 필터링
    #### 같은 이름을 가진 파일에 경우 겹칠 수 있음 ####

    # 해당 파일 즐겨찾기 값을 True면 False로 False면 True로 수정
    File.objects.filter(title=filename, bucketPath=bucketPath).update(isFavor=Case(
        When(isFavor=True, then=Value(False)),
        default=Value(True))
    )

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

# url 원하는 형식으로 바꿔주기 위함
def url_convert(url):
    url = str(url)
    temp = url.split('/')
    temp.pop(0);temp.pop(0);temp.pop(0)
    dir = ''
    for i in temp:
        dir += i + '/'
    dir = dir[:-1]
    return dir


