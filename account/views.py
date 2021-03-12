# restframework imports
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
#jwt
from rest_framework_simplejwt.views import TokenViewBase
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
#djnago imports
from django.conf import settings
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from .serializers import (
	UserCreateSerializer, SubscriberAuthSerializer,
	InstructorAuthSerializer, AdminAuthSerializer,
	UserDetailSerializer, UserListSerializer,
	ChangePasswordSerializer,
)

from utils import res_codes
from utils.permissions import IsAdmin

User = get_user_model()


class SignUpView(APIView):
	serializer_class = UserCreateSerializer

	def post(self, request, *args, **kwargs):
		"""
		### Body:
		```
		{
		    "email": "vs@yopmail.com",
		    "first_name": "v",
		    "last_name": "s",
		    "password": "password",
		    "profile": {
		        "country": "India",
		        "organization":"School",
		        "date_of_birth": "2019-02-19"
		    }
		}
		```

		#### Response (success):
		```
		{
		    "code": 1001,
		    "msg": "Account created successfully",
		    "data": {
		        "id": "db54e0a6-a9e3-40b6-b2d0-1a54b3583320",
		        "first_name": "v",
		        "last_name": "s",
		        "email": "vs@yopmail.com",
		        "profile": {
		            "country": "India",
		            "date_of_birth": "2019-02-19",
		            "organization": "School"
		        }
		    }
		}
		```

		#### Response (error):
		```
		{
		    "code": 1000,
		    "msg": "Invalid post data provided",
		    "data": {
		        "first_name": [
		            "This field may not be blank."
		        ],
		        "password": [
		            "This field may not be blank."
		        ],
		        "email": [
		            "This field may not be blank."
		        ],
		        "last_name": [
		            "This field may not be blank."
		        ],
		        "profile": {
		            "date_of_birth": [
		                "Date has wrong format. Use one of these formats instead: YYYY-MM-DD."
		            ],
		            "organization": [
		                "This field may not be blank."
		            ],
		            "country": [
		                "This field may not be blank."
		            ]
		        }
		    }
		}
		```

		#### Response (error):
		```
		{
			"code": 1000,
			"msg": "Invalid post data provided",
			"data": {
				"email": [
					"This field must be unique."
				]
			}
		}
		```
		#### Response (error):
		```
		{
		    "code": 1000,
		    "msg": "Invalid post data provided",
		    "data": {
		        "profile": {
		            "date_of_birth": [
		                "Date has wrong format. Use one of these formats instead: YYYY-MM-DD."
		            ]
		        }
		    }
		}
		```
		"""
		data = request.data.copy()
		serializer = self.serializer_class(data=data)
		if serializer.is_valid():
			user_obj = serializer.save()
			return Response(
				res_codes.get_response_dict(
					res_codes.SIGNUP_SUCCESS,
					serializer.data,
				),
				status=status.HTTP_201_CREATED,
			)
		return Response(
			res_codes.get_response_dict(
				res_codes.INVALID_POST_DATA,
				serializer.errors,
			),
			status=status.HTTP_400_BAD_REQUEST
		)


class LoginViewBase(TokenViewBase):

	def post(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)

		try:
			serializer.is_valid(raise_exception=True)
		except TokenError as e:
			raise InvalidToken(e.args[0])

		return Response(
			res_codes.get_response_dict(
				res_codes.LOGIN_SUCCESS,
				serializer.validated_data,
			)
		)


class SubscriberLoginAPIView(LoginViewBase):
	"""
	#### Response:
	```
	{
		"code": 1003,
		"msg": "Login authentication is successful",
		"data": {
			"refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTU1MTA4MzkyMiwianRpIjoiMDBiMGFhMWM0NjEwNDAyMDkzMGUxZTY4YzFhMmQ2ZTEiLCJ1c2VyX2lkIjoiMjg5ZDg3ZGYtY2RkZS00OGQzLTg5MzctZGJlMjE5YTVhYTNkIn0.M2kAaTGOLsHmbM6f9TRGxk27Pa7BFiWpAnXjf0Mhc-Y",
			"access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTUwOTk3ODIyLCJqdGkiOiI5MGM4ZTgwNDk5NDU0MTA1OGIwODY4NDI3NDA4YWEzYiIsInVzZXJfaWQiOiIyODlkODdkZi1jZGRlLTQ4ZDMtODkzNy1kYmUyMTlhNWFhM2QifQ.15OEc4P8W5ZbQRSadN9XeQLdH22O-Ly7Wdc115MRQXI"
		}
	}
	```
	"""
	serializer_class = SubscriberAuthSerializer


