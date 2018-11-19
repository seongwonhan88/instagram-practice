import imghdr
from pprint import pprint

import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

User = get_user_model()


class FacebookBackend:
    def authenticate(self, request, facebook_request_token):
        api_base = 'https://graph.facebook.com/v3.2'
        api_get_access_token = f'{api_base}/oauth/access_token?'
        api_me = f'{api_base}/me'
        # code = facebook_request_token
        # request token to access token using 'requests'

        # VERY IMPORTANT. NO HARDCODING
        params = {
            'client_id': settings.FACEBOOK_APP_ID,
            'redirect_uri': 'http://localhost:8000/members/facebook-login/',
            'client_secret': settings.FACEBOOK_APP_SECRET,
            'code': facebook_request_token
        }

        response = requests.get(api_get_access_token, params)
        # response_object = json.loads(response.text)
        # # return HttpResponse('{}, {}'.format(response_object, type(response_object)))

        data = response.json()
        access_token = data['access_token']

        # using access token to bring user info

        params = {
            'access_token': access_token,
            'fields': ', '.join([
                'id',
                'first_name',
                'last_name',
                'picture.type(large)',
            ]),
        }
        response = requests.get(api_me, params)
        data = response.json()
        pprint(data)

        facebook_id = data['id']
        first_name = data['first_name']
        last_name = data['last_name']
        url_img_profile = data['picture']['data']['url']
        # requesting for image url
        img_response = requests.get(url_img_profile)
        img_data = img_response.content
        # extension finder from binary
        ext = imghdr.what('', h=img_data)
        # first parameter for name, and second for binary file
        f = SimpleUploadedFile(f'{facebook_id}.{ext}', img_response.cdontent)
        try:
            user = User.objects.get(username=facebook_id)
            user.last_name = last_name
            user.first_name = first_name
            # user.img_profile = f
            user.save()

        except User.DoesNotExist:
            user = User.objects.create_user(
                username=facebook_id,
                first_name=first_name,
                last_name=last_name,
                img_profile=f, )

        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
