from collections import UserList
from operator import index
from django.shortcuts import render,get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status #응답코드용 
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import *
from django.contrib.auth import get_user_model
import json
import pymysql
import django.db
import sys
from django.conf import settings
import json
import boto3
from django.http import JsonResponse
import uuid

# Create your views here.

@api_view(['POST'])
@permission_classes([AllowAny])
def user_signup(request): #회원가입
    userserializer=UserSerializer(data=request.data)
    if userserializer.is_valid(raise_exception=True): #UserSerializer validate
        token = userserializer.save()
        return Response(token,status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_400_BAD_REQUEST)

@permission_classes([AllowAny]) #로그인
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class=MyTokenObtainPairSerializer

@api_view(['PUT'])    
# @permission_classes([IsAuthenticated]) #회원으로 인증된 요청 한해서 view 호출
def user_info_update(request): #회원정보 수정
    body=json.loads(request.body)
    User=get_user_model()
    me=get_object_or_404(User,phone_num=body["phone_num"])

    # print(me)
    
    userserializer=UserSerializer(me,data=request.data)
    # print(userserializer.is_valid())
    if userserializer.is_valid():
        token=userserializer.save()
        # print(token)
        return Response(status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_400_BAD_REQUEST)

def check(request):
    s3_client = boto3.client(
        's3',
        aws_access_key_id = getattr(settings, 'AWS_ACCESS_KEY_ID'), 
        aws_secret_access_key = getattr(settings, 'AWS_SECRET_ACCESS_KEY')
    )

    file = request.FILES.get('file')
    filename = str(uuid.uuid1()).replace('-','')
    s3_client.upload_fileobj(
        file,
        'recycleledger-image',
        filename,
        ExtraArgs = {
            "ContentType" : 'image/jpeg'
        }
    )
    return JsonResponse({'message':'SUCCESS'},status=200)






# request에 {"phone_num":"","update_data":{}}

'''
    업데이트시 수정해서 폼 그대로 작성
    {
        "phone_num":"01024280249",
        "username":"이태검",
        "address":"여의도 위워크",
        "account":"27960204127606",
        "po_name":"버거킹 서초점",
        "business_num":"1234123412",
        "password":"password",
        "job":"중상"
    }   



    회원가입시 POST
    {
        "phone_num":"01024280249",
        "username":"이태검",
        "address":"여의도 위워크",
        "account":"27960204127606",
        "po_name":"버거킹",
        "business_num":"1234123412",
        "password":"password",
        "job":"중상"
    }   
    return 
    {
        "refresh":"토큰",
        "access":"토큰"
    }
    
'''
'''
    로그인시 POST 
    {
        "phone_num":"01024280249",
        "password":"패스워드"
    }
    return
    {
        "refresh": "토큰",
        "access": "토큰",

    }
'''
'''
    로그아웃시 POST
    {
        "refresh":"토큰"
    }
    return
    {} #200ok
    
    로그인 안한상황에 로그아웃하면
    {
        "detail": "블랙리스트에 추가된 토큰",
        "code": "token_not_valid"
    }
  
'''

