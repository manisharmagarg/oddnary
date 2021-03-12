# restframework imports
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
#djnago imports
from django.conf import settings
from django.contrib.auth import get_user_model
from .serializers import (
	UserCourseListSerializer,
	AddCouserInMyCoursesSerializer,
	UserCategoryCourseDetailSerializer,
)
from courses.models import (
	Course,
	UserMyCourseLibrary,
	Category,
)
from utils import res_codes

User = get_user_model()


class UserCourseListAPIView(APIView):
	permission_classes = (IsAuthenticated,)
	serializer_class = UserCourseListSerializer

	def get(self, request, format=None):
		"""
		{
		    "msg": "Request processed successfully",
		    "data": [
		        {
		            "name": "AI",
		            "description": "Learn AI",
		            "is_active": true
		        },
		        {
		            "name": "ML",
		            "description": "Learn ML",
		            "is_active": false
		        },
		    ],
		    "code": 2000
		}
		# Response(Error)
		```
		{
		    "detail": "Given token not valid for any token type",
		    "messages": [
		        {
		            "token_type": "access",
		            "token_class": "AccessToken",
		            "message": "Token is invalid or expired"
		        }
		    ],
		    "code": "token_not_valid"
		}
		```
		"""

		user_courses = Course.objects.filter(
			author=request.user
			)
		serializer = self.serializer_class(
				user_courses,
				many=True
			)
		return Response(
				res_codes.get_response_dict(
					res_codes.SUCCESS,
					serializer.data,
				),
				status=status.HTTP_200_OK,
			)


class UserCourseDetailAPIView(APIView):
	"""
	Retrieve, update or delete a course instance.
	"""
	permission_classes = (IsAuthenticated,)
	serializer_class = UserCourseListSerializer

	def get_object(self):
		try:
			return Course.objects.get(
				pk=self.kwargs.get('pk'),
				author=self.request.user
				)
		except Course.DoesNotExist:
			return None

	def get(self, request, *args, **kwargs):
		"""
		#Response
		```
		{
		    "data": {
		        "name": "AI",
		        "description": "Learn AI",
		        "is_active": false
		    },
		    "code": 2000,
		    "msg": "Request processed successfully"
		}
		```
		# Response(Error if wrong pk provide or unrelated course)
		```
		{
		    "code": 3016,
		    "msg": "Course Not found for this user"
		}
		"""
		course = self.get_object()
		if course:
			serializer = self.serializer_class(course)
			return Response(
					res_codes.get_response_dict(
						res_codes.SUCCESS,
						serializer.data,
					),
					status=status.HTTP_200_OK,
				)			
		return Response(
					res_codes.get_response_dict(
						res_codes.COURSE_NOT_FOUND_FOR_USER
					),
					status=status.HTTP_400_BAD_REQUEST
				)


class AddCourseInMyCoursesAPIView(APIView):
	permission_classes = (IsAuthenticated,)
	serializer_class = AddCouserInMyCoursesSerializer

	def post(self, request, *args, **kwargs):
		"""
		# Response(Success)
		```
		{
		    "data": {
		        "course": "a26077a9-9a40-4f35-87a6-d5828c46baf6"
		    },
		    "msg": "Course added to library successfully",
		    "code": 3017
		}
		```
		# Response(Error)
		```
		{
		    "data": {
		        "course": [
		            "This field may not be null."
		        ]
		    },
		    "code": 1000,
		    "msg": "Invalid post data provided"
		}
		```
		# Response(Error)
		```
		{
		    "detail": "Given token not valid for any token type",
		    "code": "token_not_valid",
		    "messages": [
		        {
		            "token_class": "AccessToken",
		            "message": "Token is invalid or expired",
		            "token_type": "access"
		        }
		    ]
		}
		```
		"""
		data = request.data.copy()
		serializer = self.serializer_class(data=data)
		if serializer.is_valid():
			course = serializer.save(user=request.user)
			return Response(
				res_codes.get_response_dict(
					res_codes.USER_ADDED_COURSE,
					serializer.data,
				),
				status=status.HTTP_201_CREATED,
			)
		return Response(
			res_codes.get_response_dict(
				res_codes.INVALID_POST_DATA,
				serializer.errors,
			)
		)