class InstructorLoginAPIView(LoginViewBase):
	"""
	#### Response:
	```
	{
		"code": 1003,
		"msg": "Login authentication is successful",
		"data": {
			"refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTU1MTA4MzkyMiwianRpIjoiMDBiMGFhMWM0NjEwNDAyMDkzMGUxZTY4YzFhMmQ2ZTEiLCJ1c2VyX2lkIjoiMjg5ZDg3ZGYtY2RkZS00OGQzLTg5MzctZGJlMjE5YTVhYTNkIn0.M2kAaTGOLsHmbM6f9TRGxk27Pa7BFiWpAnXjf0Mhc-Y",
			"access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTUwOTk3ODIyLCJqdGkiOiI5MGM4ZTgwNDk5NDU0MTA1OGIwODY4NDI3NDA4YWEzYiIsInVzZXJfaWQiOiIyODlkODdkZi1jZGRlLTQ4ZDMtODkzNy1kYmUyMTlhNWFhM2QifQ.15OEc4P8W5ZbQRSadN9XeQLdH22O-Ly7Wdc115MRQXI"
		}
	}
	```
	"""
	serializer_class = InstructorAuthSerializer


class AdminLoginAPIView(LoginViewBase):
	"""
	#### Response:
	```
	{
		"code": 1003,
		"msg": "Login authentication is successful",
		"data": {
			"refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTU1MTA4MzkyMiwianRpIjoiMDBiMGFhMWM0NjEwNDAyMDkzMGUxZTY4YzFhMmQ2ZTEiLCJ1c2VyX2lkIjoiMjg5ZDg3ZGYtY2RkZS00OGQzLTg5MzctZGJlMjE5YTVhYTNkIn0.M2kAaTGOLsHmbM6f9TRGxk27Pa7BFiWpAnXjf0Mhc-Y",
			"access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTUwOTk3ODIyLCJqdGkiOiI5MGM4ZTgwNDk5NDU0MTA1OGIwODY4NDI3NDA4YWEzYiIsInVzZXJfaWQiOiIyODlkODdkZi1jZGRlLTQ4ZDMtODkzNy1kYmUyMTlhNWFhM2QifQ.15OEc4P8W5ZbQRSadN9XeQLdH22O-Ly7Wdc115MRQXI"
		}
	}
	```
	"""
	serializer_class = AdminAuthSerializer


class RefreshTokenAPIView(LoginViewBase):
	"""
	{
		"code": 1003,
		"msg": "Login authentication is successful",
		"data": {
			"access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTUxMDAwMzkxLCJqdGkiOiJmOGIxYTkwMTNjYTk0NWQ5YjNlMDNlMzYwMzQ3ZDg5YSIsInVzZXJfaWQiOiIyODlkODdkZi1jZGRlLTQ4ZDMtODkzNy1kYmUyMTlhNWFhM2QifQ.pcyhnjb9mapgul0aJKWsRekzhC26ZBe-UBqzOPwzQoU"
		}
	}
	"""
	serializer_class = TokenRefreshSerializer


