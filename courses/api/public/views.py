# restframework imports
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.exceptions import (
	NotFound,
)
#djnago imports
from django.conf import settings
from django.contrib.auth import get_user_model
from .serializers import (
	PublicCourseListSerializer,
	PublicCourseDetailSerializer,
	PublicCategoryCourseDetailSerializer,
)
from courses.models import (
	Course,
	CourseDetailTab,
	Category,
)
from utils import res_codes


class PublicCourseListAPIView(APIView):
	serializer_class = PublicCourseListSerializer

	def get(self, request, format=None):
		"""
		#Response
		```
		{
			"code": 2000,
		    "msg": "Request processed successfully",
		    "data": [
		        {
					"id": "63ce453a-2327-40ab-9a50-b5db46e88234",
		            "name": "NN",
		            "description": "Learn NN"
		        },
		        {
					"id": "63ce453a-2327-40ab-9a50-b5db46e88234",
		            "name": "AI",
		            "description": "Learn AI"
		        }
		    ]
		}
		```
		"""

		courses = Course.objects.filter(is_active=True, is_deleted=False)
		serializer = self.serializer_class(
				courses,
				many=True
			)
		return Response(
				res_codes.get_response_dict(
					res_codes.SUCCESS,
					serializer.data,
				),
				status=status.HTTP_200_OK,
			)


class PublicCourseDetailAPIView(APIView):
	serializer_class = PublicCourseDetailSerializer

	def get_object(self):
		try:
			course = Course.objects.get(
				id=self.kwargs.get('pk'),
				is_active=True,
				is_deleted=False,
			)
		except Course.DoesNotExist:
			raise NotFound(
				res_codes.get_response_dict(
					res_codes.NOT_FOUND
				)
			)
		return course

	def get(self, request, *args, **kwargs):
		"""
		### Response
		```
		{
			"code": 2000,
			"msg": "Request processed successfully",
			"data": {
				"id": "63ce453a-2327-40ab-9a50-b5db46e88234",
				"name": "sdfds",
				"description": "",
				"tabs": [
					{
						"name": "certification",
						"content": "dfsdfsldkflksdf;s",
						"index": 0,
						"lists": [
							{
								"content": "slslslslslslsls",
								"index": 0
							}
						]
					}
				]
			}
		}
		```
		"""
		course = self.get_object()
		serializer = self.serializer_class(course)
		return Response(
				res_codes.get_response_dict(
					res_codes.SUCCESS,
					serializer.data,
				),
				status=status.HTTP_200_OK,
			)


class PublicCategoryCourseFullDetailApiView(APIView):
	"""
	To list all the available categories with courses
	"""
	serializer_class = PublicCategoryCourseDetailSerializer

	def get(self, request, *args, **kwargs):
		"""
		# Response(Success)
		``` 
		{
		    "code": 2000,
		    "msg": "Request processed successfully",
		    "data": [
		        {
		            "id": "902f4bda-4cbe-4a71-bec3-c767f02b8ae6",
		            "name": "test cat",
		            "description": "test",
		            "courses": [
		                {
		                    "id": "a745601c-4b17-4608-973f-1043bb5774d9",
		                    "course": {
		                        "id": "9a7657b2-55c7-4e45-859f-dbc9e4738061",
		                        "name": "AI 22",
		                        "description": "Learn AI"
		                    }
		                },
		                {
		                    "id": "42483d01-dc6b-4cce-992d-6bb214f8bed0",
		                    "course": {
		                        "id": "e0344bb0-b6d3-4ce3-a0ed-2873179f4e15",
		                        "name": "AI 22",
		                        "description": "Learn AI"
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
		                        "id": "a391fce2-bb39-47bf-abe1-6209cfcc06a4",
		                        "name": "AI 22",
		                        "description": "Learn AI"
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


class PublicCategoryCourseDetailApiView(APIView):
	"""
	To get detail of particular category with courses
	"""
	serializer_class = PublicCategoryCourseDetailSerializer

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
		    "code": 2000,
		    "data": {
		        "id": "902f4bda-4cbe-4a71-bec3-c767f02b8ae6",
		        "name": "test cat",
		        "description": "test",
		        "courses": [
		            {
		                "id": "a745601c-4b17-4608-973f-1043bb5774d9",
		                "course": {
		                    "id": "9a7657b2-55c7-4e45-859f-dbc9e4738061",
		                    "name": "AI 22",
		                    "description": "Learn AI"
		                }
		            },
		            {
		                "id": "42483d01-dc6b-4cce-992d-6bb214f8bed0",
		                "course": {
		                    "id": "e0344bb0-b6d3-4ce3-a0ed-2873179f4e15",
		                    "name": "AI 22",
		                    "description": "Learn AI"
		                }
		            }
		        ]
		    },
		    "msg": "Request processed successfully"
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