import os

from django.conf import settings
from django.http import FileResponse, HttpResponse


def media_serve(request, path):
    # /media/로 시작하는 모든 URL이 해당 view를 통해 처리
    # /media/<뒤>/ 에서
    # <뒤> 부분을 path라는 변수에 할당
    # settings에 있는 MEDIA_ROOT를 기준으로 (import django.conf import settings)
    # settings.MEDIA_ROOT
    # file_path에 있는 내용을 open()한 결과를 Fileresponse 담아서 리턴

    file_path = os.path.join(settings.MEDIA_ROOT, path)

    f = open(file_path, 'rb')

    return FileResponse(f, content_type='image/jpeg')
    # return HttpResponse(path)