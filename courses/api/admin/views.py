# restframework imports
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
#djnago imports
from django.conf import settings
from django.contrib.auth import get_user_model
from .serializers import (
	CourseCreateSerializer,
	CourseSerializer,
	CourseSectionCreateSerializer,
	CourseSectionSerializer,
	CourseFileCreateSerializer,
	CourseFileSerializer,
	CoursesDetailSerializer,
	CourseDetailTabCreateSerializer,
	CourseDetailTabSerializer,
	CourseDetailTabListCreateSerializer,
	CourseDetailTabListDetailSerializer,
	CoursesFullDetailSerializer,
	CategoryCreateSerializer,
	CategoryCourseCreateSerializer,
	CategoryCourseRelationSerializer,
	CategoryCourseUpdateSerializer,
)
from courses.models import (
	Course,
	CourseSection,
	CourseFile,
	CourseDetailTab,
	CourseDetailTabList,
	Category,
	CategoryCourseRelation,
)
from utils.permissions import IsAdmin

from utils import res_codes

User = get_user_model()


class CourseCreateListAPIView(APIView):
	permission_classes = (IsAuthenticated, IsAdmin)
	serializer_class = CourseCreateSerializer

	def post(self, request, *args, **kwargs):
		"""
		### Body:
		```
		{
		    "name": "AI",
		    "description": "Learn AI",
		    "category": "902f4bda-4cbe-4a71-bec3-c767f02b8ae6",
		    "is_active": true   // this field is optional
		}
		```

		#### Response (success):
		```
		{
			"code": 3000,
			"msg": "Course created successfully",
			"data": {
				"id": "ff068528-cf3d-43a2-b695-bd788d5da2c4",
				"author": {
					"id": "289d87df-cdde-48d3-8937-dbe219a5aa3d",
					"first_name": null,
					"last_name": null,
					"email": "admin@yopmail.com"
				},
				"name": "some random course 1",
				"description": "desc",
				"is_active": false
			}
		}
		```

		#### Response (error):
		```
		{
		    "data": {
		        "name": [
		            "This field may not be blank."
		        ],
		        "description": [
		            "This field may not be blank."
		        ]
		    },
		    "code": 1000,
		    "msg": "Invalid post data provided"
		}
		```
		```
		#### Response(error):
		{
		    "data": {
		        "category": "This field can't be null."
		    },
		    "msg": "Invalid post data provided",
		    "code": 1000
		}
		```
		### Response(error):
		{
		    "msg": "Invalid post data provided",
		    "code": 1000,
		    "data": {
		        "category": "Such category does not exists."
		    }
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
		data = request.data.copy()
		try:
			category_id = data['category']
		except:
			category_id = None
		if category_id:
			try:
				category = Category.objects.get(id=category_id)
			except (Category.DoesNotExist, Exception):
				category_error = {
					'category': 'Such category does not exists.'
				}
				return Response(
					res_codes.get_response_dict(
						res_codes.INVALID_POST_DATA,
						category_error,
					),
					status=status.HTTP_400_BAD_REQUEST
				)
		
		else:
			category_error = {
				'category': "This field can't be null."
			}
			return Response(
				res_codes.get_response_dict(
					res_codes.INVALID_POST_DATA,
					category_error,
				),
				status=status.HTTP_400_BAD_REQUEST
			)
		serializer = self.serializer_class(data=data)
		if serializer.is_valid():
			course = serializer.save(author=request.user)
			try:
				CategoryCourseRelation.objects.create(
					course=course,
					category=category
				)
			except:
				pass
				
			return Response(
				res_codes.get_response_dict(
					res_codes.COURSE_CREATED,
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


	def get(self, request, format=None):
		"""
		{
			"code": 2000,
			"msg": "Request processed successfully",
			"data": [
				{
					"id": "63ce453a-2327-40ab-9a50-b5db46e88234",
					"author": {
						"id": "c29aa927-2bf2-44c8-9b01-b868b63dfc80",
						"first_name": null,
						"last_name": null,
						"email": "vivek@gmail.com"
					},
					"name": "sdfds",
					"description": "",
					"is_active": true,
					"is_deleted": true
				}
			]
		}
		"""
		courses = Course.objects.all()
		serializer = CourseSerializer(
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


class CourseUpdateApiView(APIView):
	"""
	Retrieve, update or delete a course instance.
	"""
	permission_classes = (IsAuthenticated, IsAdmin)
	serializer_class = CourseSerializer

	def get_object(self):
		try:
			return Course.objects.get(pk=self.kwargs.get('pk'))
		except Course.DoesNotExist:
			return None

	def get(self, request, *args, **kwargs):
		"""
		#Response
		```
		{
		    "data": {
		        "id": "a26077a9-9a40-4f35-87a6-d5828c46baf6",
		        "author": {
		            "id": "bbc34100-0870-493c-a5ea-2a6d72977ddc",
		            "first_name": "golu",
		            "last_name": "saini",
		            "email": "gauravsaini793@gmail.com"
		        },
		        "name": "AI course update",
		        "description": "Learn AI Course",
		        "is_active": true,
		        "is_deleted": false
		    },
		    "code": 2000,
		    "msg": "Request processed successfully"
		}
		```
		# Response(Error)
		```
		{
		    "code": 4000,
		    "msg": "Such pk not found"
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
				res_codes.PK_NOT_FOUND
			),
			status=status.HTTP_400_BAD_REQUEST
		)

	def patch(self, request, *args, **kwargs):
		"""
		#Request(Body)
		```
		{
		    "author": "0f75a7e7-321f-4691-ac26-2de6fafe2ee1",
		    "name": "AI",
		    "description": "Learn AI",
		    "is_active": false
		}
		```
		#Response(Success)
		```
		{
		    "data": {
		        "id": "a26077a9-9a40-4f35-87a6-d5828c46baf6",
		        "author": {
		            "id": "bbc34100-0870-493c-a5ea-2a6d72977ddc",
		            "first_name": "golu",
		            "last_name": "saini",
		            "email": "gauravsaini793@gmail.com"
		        },
		        "name": "AI course update",
		        "description": "Learn AI Course",
		        "is_active": true,
		        "is_deleted": false
		    },
		    "code": 3001,
		    "msg": "Course updated successfully"
		}
		```
		# Response(Error)
		```
		{
		    "author": [
		        "'0f75a7e7-321f-4691-ac26-2de6fafe1' is not a valid UUID."
		    ]
		}
		```
		# Response(Error)
		```
		{
		    "code": 4000,
		    "msg": "Such pk not found"
		}
		```
		"""
		course = self.get_object()
		if course:
			serializer = self.serializer_class(
				course,
				data=request.data,
				partial=True,
			)
			if serializer.is_valid():
				serializer.save()
				return Response(
						res_codes.get_response_dict(
							res_codes.COURSE_UPDATED,
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
		return Response(
			res_codes.get_response_dict(
				res_codes.PK_NOT_FOUND
			),
			status=status.HTTP_400_BAD_REQUEST
		)

	def delete(self, request, *args, **kwargs):
		"""
		#Response(Success)
		{
		    "code": 3002,
		    "msg": "Course deleted successfully"
		}
		# Response(Error)
		```
		{
		    "msg": "Such pk not found",
		    "code": 4000
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
		course = self.get_object()
		if course:
			course.is_active = False
			course.is_deleted = True
			course.save()
			return Response(
						res_codes.get_response_dict(
							res_codes.COURSE_DELETED
						),
						status=status.HTTP_204_NO_CONTENT
					)
		return Response(
					res_codes.get_response_dict(
						res_codes.PK_NOT_FOUND
					),
					status=status.HTTP_400_BAD_REQUEST
				)


class CourseSectionCreateApiView(APIView):
	permission_classes = (IsAuthenticated, IsAdmin)
	serializer_class = CourseSectionCreateSerializer
	queryset = CourseSection.objects.all()

	def post(self, request, *args, **kwargs):
		"""
		### Body:
		```
		{
			"course": "4dd35b89-3261-4c5a-b022-cd84b5676949",
			"name": "AI",
			"index": "3"
		}
		```
		#### Response (success):
		```
		{
			"data": {
				"course": "4dd35b89-3261-4c5a-b022-cd84b5676949",
				"name": "AI",
				"index": 3
			},
			"code": 3004,
			"msg": "Course Section created successfully"
		}
		```
		#### Response (error):
		```
		{
			"data": {
				"index": [
				    "A valid integer is required."
				],
				"name": [
				    "This field may not be blank."
				],
				"course": [
				    "This field may not be null."
				]
			},
			"code": 1000,
			"msg": "Invalid post data provided"
		}
		```
		#### Response (error):
		```
		{
		    "code": 1000,
		    "data": {
		        "course": [
		            "'4dd35b89-3261-4c5a-b022-cd84b5676948' is not a valid UUID."
		        ]
		    },
		    "msg": "Invalid post data provided"
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
		data = request.data.copy()
		serializer = self.serializer_class(data=data)
		if serializer.is_valid():
			serializer.save()
			return Response(
				res_codes.get_response_dict(
					res_codes.COURSE_SECTION_CREATED,
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


class CourseSectionListAPIView(APIView):
	"""
	List all the available course sections
	"""
	permission_classes = (IsAuthenticated, IsAdmin)
	serializer_class = CourseSectionSerializer

	def get(self, request, format=None):
		"""
		#Response
		{
		    "code": 2000,
		    "data": [
		        {
		            "course": "8b30e0cc-e70e-48f8-a0ec-245c6134fb45",
		            "name": "Test Course1",
		            "index": 0,
		            "is_active": false
		        },
		        {
		            "course": "8b30e0cc-e70e-48f8-a0ec-245c6134fb45",
		            "name": "Course2",
		            "index": 3,
		            "is_active": false
		        }
		    ],
		    "msg": "Request processed successfully"
		}
		"""
		course_sections = CourseSection.objects.all()
		serializer = self.serializer_class(
				course_sections,
				many=True
			)
		return Response(
				res_codes.get_response_dict(
					res_codes.SUCCESS,
					serializer.data,
				),
				status=status.HTTP_200_OK,
			)


class CourseSectionUpdateApiView(APIView):
	"""
	Retrieve, update or delete a course section instance.
	"""
	permission_classes = (IsAuthenticated, IsAdmin)
	serializer_class = CourseSectionSerializer

	def get_object(self):
		try:
			return CourseSection.objects.get(pk=self.kwargs.get('pk'))
		except CourseSection.DoesNotExist:
			return None

	def get(self, request, *args, **kwargs):
		"""
		# Response(Success)
		``` 
		{
		    "code": 2000,
		    "data": {
		        "id": "c4cd2d9d-277e-439f-8958-1a1a6f1be62e",
		        "course": {
		            "id": "8b30e0cc-e70e-48f8-a0ec-245c6134fb45",
		            "author": {
		                "id": "0f75a7e7-321f-4691-ac26-2de6fafe2ee1",
		                "first_name": null,
		                "last_name": null,
		                "email": "testuser@gmail.com"
		            },
		            "name": "fdgdf",
		            "description": "",
		            "is_active": true,
		            "is_deleted": false
		        },
		        "name": "Test Section",
		        "index": 0,
		        "is_active": false
		    },
		    "msg": "Request processed successfully"
		}
		```
		# Response(Error)
		```
		{
		    "msg": "Such pk not found",
		    "code": 4000
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

		course_section = self.get_object()
		if course_section:
			serializer = self.serializer_class(course_section)
			return Response(
				res_codes.get_response_dict(
					res_codes.SUCCESS,
					serializer.data,
				),
				status=status.HTTP_200_OK,
			)
		return Response(
				res_codes.get_response_dict(
					res_codes.PK_NOT_FOUND
				),
				status=status.HTTP_400_BAD_REQUEST
			)

	def patch(self, request, *args, **kwargs):
		"""
		#Request(Body)
		```
		{
		    "course": "8b30e0cc-e70e-48f8-a0ec-245c6134fb45",
		    "name": "AI",
		    "index": 3,
		    "is_active": false
		}
		```
		#Response(Success)
		```
		{
		    "msg": "Course Section updated successfully",
		    "code": 3005,
		    "data": {
		        "id": "c4cd2d9d-277e-439f-8958-1a1a6f1be62e",
		        "course": {
		            "id": "8b30e0cc-e70e-48f8-a0ec-245c6134fb45",
		            "author": {
		                "id": "0f75a7e7-321f-4691-ac26-2de6fafe2ee1",
		                "first_name": null,
		                "last_name": null,
		                "email": "testuser@gmail.com"
		            },
		            "name": "fdgdf",
		            "description": "",
		            "is_active": true,
		            "is_deleted": false
		        },
		        "name": "AI Course",
		        "index": 3,
		        "is_active": false
		    }
		}
		```
		# Response(Error)
		```
		{
		    "data": {
		        "course": [
		            "Invalid pk \"8b30e0cc-e70e-48f8-a0ec-245c6134fb74\" - object does not exist."
		        ]
		    },
		    "code": 1000,
		    "msg": "Invalid post data provided"
		}
		```
		# Response(Error)
		```
		{
		    "msg": "Such pk not found",
		    "code": 4000
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
		course_section = self.get_object()
		if course_section:
			serializer = self.serializer_class(
				course_section,
				data=request.data,
				partial=True,
			)
			if serializer.is_valid():
				serializer.save()
				return Response(
					res_codes.get_response_dict(
						res_codes.COURSE_SECTION_UPDATED,
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
		return Response(
			res_codes.get_response_dict(
				res_codes.PK_NOT_FOUND
			),
			status=status.HTTP_400_BAD_REQUEST
		)

	def delete(self, request, *args, **kwargs):
		"""
		#Response(Success)
		{
		    "msg": "Course Section deleted successfully",
		    "code": 3006
		}
		# Response(Error)
		```
		{
		    "msg": "Such pk not found",
		    "code": 4000
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
		course_section = self.get_object()
		if course_section:
			course_section.is_active = False
			course_section.is_deleted = True
			course_section.save()
			return Response(
				res_codes.get_response_dict(
					res_codes.COURSE_SECTION_DELETED
				),
				status=status.HTTP_204_NO_CONTENT,
			)
		return Response(
			res_codes.get_response_dict(
				res_codes.PK_NOT_FOUND
			),
			status=status.HTTP_400_BAD_REQUEST
		)


class CourseFileCreateAPIView(APIView):
	permission_classes = (IsAuthenticated, IsAdmin)
	serializer_class = CourseFileCreateSerializer

	def post(self, request, *args, **kwargs):
		"""
		### Body:
		```
		{
			"section": "c4cd2d9d-277e-439f-8958-1a1a6f1be62e",
			"name": "AI File",
			"description": "File Learn AI",
			"file": "/media/8b30e0cc-e70e-48f8-a0ec-245c6134fb45/c4cd2d9d-277e-439f-8958-1a1a6f1be62e/969047d8-5ec0-413b-8b81-71cd938568f3/AI_file.py",
			"index":3,
		    "is_active": true    # this field is optional
		}
		```
		#### Response (success):
		```
		{
		    "data": {
		        "section": "c4cd2d9d-277e-439f-8958-1a1a6f1be62e",
		        "name": "AI File",
		        "description": "File Learn AI",
		        "file": "/media/8b30e0cc-e70e-48f8-a0ec-245c6134fb45/c4cd2d9d-277e-439f-8958-1a1a6f1be62e/969047d8-5ec0-413b-8b81-71cd938568f3/AI_file.py",
		        "index": 3,
		        "is_active": true
		    },
		    "msg": "Course Section File saved successfully",
		    "code": 3007
		}
		```
		#### Response (error):
		```
		{
		    "data": {
		        "file": [
		            "No file was submitted."
		        ],
		        "name": [
		            "This field may not be blank."
		        ],
		        "section": [
		            "This field may not be null."
		        ],
		        "description": [
		            "This field may not be blank."
		        ],
		        "index": [
		            "A valid integer is required."
		        ]
		    },
		    "msg": "Invalid post data provided",
		    "code": 1000
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
		data = request.data.copy()
		serializer = self.serializer_class(data=data)
		if serializer.is_valid():
			serializer.save()
			return Response(
				res_codes.get_response_dict(
					res_codes.COURSE_SECTION_FILE_CREATED,
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


class CourseFileUpdateAPIView(APIView):
	"""
	Retrieve, update or delete a course file instance.
	"""
	permission_classes = (IsAuthenticated, IsAdmin)
	serializer_class = CourseFileSerializer

	def get_object(self):
		try:
			return CourseFile.objects.get(pk=self.kwargs.get('pk'))
		except CourseFile.DoesNotExist:
			return None

	def get(self, request, *args, **kwargs):
		"""
		# Response(Success)
		``` 
		{
		    "code": 2000,
		    "msg": "Request processed successfully",
		    "data": {
		        "id": "5b8b1e7e-e037-4da1-a630-5e3d97ceb294",
		        "section": {
		            "id": "c4cd2d9d-277e-439f-8958-1a1a6f1be62e",
		            "course": {
		                "id": "8b30e0cc-e70e-48f8-a0ec-245c6134fb45",
		                "author": {
		                    "id": "0f75a7e7-321f-4691-ac26-2de6fafe2ee1",
		                    "first_name": null,
		                    "last_name": null,
		                    "email": "testuser@gmail.com"
		                },
		                "name": "fdgdf",
		                "description": "",
		                "is_active": true,
		                "is_deleted": false
		            },
		            "name": "AI Courses",
		            "index": 3,
		            "is_active": false
		        },
		        "name": "AI",
		        "description": "Test",
		        "file": "/media/8b30e0cc-e70e-48f8-a0ec-245c6134fb45/c4cd2d9d-277e-439f-8958-1a1a6f1be62e/5b8b1e7e-e037-4da1-a630-5e3d97ceb294/import_data.html",
		        "index": 5,
		        "is_active": false
		    }
		}
		```
		# Response(Error)
		```
		{
		    "msg": "Such pk not found",
		    "code": 4000
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

		course_file = self.get_object()
		if course_file:
			serializer = self.serializer_class(course_file)
			return Response(
				res_codes.get_response_dict(
					res_codes.SUCCESS,
					serializer.data,
				),
				status=status.HTTP_200_OK,
			)
		return Response(
				res_codes.get_response_dict(
					res_codes.PK_NOT_FOUND
				),
				status=status.HTTP_400_BAD_REQUEST
			)

	def patch(self, request, *args, **kwargs):
		"""
		#Request(Body)
		```
		{
			"section": "c4cd2d9d-277e-439f-8958-1a1a6f1be62e",
			"name": "AI",
			"description": "File Learn AI",
			"file": "/media/8b30e0cc-e70e-48f8-a0ec-245c6134fb45/c4cd2d9d-277e-439f-8958-1a1a6f1be62e/5b8b1e7e-e037-4da1-a630-5e3d97ceb294/import_data.html",
			"index":5,
		    "is_active": true
		}
		```
		#Response(Success)
		```
		{
		    "data": {
		        "id": "5b8b1e7e-e037-4da1-a630-5e3d97ceb294",
		        "section": {
		            "id": "c4cd2d9d-277e-439f-8958-1a1a6f1be62e",
		            "course": {
		                "id": "8b30e0cc-e70e-48f8-a0ec-245c6134fb45",
		                "author": {
		                    "id": "0f75a7e7-321f-4691-ac26-2de6fafe2ee1",
		                    "first_name": null,
		                    "last_name": null,
		                    "email": "testuser@gmail.com"
		                },
		                "name": "fdgdf",
		                "description": "",
		                "is_active": true,
		                "is_deleted": false
		            },
		            "name": "AI Courses",
		            "index": 3,
		            "is_active": false
		        },
		        "name": "AI",
		        "description": "Test",
		        "file": "/media/8b30e0cc-e70e-48f8-a0ec-245c6134fb45/c4cd2d9d-277e-439f-8958-1a1a6f1be62e/5b8b1e7e-e037-4da1-a630-5e3d97ceb294/import_data.html",
		        "index": 5,
		        "is_active": true
		    },
		    "code": 3008,
		    "msg": "Course Section File updated successfully"
		}
		```
		# Response(Error)
		```
		{
		    "msg": "Invalid post data provided",
		    "code": 1000,
		    "data": {
		        "section": [
		            "'c4cd2d9d-277e-439f-8958-1a1a6f1be62' is not a valid UUID."
		        ]
		    }
		}
		```
		# Response(Error)
		```
		{
		    "msg": "Such pk not found",
		    "code": 4000
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
		course_file = self.get_object()
		if course_file:
			serializer = self.serializer_class(
				course_file,
				data=request.data,
				partial=True,
			)
			if serializer.is_valid():
				serializer.save()
				return Response(
					res_codes.get_response_dict(
						res_codes.COURSE_SECTION_FILE_UPDATED,
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
		return Response(
			res_codes.get_response_dict(
				res_codes.PK_NOT_FOUND
			),
			status=status.HTTP_400_BAD_REQUEST
		)

	def delete(self, request, *args, **kwargs):
		"""
		#Response(Success)
		{
		    "msg": "Course Section File deleted successfully",
		    "code": 3009
		}
		# Response(Error)
		```
		{
		    "msg": "Such pk not found",
		    "code": 4000
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
		course_file = self.get_object()
		if course_file:
			course_file.is_active = False
			course_file.is_deleted = True
			return Response(
				res_codes.get_response_dict(
					res_codes.COURSE_SECTION_FILE_DELETED
				),
				status=status.HTTP_204_NO_CONTENT,
			)
		return Response(
			res_codes.get_response_dict(
				res_codes.PK_NOT_FOUND
			),
			status=status.HTTP_400_BAD_REQUEST
		)


class CoursesDetailAPIView(APIView):
	"""
	List all the available course,sections,files.
	"""
	permission_classes = (IsAuthenticated, IsAdmin)
	serializer_class = CoursesDetailSerializer

	def get(self, request, format=None):
		"""
		#Response
		{
		    "data": [
		        {
		            "author": "0f75a7e7-321f-4691-ac26-2de6fafe2ee1",
		            "name": "AI",
		            "description": "Learn AI",
		            "is_active": true,
		            "course_sections": [
		                {
		                    "course": "8b30e0cc-e70e-48f8-a0ec-245c6134fb45",
		                    "name": "Test Section",
		                    "index": 0,
		                    "is_active": false,
		                    "course_files": [
		                        {
		                            "section": "c4cd2d9d-277e-439f-8958-1a1a6
		                            	f1be62e",
		                            "name": "AI",
		                            "description": "Test",
		                            "file": "/media/8b30e0cc-e70e-48f8-a0ec-24
		                            	5c6134fb45/c4cd2d9d-277e-439f-8958-1a1
		                            	a6f1be62e/5b8b1e7e-e037-4da1-a630-5e3d
		                            	97ceb294/import_data.html",
		                            "index": 5,
		                            "is_active": false
		                        },
		                        {
		                            "section": "c4cd2d9d-277e-439f-8958-1a1a6f
		                            	1be62e",
		                            "name": "AI",
		                            "description": "Test",
		                            "file": "/media/8b30e0cc-e70e-48f8-a0ec-245
		                            	c6134fb45/c4cd2d9d-277e-439f-8958-1a1a6
		                            	f1be62e/3b1a5509-8eec-4ad3-9099-da11946
		                            	81816/import_data.html",
		                            "index": 5,
		                            "is_active": false
		                        }
		                    ]
		                },
		                {
		                    "course": "8b30e0cc-e70e-48f8-a0ec-245c6134fb45",
		                    "name": "ML",
		                    "index": 3,
		                    "is_active": false,
		                    "course_files": []
		                }
		            ]
		        },
		        {
		            "author": "0f75a7e7-321f-4691-ac26-2de6fafe2ee1",
		            "name": "MLM",
		            "description": "2",
		            "is_active": false,
		            "course_sections": []
		        },
		    ],
		    "code": 2000,
		    "msg": "Request processed successfully"
		}
		"""
		courses = Course.objects.all()
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


class CourseDetailTabCreateAPIView(APIView):
	permission_classes = (IsAuthenticated, IsAdmin)
	serializer_class = CourseDetailTabCreateSerializer

	def post(self, request, *args, **kwargs):
		"""
		### Body:
		```
		{
		    "course": "8b30e0cc-e70e-48f8-a0ec-245c6134fb45",
		    "name": "AI",
		    "content": "AI content",
		    "index": "3",
		    "is_active": false
		}
		```
		#### Response (success):
		```
		{
		    "code": 3010,
		    "data": {
		        "course": "8b30e0cc-e70e-48f8-a0ec-245c6134fb45",
		        "name": "AI",
		        "content": "AI content",
		        "index": 3,
		        "is_active": false
		    },
		    "msg": "Course Detail Tab created successfully"
		}
		```
		#### Response (error):
		```
		{
		    "code": 1000,
		    "msg": "Invalid post data provided",
		    "data": {
		        "content": [
		            "This field may not be blank."
		        ],
		        "index": [
		            "A valid integer is required."
		        ],
		        "name": [
		            "This field may not be blank."
		        ],
		        "course": [
		            "This field may not be null."
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
		        "course": [
		            "Invalid pk \"8b30e0cc-e70e-48f8-a0ec-245c6134fb46\" - object does not exist."
		        ]
		    }
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
		data = request.data.copy()
		serializer = self.serializer_class(data=data)
		if serializer.is_valid():
			serializer.save()
			return Response(
				res_codes.get_response_dict(
					res_codes.COURSE_DETAIL_TAB_CREATED,
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


class CourseDetailTabUpdateAPIView(APIView):
	"""
	Retrieve, update or delete a course file instance.
	"""
	permission_classes = (IsAuthenticated, IsAdmin)
	serializer_class = CourseDetailTabSerializer

	def get_object(self):
		try:
			return CourseDetailTab.objects.get(pk=self.kwargs.get('pk'))
		except CourseDetailTab.DoesNotExist:
			return None

	def get(self, request, *args, **kwargs):
		"""
		# Response(Success)
		``` 
		{
		    "code": 2000,
		    "msg": "Request processed successfully",
		    "data": {
		        "id": "9128d478-0df2-4233-9422-160fdc1b54cc",
		        "course": {
		            "id": "a26077a9-9a40-4f35-87a6-d5828c46baf6",
		            "author": {
		                "id": "bbc34100-0870-493c-a5ea-2a6d72977ddc",
		                "first_name": "golu",
		                "last_name": "saini",
		                "email": "gauravsaini793@gmail.com"
		            },
		            "name": "AI course update",
		            "description": "Learn AI Course",
		            "is_active": true,
		            "is_deleted": false
		        },
		        "name": "AI",
		        "content": "AI content",
		        "index": 3,
		        "is_active": true
		    }
		}
		```
		# Response(Error)
		```
		{
		    "msg": "Such pk not found",
		    "code": 4000
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

		detail_tab = self.get_object()
		if detail_tab:
			serializer = self.serializer_class(detail_tab)
			return Response(
				res_codes.get_response_dict(
					res_codes.SUCCESS,
					serializer.data,
				),
				status=status.HTTP_200_OK,
			)
		return Response(
				res_codes.get_response_dict(
					res_codes.PK_NOT_FOUND
				),
				status=status.HTTP_400_BAD_REQUEST
			)

	def patch(self, request, *args, **kwargs):
		"""
		#Request(Body)
		```
		{
		    "course": "8b30e0cc-e70e-48f8-a0ec-245c6134fb45",
		    "name": "NN",
		    "content": "NN content",
		    "index": "3",
		    "is_active": false
		}
		```
		#Response(Success)
		```
		{
		    "code": 3011,
		    "data": {
		        "id": "9128d478-0df2-4233-9422-160fdc1b54cc",
		        "course": {
		            "id": "a26077a9-9a40-4f35-87a6-d5828c46baf6",
		            "author": {
		                "id": "bbc34100-0870-493c-a5ea-2a6d72977ddc",
		                "first_name": "golu",
		                "last_name": "saini",
		                "email": "gauravsaini793@gmail.com"
		            },
		            "name": "AI course update",
		            "description": "Learn AI Course",
		            "is_active": true,
		            "is_deleted": false
		        },
		        "name": "NN file",
		        "content": "NN content",
		        "index": 3,
		        "is_active": true
		    },
		    "msg": "Course Detail Tab updated successfully"
		}
		```
		# Response(Error)
		```
		{
		    "data": {
		        "course": [
		            "Invalid pk \"8b30e0cc-e70e-48f8-a0ec-245c6134fb95\" 
		            - object does not exist."
		        ]
		    },
		    "msg": "Invalid post data provided",
		    "code": 1000
		}
		```
		# Response(Error)
		```
		{
		    "msg": "Such pk not found",
		    "code": 4000
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
		detail_tab = self.get_object()
		if detail_tab:
			serializer = self.serializer_class(
				detail_tab,
				data=request.data,
				partial=True,
			)
			if serializer.is_valid():
				serializer.save()
				return Response(
					res_codes.get_response_dict(
						res_codes.COURSE_DETAIL_TAB_UPDATED,
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
		return Response(
			res_codes.get_response_dict(
				res_codes.PK_NOT_FOUND
			),
			status=status.HTTP_400_BAD_REQUEST
		)

	def delete(self, request, *args, **kwargs):
		"""
		#Response(Success)
		{
		    "code": 3012,
		    "msg": "Course Detail Tab deleted successfully"
		}
		# Response(Error)
		```
		{
		    "msg": "Such pk not found",
		    "code": 4000
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
		detail_tab = self.get_object()
		if detail_tab:
			detail_tab.is_active = False
			detail_tab.is_deleted = True
			detail_tab.save()
			return Response(
				res_codes.get_response_dict(
					res_codes.COURSE_DETAIL_TAB_DELETED
				),
				status=status.HTTP_204_NO_CONTENT,
			)
		return Response(
			res_codes.get_response_dict(
				res_codes.PK_NOT_FOUND
			),
			status=status.HTTP_400_BAD_REQUEST
		)


class CourseDetailTabListCreateApiView(APIView):
	permission_classes = (IsAuthenticated, IsAdmin)
	serializer_class = CourseDetailTabListCreateSerializer

	def post(self, request, *args, **kwargs):
		"""
		### Body:
		```
		{
			"course_detail_tab": "9128d478-0df2-4233-9422-160fdc1b54cc",
			"content": "AI tab",
			"index": "3",
			"is_active"
		}
		```
		#### Response (success):
		```
		{
			"data": {
				"course_detail_tab": "9128d478-0df2-4233-9422-160fdc1b54cc",
				"content": "AI tab",
				"index": 3,
				"is_active": false
			},
			"code": 3013,
			"msg": "Course Detail Tab List created successfully"
		}
		```
		#### Response (error):
		```
		{
			"data": {
				"course_detail_tab": [
				    "A valid integer is required."
				],
				"content": [
				    "This field may not be blank."
				],
				"index": [
				    "This field may not be null."
				]
			},
			"code": 1000,
			"msg": "Invalid post data provided"
		}
		```
		#### Response (error):
		```
		{
		    "code": 1000,
		    "data": {
		        "course_detail_tab": [
		            "'4dd35b89-3261-4c5a-b022-cd84b5676948' is not a valid UUID."
		        ]
		    },
		    "msg": "Invalid post data provided"
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
		data = request.data.copy()
		serializer = self.serializer_class(data=data)
		if serializer.is_valid():
			serializer.save()
			return Response(
				res_codes.get_response_dict(
					res_codes.COURSE_DETAIL_TAB_LIST_CREATED,
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


class CourseDetailTabListUpdateApiView(APIView):
	"""
	Retrieve, update or delete a course tab list instance.
	"""
	permission_classes = (IsAuthenticated, IsAdmin)
	serializer_class = CourseDetailTabListDetailSerializer

	def get_object(self):
		try:
			return CourseDetailTabList.objects.get(pk=self.kwargs.get('pk'))
		except CourseDetailTabList.DoesNotExist:
			return None

	def get(self, request, *args, **kwargs):
		"""
		# Response(Success)
		``` 
		{
		    "msg": "Request processed successfully",
		    "code": 2000,
		    "data": {
		        "id": "9cb80e00-ba54-47d1-89ab-19ad282d6e95",
		        "course_detail_tab": {
		            "id": "9128d478-0df2-4233-9422-160fdc1b54cc",
		            "course": {
		                "id": "a26077a9-9a40-4f35-87a6-d5828c46baf6",
		                "author": {
		                    "id": "bbc34100-0870-493c-a5ea-2a6d72977ddc",
		                    "first_name": "golu",
		                    "last_name": "saini",
		                    "email": "gauravsaini793@gmail.com"
		                },
		                "name": "AI course update",
		                "description": "Learn AI Course",
		                "is_active": true,
		                "is_deleted": false
		            },
		            "name": "NN file",
		            "content": "NN content",
		            "index": 3,
		            "is_active": true
		        },
		        "content": "AI YARD",
		        "index": 3,
		        "is_active": true
		    }
		}
		```
		# Response(Error)
		```
		{
		    "msg": "Such pk not found",
		    "code": 4000
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

		tab_list_obj = self.get_object()
		if tab_list_obj:
			serializer = self.serializer_class(tab_list_obj)
			return Response(
				res_codes.get_response_dict(
					res_codes.SUCCESS,
					serializer.data,
				),
				status=status.HTTP_200_OK,
			)
		return Response(
				res_codes.get_response_dict(
					res_codes.PK_NOT_FOUND
				),
				status=status.HTTP_400_BAD_REQUEST
			)

	def patch(self, request, *args, **kwargs):
		"""
		#Request(Body)
		```
		{
		    "course_detail_tab": "8b30e0cc-e70e-48f8-a0ec-245c6134fb45",
		    "content": "AI files",
		    "index": 3,
		    "is_active": false
		}
		```
		#Response(Success)
		```
		{
		    "data": {
		        "id": "9cb80e00-ba54-47d1-89ab-19ad282d6e95",
		        "course_detail_tab": {
		            "id": "9128d478-0df2-4233-9422-160fdc1b54cc",
		            "course": {
		                "id": "a26077a9-9a40-4f35-87a6-d5828c46baf6",
		                "author": {
		                    "id": "bbc34100-0870-493c-a5ea-2a6d72977ddc",
		                    "first_name": "golu",
		                    "last_name": "saini",
		                    "email": "gauravsaini793@gmail.com"
		                },
		                "name": "AI course update",
		                "description": "Learn AI Course",
		                "is_active": true,
		                "is_deleted": false
		            },
		            "name": "NN file",
		            "content": "NN content",
		            "index": 3,
		            "is_active": true
		        },
		        "content": "AI files",
		        "index": 3,
		        "is_active": false
		    },
		    "msg": "Course Detail Tab List updated successfully",
		    "code": 3014
		}
		```
		# Response(Error)
		```
		{
		    "data": {
		        "course_detail_tab": [
		            "Invalid pk \"8b30e0cc-e70e-48f8-a0ec-245c6134fb74\" 
		            	- object does not exist."
		        ]
		    },
		    "code": 1000,
		    "msg": "Invalid post data provided"
		}
		```
		# Response(Error)
		```
		{
		    "msg": "Such pk not found",
		    "code": 4000
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
		tab_list_obj = self.get_object()
		if tab_list_obj:
			serializer = self.serializer_class(
				tab_list_obj,
				data=request.data,
				partial=True,
			)
			if serializer.is_valid():
				serializer.save()
				return Response(
					res_codes.get_response_dict(
						res_codes.COURSE_DETAIL_TAB_LIST_UPDATED,
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
		return Response(
			res_codes.get_response_dict(
				res_codes.PK_NOT_FOUND
			),
			status=status.HTTP_400_BAD_REQUEST
		)

	def delete(self, request, *args, **kwargs):
		"""
		#Response(Success)
		{
		    "msg": "Course Tab List deleted successfully",
		    "code": 3015
		}
		# Response(Error)
		```
		{
		    "msg": "Such pk not found",
		    "code": 4000
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
		tab_list_obj = self.get_object()
		if tab_list_obj:
			tab_list_obj.is_active = False
			tab_list_obj.is_deleted = True
			tab_list_obj.save()
			return Response(
				res_codes.get_response_dict(
					res_codes.COURSE_DETAIL_TAB_LIST_DELETED,
				),
				status=status.HTTP_204_NO_CONTENT,
			)
		return Response(
			res_codes.get_response_dict(
				res_codes.PK_NOT_FOUND
			),
			status=status.HTTP_400_BAD_REQUEST
		)


class CoursesFullDetailAPIView(APIView):
	"""
	To list all the available courses with sections, files, detail tabs
	and detail tab lists.
	"""
	permission_classes = (IsAuthenticated, IsAdmin)
	serializer_class = CoursesFullDetailSerializer

	def get(self, request, *args, **kwargs):
		"""
		# Response(Success)
		``` 
		{
		    "msg": "Request processed successfully",
		    "code": 2000,
		    "data": [
		        {
		            "id": "8b30e0cc-e70e-48f8-a0ec-245c6134fb45",
		            "author": {
		                "id": "0f75a7e7-321f-4691-ac26-2de6fafe2ee1",
		                "first_name": null,
		                "last_name": null,
		                "email": "testuser@gmail.com"
		            },
		            "name": "fdgdf",
		            "description": "",
		            "is_active": true,
		            "sections": [
		                {
		                    "id": "c4cd2d9d-277e-439f-8958-1a1a6f1be62e",
		                    "files": [
		                        {
		                            "id": "5b8b1e7e-e037-4da1-a630-5e3d97ceb294",
		                            "name": "AI",
		                            "description": "Test",
		                            "file": "/media/8b30e0cc-e70e-48f8-a0ec-245c6134fb45/c4cd2d9d-277e-439f-8958-1a1a6f1be62e/5b8b1e7e-e037-4da1-a630-5e3d97ceb294/import_data.html",
		                            "index": 5,
		                            "is_active": true
		                        },
		                        {
		                            "id": "3b1a5509-8eec-4ad3-9099-da1194681816",
		                            "name": "AI",
		                            "description": "Test",
		                            "file": "/media/8b30e0cc-e70e-48f8-a0ec-245c6134fb45/c4cd2d9d-277e-439f-8958-1a1a6f1be62e/3b1a5509-8eec-4ad3-9099-da1194681816/import_data.html",
		                            "index": 5,
		                            "is_active": false
		                        }
		                    ],
		                    "name": "AI Courses",
		                    "index": 3,
		                    "is_active": false
		                },
		                {
		                    "id": "fd39e393-c328-491b-bb8a-16ad4c318d1a",
		                    "files": [],
		                    "name": "test",
		                    "index": 3,
		                    "is_active": false
		                }
		            ],
		            "detail_tabs": [
		                {
		                    "id": "5602539f-d057-4dde-9f92-7c0d0351309e",
		                    "lists": [],
		                    "name": "AI",
		                    "content": "AI content",
		                    "index": 3,
		                    "is_active": false
		                },
		                {
		                    "id": "306dcda1-567c-44db-9f49-d83d7db2d9f3",
		                    "lists": [],
		                    "name": "AI",
		                    "content": "AI content",
		                    "index": 3,
		                    "is_active": false
		                },
		                {
		                    "id": "6d403328-2b0c-413b-a6bb-f47f0099a412",
		                    "lists": [],
		                    "name": "AI",
		                    "content": "AI content",
		                    "index": 3,
		                    "is_active": false
		                }
		            ]
		        }
		    ]
		}
		```
		"""
		courses = Course.objects.all()
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


class CategoryCreateApiView(APIView):
	permission_classes = (IsAuthenticated, IsAdmin)
	serializer_class = CategoryCreateSerializer

	def post(self, request, *args, **kwargs):
		"""
		### Body:
		```
		{
			"name": "AI",
			"description": "desc"
		}
		```
		#### Response:
		```
		{
		    "data": {
		        "id": "6829f57f-084f-4930-97e7-117899b9e55d",
		        "name": "test",
		        "description": "desc"
		    },
		    "msg": "Category created successfully",
		    "code": 6000
		}
		```
		#### Response (error):
		```
		{
		    "code": 1000,
		    "data": {
		        "name": [
		            "This field must be unique."
		        ]
		    },
		    "msg": "Invalid post data provided"
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
		data = request.data.copy()
		serializer = self.serializer_class(data=data)
		if serializer.is_valid():
			serializer.save()
			return Response(
				res_codes.get_response_dict(
					res_codes.CATEGORY_CREATED,
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

	def get(self, request, format=None):
		"""
		{
		    "code": 2000,
		    "data": [
		        {
		            "id": "6829f57f-084f-4930-97e7-117899b9e55d",
		            "name": "test",
		            "description": "desc"
		        },
		        {
		            "id": "70d24a8f-7726-437b-9b28-a2b4cee965de",
		            "name": "AI",
		            "description": "AI desc"
		        }
		    ],
		    "msg": "Request processed successfully"
		}
		"""
		categories = Category.objects.all()
		serializer = CourseSerializer(
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


class CategoryUpdateApiView(APIView):
	"""
	Retrieve, update or delete a category instance.
	"""
	permission_classes = (IsAuthenticated, IsAdmin)
	serializer_class = CourseSerializer

	def get_object(self):
		try:
			return Category.objects.get(pk=self.kwargs.get('pk'))
		except Category.DoesNotExist:
			return None

	def get(self, request, *args, **kwargs):
		"""
		#Response
		```
		{
		    "data": {
		        "id": "70d24a8f-7726-437b-9b28-a2b4cee965de",
		        "name": "test",
		        "description": "desc"
		    },
		    "code": 2000,
		    "msg": "Request processed successfully"
		}
		```
		# Response(Error)
		```
		{
		    "code": 4000,
		    "msg": "Such pk not found"
		}
		"""
		category = self.get_object()
		if category:
			serializer = self.serializer_class(category)
			return Response(
				res_codes.get_response_dict(
					res_codes.SUCCESS,
					serializer.data,
				),
				status=status.HTTP_200_OK,
			)
		return Response(
			res_codes.get_response_dict(
				res_codes.PK_NOT_FOUND
			),
			status=status.HTTP_400_BAD_REQUEST
		)

	def patch(self, request, *args, **kwargs):
		"""
		#Request(Body)
		```
		{
	        "name": "NN test",
	        "description": "desc"
		}
		```
		#Response(Success)
		```
		{
		    "code": 6001,
		    "msg": "Category updated successfully",
		    "data": {
		        "id": "70d24a8f-7726-437b-9b28-a2b4cee965de",
		        "name": "NN test",
		        "description": "desc"
		    }
		}
		```
		# Response(Error)
		```
		{
		    "code": 4000,
		    "msg": "Such pk not found"
		}
		```
		"""
		category = self.get_object()
		if category:
			serializer = self.serializer_class(
				category,
				data=request.data,
				partial=True,
			)
			if serializer.is_valid():
				serializer.save()
				return Response(
						res_codes.get_response_dict(
							res_codes.CATEGORY_UPDATED,
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
		return Response(
			res_codes.get_response_dict(
				res_codes.PK_NOT_FOUND
			),
			status=status.HTTP_400_BAD_REQUEST
		)

	def delete(self, request, *args, **kwargs):
		"""
		#Response(Success)
		{
		    "msg": "Category deleted successfully",
		    "code": 6002
		}
		# Response(Error)
		```
		{
		    "msg": "Such pk not found",
		    "code": 4000
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
		category = self.get_object()
		if category:
			category.delete()
			return Response(
				res_codes.get_response_dict(
					res_codes.CATEGORY_DELETED
				),
				status=status.HTTP_204_NO_CONTENT
			)
		return Response(
			res_codes.get_response_dict(
				res_codes.PK_NOT_FOUND
			),
			status=status.HTTP_400_BAD_REQUEST
		)


class CategoryCourseCreateListApiView(APIView):
	permission_classes = (IsAuthenticated, IsAdmin)
	serializer_class = CategoryCourseCreateSerializer

	def post(self, request, *args, **kwargs):
		"""
		### Body:
		```
		{
		    "category": "6829f57f-084f-4930-97e7-117899b9e55d",
		    "course": "42ee7060-5106-4e92-846d-f6a14dadce3c"
		}
		```
		#### Response:
		```
		{
    		"code": 6003,
		    "data": {
		        "id": "dae5f0c3-9aac-4405-8ab3-403b6a7b45a4",
		        "course": "42ee7060-5106-4e92-846d-f6a14dadce3c",
		        "category": "6829f57f-084f-4930-97e7-117899b9e55d"
		    },
		    "msg": "Category course created successfully"
		}
		```
		#### Response (error):
		```
		{
		    "msg": "Invalid post data provided",
		    "data": {
		        "category": [
		            "This field is required."
		        ],
		        "course": [
		            "This field is required."
		        ]
		    },
		    "code": 1000
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
		data = request.data.copy()
		serializer = self.serializer_class(data=data)
		if serializer.is_valid():
			serializer.save()
			return Response(
				res_codes.get_response_dict(
					res_codes.CATEGORY_COURSE_CREATED,
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

	def get(self, request, format=None):
		"""
		{
		    "code": 2000,
		    "data": [
		        {
		            "id": "6829f57f-084f-4930-97e7-117899b9e55d",
		            "name": "test",
		            "description": "desc"
		        },
		        {
		            "id": "70d24a8f-7726-437b-9b28-a2b4cee965de",
		            "name": "AI",
		            "description": "AI desc"
		        }
		    ],
		    "msg": "Request processed successfully"
		}
		"""
		categorie_course = CategoryCourseRelation.objects.all()
		serializer = CategoryCourseRelationSerializer(
				categorie_course,
				many=True
			)
		return Response(
				res_codes.get_response_dict(
					res_codes.SUCCESS,
					serializer.data,
				),
				status=status.HTTP_200_OK,
			)


class CategoryCourseUpdateApiView(APIView):
	"""
	Retrieve, update or delete a category course instance.
	"""
	permission_classes = (IsAuthenticated, IsAdmin)
	serializer_class = CategoryCourseUpdateSerializer

	def get_object(self):
		try:
			return CategoryCourseRelation.objects.get(pk=self.kwargs.get('pk'))
		except CategoryCourseRelation.DoesNotExist:
			return None

	def get(self, request, *args, **kwargs):
		"""
		#Response
		```
		{
		    "code": 2000,
		    "data": {
		        "id": "dae5f0c3-9aac-4405-8ab3-403b6a7b45a4",
		        "course": {
		            "id": "42ee7060-5106-4e92-846d-f6a14dadce3c",
		            "author": {
		                "id": "51fb2581-7c14-459d-9f3b-0ed593cbeb0f",
		                "first_name": null,
		                "last_name": null,
		                "email": "gauravsaini793@gmail.com"
		            },
		            "name": "Test AI",
		            "description": "test course",
		            "is_active": true,
		            "is_deleted": false
		        },
		        "category": {
		            "id": "6829f57f-084f-4930-97e7-117899b9e55d",
		            "name": "teyst",
		            "description": "desc"
		        }
		    },
		    "msg": "Request processed successfully"
		}
		```
		# Response(Error)
		```
		{
		    "code": 4000,
		    "msg": "Such pk not found"
		}
		"""
		category_course = self.get_object()
		if category_course:
			serializer = self.serializer_class(category_course)
			return Response(
				res_codes.get_response_dict(
					res_codes.SUCCESS,
					serializer.data,
				),
				status=status.HTTP_200_OK,
			)
		return Response(
			res_codes.get_response_dict(
				res_codes.PK_NOT_FOUND
			),
			status=status.HTTP_400_BAD_REQUEST
		)

	def patch(self, request, *args, **kwargs):
		"""
		#Request(Body)
		```
		{
		    "category": "902f4bda-4cbe-4a71-bec3-c767f02b8ae6",
		    "course": "42ee7060-5106-4e92-846d-f6a14dadce3c"
		}
		```
		#Response(Success)
		```
		{
		    "data": {
		        "id": "b3cfdb00-a832-46ca-80cf-6322622843ff",
		        "course": {
		            "id": "42ee7060-5106-4e92-846d-f6a14dadce3c",
		            "author": {
		                "id": "51fb2581-7c14-459d-9f3b-0ed593cbeb0f",
		                "first_name": null,
		                "last_name": null,
		                "email": "gauravsaini793@gmail.com"
		            },
		            "name": "Test AI",
		            "description": "test course",
		            "is_active": true,
		            "is_deleted": false
		        },
		        "category": {
		            "id": "902f4bda-4cbe-4a71-bec3-c767f02b8ae6",
		            "name": "test cat",
		            "description": "test"
		        }
		    },
		    "code": 6004,
		    "msg": "Category course updated successfully"
		}
		```
		# Response(Error)
		```
		{
		    "code": 4000,
		    "msg": "Such pk not found"
		}
		```
		"""
		category_course = self.get_object()
		if category_course:
			serializer = self.serializer_class(
				category_course,
				data=request.data,
				partial=True,
			)
			if serializer.is_valid():
				serializer.save()
				return Response(
						res_codes.get_response_dict(
							res_codes.CATEGORY_COURSE_UPDATED,
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
		return Response(
			res_codes.get_response_dict(
				res_codes.PK_NOT_FOUND
			),
			status=status.HTTP_400_BAD_REQUEST
		)

	def delete(self, request, *args, **kwargs):
		"""
		#Response(Success)
		{
		    "msg": "Category course deleted successfully",
		    "code": 6005
		}
		# Response(Error)
		```
		{
		    "msg": "Such pk not found",
		    "code": 4000
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
		category = self.get_object()
		if category:
			category.delete()
			return Response(
				res_codes.get_response_dict(
					res_codes.CATEGORY_COURSE_DELETED
				),
				status=status.HTTP_204_NO_CONTENT
			)
		return Response(
			res_codes.get_response_dict(
				res_codes.PK_NOT_FOUND
			),
			status=status.HTTP_400_BAD_REQUEST
		)