class UserDetailApiView(APIView):
	permission_classes = (IsAuthenticated,)
	serializer_class = UserDetailSerializer

	def get(self, request, *args, **kwargs):
		"""
		# Response (Success)
		'''
		{
		    "data": {
		        "id": "51fb2581-7c14-459d-9f3b-0ed593cbeb0f",
		        "first_name": gaurav,
		        "last_name": saini,
		        "email": "gauravsaini793@gmail.com",
		        "profile": {
		            "country": "INDIA",
		            "date_of_birth": "1993-03-04",
		            "organization": "XYZ",
		            "mobile": "123456789",
		            "address": "YNR",
		            "city": "YNR",
		            "pincode": "123567"
		        }
		    },
		    "code": 2000,
		    "msg": "Request processed successfully"
		}
		'''
		# Response(Error)
		'''
		{
		    "code": "token_not_valid",
		    "messages": [
		        {
		            "token_type": "access",
		            "message": "Token is invalid or expired",
		            "token_class": "AccessToken"
		        }
		    ],
		    "detail": "Given token not valid for any token type"
		}
		'''
		"""
		serializer = self.serializer_class(request.user)
		return Response(
				res_codes.get_response_dict(
					res_codes.SUCCESS,
					serializer.data,
				),
				status=status.HTTP_200_OK,
			)

	def patch(self, request, *args, **kwargs):
		"""
		#Request(Body)
		```
		{
			"first_name": "golu",
			"last_name": "saini",
			"email": "gauravsaini793@gmail.com",
			"profile": {
			    "country": "INDIA",
			    "date_of_birth": "1993-03-04",
			    "organization": "XYZ",
			}
		}
		```
		#Response(Success)
		```
		{
		    "code": 1006,
		    "data": {
		        "id": "51fb2581-7c14-459d-9f3b-0ed593cbeb0f",
		        "first_name": "golu",
		        "last_name": "saini",
		        "email": "gauravsaini793@gmail.com",
		        "profile": {
		            "country": "INDIA",
		            "date_of_birth": "1993-03-04",
		            "organization": "XYZ",
		        }
		    },
		    "msg": "User detail updated successfully."
		}
		```
		#### Response (error):
		```
		{
		    "code": "token_not_valid",
		    "messages": [
		        {
		            "token_type": "access",
		            "message": "Token is invalid or expired",
		            "token_class": "AccessToken"
		        }
		    ],
		    "detail": "Given token not valid for any token type"
		}
		```
		"""
		serializer = UserCreateSerializer(
			request.user,
			data=request.data,
			partial=True,
		)
		if serializer.is_valid():
			serializer.save()
			return Response(
				res_codes.get_response_dict(
					res_codes.USER_PROFILE_UPDATED,
					serializer.data,
				),
				status=status.HTTP_200_OK,
			)
		return Response(
			res_codes.get_response_dict(
				res_codes.INVALID_POST_DATA,
				serializer.errors
			),
			status=status.HTTP_400_BAD_REQUEST
		)


class UserListApiView(APIView):
	permissions = (IsAuthenticated, IsAdmin,)
	serializer_class = UserListSerializer

	def get(self, request, *args, **kwargs):
		"""
		#Response
		{
		    "data": [
		        {
		            "id": "80d55bf3-af57-41b5-aa85-ba0aee152878",
		            "first_name": "test user",
		            "last_name": "last",
		            "email": "test@gmail.com"
		        }
		    ],
		    "code": 2000,
		    "msg": "Request processed successfully"
		}
		"""
		users = User.objects.filter(is_staff=False)
		serializer = self.serializer_class(
			users,
			many=True)
		return Response(
			res_codes.get_response_dict(
				res_codes.SUCCESS,
				serializer.data,
			),
			status=status.HTTP_200_OK,
		)


class PasswordResetApiView(APIView):
	permissions = (IsAuthenticated,)
	serializer_class = ChangePasswordSerializer

	def put(self, request, *args, **kwargs):
		"""
		# Response (Success)
		'''
		{
		    "code": 1005,
		    "msg": "Password updated successfully."
		}
		'''
		# Response(Error)
		'''
		{
		    "msg": "Invalid post data provided",
		    "code": 1000,
		    "data": {
		        "password": {
		            "msg": "Wrong password supplied.",
		            "code": "1004"
		        }
		    }
		}
		'''
		# Response(Error)
		'''
		{
		    "code": "token_not_valid",
		    "messages": [
		        {
		            "token_type": "access",
		            "message": "Token is invalid or expired",
		            "token_class": "AccessToken"
		        }
		    ],
		    "detail": "Given token not valid for any token type"
		}
		'''
		"""
		data = request.data.copy()
		serializer = self.serializer_class(
			request.user,
			data=data
			)
		if serializer.is_valid():
			serializer.save()
			return Response(
				res_codes.get_response_dict(
					res_codes.PASSWORD_UPDATE_SUCCESS,
				),
				status=status.HTTP_200_OK,
			)
		return Response(
			res_codes.get_response_dict(
				res_codes.INVALID_POST_DATA,
				serializer.errors
			),
			status=status.HTTP_400_BAD_REQUEST
		)