class DeleteCourseFromMyCoursesAPIView(APIView):
	permission_classes = (IsAuthenticated,)

	def get_object(self):
		try:
			return UserMyCourseLibrary.objects.get(
				pk=self.kwargs.get('pk'),
				user=self.request.user
				)
		except UserMyCourseLibrary.DoesNotExist:
			return None

	def delete(self, request, *args, **kwargs):
		"""
		# Response(Success)
		```
		{
		    "msg": "Course removed successfully from library",
		    "code": 3018
		}
		```
		# Response(Error with wrong pk or invalid user)
		```
		{
		    "msg": "Course Not found for this user",
		    "code": 3016
		}
		```
		# Response(Error)
		```
		{
		    "detail": "Given token not valid for any token type",
		    "code": "token_not_valid",
		    "messages": [
		        {
		            "token_class": "AccessToken",
		            "message": "Token is invalid or expired",
		            "token_type": "access"
		        }
		    ]
		}
		```
		"""
		my_course = self.get_object(pk, request.user)
		if my_course:
			my_course.delete()
			return Response(
				res_codes.get_response_dict(
					res_codes.USER_DELETED_COURSE
				),
				status=status.HTTP_204_NO_CONTENT
			)
		return Response(
			res_codes.get_response_dict(
				res_codes.COURSE_NOT_FOUND_FOR_USER
			),
			status=status.HTTP_400_BAD_REQUEST
		)


class UserCategoryCourseFullDetailApiView(APIView):
	"""
	To list all the available categories with courses
	"""
	permission_classes = (IsAuthenticated,)
	serializer_class = UserCategoryCourseDetailSerializer

	def get(self, request, *args, **kwargs):
		"""
		# Response(Success)
		``` 
		{
		    "msg": "Request processed successfully",
		    "code": 2000,
		    "data": [
		        {
		            "id": "902f4bda-4cbe-4a71-bec3-c767f02b8ae6",
		            "name": "test cat",
		            "description": "test",
		            "courses": [
		                {
		                    "id": "a745601c-4b17-4608-973f-1043bb5774d9",
		                    "course": {
		                        "name": "AI 22",
		                        "description": "Learn AI",
		                        "is_active": true
		                    }
		                },
		                {
		                    "id": "42483d01-dc6b-4cce-992d-6bb214f8bed0",
		                    "course": {
		                        "name": "AI 22",
		                        "description": "Learn AI",
		                        "is_active": true
		                    }
		                }
		            ]
		        },
		        {
		            "id": "6829f57f-084f-4930-97e7-117899b9e55d",
		            "name": "teyst",
		            "description": "desc",
		            "courses": [
		                {
		                    "id": "ed35ba0d-51a1-4336-a0d9-5f904a940f61",
		                    "course": {
		                        "name": "AI 22",
		                        "description": "Learn AI",
		                        "is_active": true
		                    }
		                }
		            ]
		        }
		    ]
		}
		```
		"""
		categories = Category.objects.all()
		serializer = self.serializer_class(
			categories,
			many=True
		)
		return Response(
			res_codes.get_response_dict(
				res_codes.SUCCESS,
				serializer.data,
			),
			status=status.HTTP_200_OK,
		)


class UserCategoryCourseDetailApiView(APIView):
	"""
	To get detail of particular category with courses
	"""
	permission_classes = (IsAuthenticated,)
	serializer_class = UserCategoryCourseDetailSerializer

	def get_object(self):
		try:
			category = Category.objects.get(
				id=self.kwargs.get('pk'),
			)
		except Category.DoesNotExist:
			raise NotFound(
				res_codes.get_response_dict(
					res_codes.NOT_FOUND
				)
			)
		return category

	def get(self, request, *args, **kwargs):
		"""
		# Response(Success)
		``` 
		{
		    "msg": "Request processed successfully",
		    "data": {
		        "id": "902f4bda-4cbe-4a71-bec3-c767f02b8ae6",
		        "name": "test cat",
		        "description": "test",
		        "courses": [
		            {
		                "id": "a745601c-4b17-4608-973f-1043bb5774d9",
		                "course": {
		                    "name": "AI 22",
		                    "description": "Learn AI",
		                    "is_active": true
		                }
		            },
		            {
		                "id": "42483d01-dc6b-4cce-992d-6bb214f8bed0",
		                "course": {
		                    "name": "AI 22",
		                    "description": "Learn AI",
		                    "is_active": true
		                }
		            }
		        ]
		    },
		    "code": 2000
		}
		```
		"""
		category = self.get_object()
		serializer = self.serializer_class(category)
		return Response(
			res_codes.get_response_dict(
				res_codes.SUCCESS,
				serializer.data,
			),
			status=status.HTTP_200_OK,
		)