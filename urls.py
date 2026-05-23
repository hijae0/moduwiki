from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    # 메인 주소를 encyclopedia 앱의 urls.py로 연결합니다.
    path('', include("encyclopedia.urls")), 
]