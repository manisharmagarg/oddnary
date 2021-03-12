# restframework imports
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
#djnago imports
from django.conf import settings
from django.contrib.auth import get_user_model
from .serializers import (
	AssignmentDetailSerializer,
	AssignmentSolutionCreateSerializer,
	AssignmentSolutionDetailSerializer,
	AssignmentSolutionFileUploadSerializer,
	AssignmentSolutionDetailWithFileSerializer,
)
from assignments.models import (
	Assignment,
	AssignmentSolution,
)
from utils import res_codes

User = get_user_model()


class AssignmentDetailAPIView(APIView):
	permission_classes = (IsAuthenticated,)
	serializer_class = AssignmentDetailSerializer

	def get_object(self):
		try:
			return Assignment.objects.get(
				pk=self.kwargs.get('pk'),
				course__author=self.request.user
				)
		except Assignment.DoesNotExist:
			return None

	def get(self, request, *args, **kwargs):
		"""
		#Response
		```
		{
		    "code": 2000,
		    "msg": "Request processed successfully",
		    "data": {
		        "course": "a26077a9-9a40-4f35-87a6-d5828c46baf6",
		        "course_section": null,
		        "name": "New AI Assignment",
		        "description": "Test Assignment",
		        "index": 2,
		        "is_active": false,
		        "files": [
		            {
		                "assignment": "630158a9-0490-4bd3-b787-5b43e23a4e92",
		                "name": "AI sub assignment",
		                "file": "/media/8b30e0cc-e70e-48f8-a0ec-245c6134fb45/1b817199-71f4-45ec-a1ab-2b388bc421ce/6cd235fa-b341-4cbc-8e36-6c25805d35ba/serializers.py",
		                "description": "AI assignment",
		                "index": 5,
		                "is_active": false
		            }
		        ]
		    }
		}
		```
		# Response(Error)
		```
		{
		    "code": 4000,
		    "msg": "Such pk not found"
		}
		"""
		assignment = self.get_object()
		if assignment:
			serializer = self.serializer_class(assignment)
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


class CourseAssignmentDetailAPIView(APIView):
	permission_classes = (IsAuthenticated,)
	serializer_class = AssignmentDetailSerializer

	def get_object(self):
		return Assignment.objects.filter(
			course__id=self.kwargs.get('pk'),
			course__author=self.request.user
			)

	def get(self, request, *args, **kwargs):
		"""
		#Response
		```
		{
		    "data": [
		        {
		            "course": "a26077a9-9a40-4f35-87a6-d5828c46baf6",
		            "course_section": null,
		            "name": "New AI Assignment",
		            "description": "Test Assignment",
		            "index": 2,
		            "is_active": false,
		            "files": [
		                {
		                    "assignment": "630158a9-0490-4bd3-b787-5b43e23a4e92",
		                    "name": "AI sub assignment",
		                    "file": "/media/8b30e0cc-e70e-48f8-a0ec-245c6134fb45/
		                    	1b817199-71f4-45ec-a1ab-2b388bc421ce/6cd235fa-b3
		                    	41-4cbc-8e36-6c25805d35ba/serializers.py",
		                    "description": "AI assignment",
		                    "index": 5,
		                    "is_active": false
		                }
		            ]
		        },
		        {
		            "course": "8b30e0cc-e70e-48f8-a0ec-245c6134fb45",
		            "course_section": "c4cd2d9d-277e-439f-8958-1a1a6f1be62e",
		            "name": "New AI Assignment",
		            "dataescription": "Assignment For Users",
		            "index": 3,
		            "is_active": false,
		            "files": [
		                {
		                    "assignment": "1b817199-71f4-45ec-a1ab-2b388bc421ce",
		                    "name": "AI sub assignment",
		                    "file": "/media/8b30e0cc-e70e-48f8-a0ec-245c6134fb45/
		                    	1b817199-71f4-45ec-a1ab-2b388bc421ce/1f118585-5cc
		                    	a-40fd-ac6f-b6cbab1ecd14/urls.py",
		                    "description": "AI assigment",
		                    "index": 5,
		                    "is_active": false
		                }
		            ]
		        },
		        {
		            "course": "8b30e0cc-e70e-48f8-a0ec-245c6134fb45",
		            "course_section": null,
		            "name": "New Assignment",
		            "description": "Test Assignment",
		            "index": 3,
		            "is_active": false,
		            "files": []
		        },
		    ],
		    "msg": "Request processed successfully",
		    "code": 2000
		}
		```
		"""
		assignment = self.get_object()
		serializer = self.serializer_class(
			assignment,
			many=True
			)
		return Response(
				res_codes.get_response_dict(
					res_codes.SUCCESS,
					serializer.data,
				),
				status=status.HTTP_200_OK,
			)


class AssignmentSolutionCreateAPIView(APIView):
	permission_classes = (IsAuthenticated,)
	serializer_class = AssignmentSolutionCreateSerializer

	def post(self, request, *args, **kwargs):
		"""
		### Body:
		```
		{
		    "assignment": "630158a9-0490-4bd3-b787-5b43e23a4e92",
		    "comment": "AI Solution"
		}
		```
		#### Response (success):
		```
		{
		    "data": {
		        "assignment": "630158a9-0490-4bd3-b787-5b43e23a4e92",
		        "comment": "AI Solution"
		    },
		    "msg": "Assignment Solution Created successfully",
		    "code": 5006
		}
		```
		#### Response (error):
		```
		{
		    "code": 1000,
		    "msg": "Invalid post data provided",
		    "data": {
		        "assignment": [
		            "This field may not be null."
		        ],
		        "comment": [
		            "This field may not be blank."
		        ]
		    }
		}
		```
		#### Response (error):
		```
		{
		    "data": {
		        "assignment": [
		            "'630158a9-490-4bd3-b787-5b43e23a4e92' is not a valid UUID."
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
			serializer.save(user=request.user)
			return Response(
				res_codes.get_response_dict(
					res_codes.ASSIGNMENT_SOLUTION_CREATED,
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


class AssignmentSolutionDetailAPIView(APIView):
	permission_classes = (IsAuthenticated,)
	serializer_class = AssignmentSolutionDetailSerializer

	def get_object(self):
		return AssignmentSolution.objects.filter(
			assignment__id=self.kwargs.get('pk'),
			user=self.request.user
			)

	def get(self, request, *args, **kwargs):
		"""
		#Response
		```
		{
    		"data": [
		        {
		            "comment": "AI Solution"
		        },
		        {
		            "comment": "AI Solution"
		        }
		    ],
		    "msg": "Request processed successfully",
		    "code": 2000
		}
		```
		# Response(Error)
		```
		{
		    "code": 4000,
		    "msg": "Such pk not found"
		}
		"""
		assignment_solution = self.get_object()
		serializer = self.serializer_class(
			assignment_solution,
			many=True
			)
		return Response(
				res_codes.get_response_dict(
					res_codes.SUCCESS,
					serializer.data,
				),
				status=status.HTTP_200_OK,
			)


class AssignmentSolutionDetailWithFileAPIView(APIView):
	permission_classes = (IsAuthenticated,)
	serializer_class = AssignmentSolutionDetailWithFileSerializer

	def get_object(self):
		return AssignmentSolution.objects.filter(
			assignment__id=self.kwargs.get('pk'),
			user=self.request.user
			)

	def get(self, request, *args, **kwargs):
		"""
		#Response
		```
		{
		    "code": 2000,
		    "data": [
		        {
		            "comment": "AI Solution",
		            "files": [
		                {
		                    "assignment_solution": "62d77c7c-7db2-4432-95cc-7fbda7aaa770",
		                    "name": "AI",
		                    "comment": "This is a test comment"
		                }
		            ]
		        },
		        {
		            "comment": "AI Solution",
		            "files": []
		        }
		    ],
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
		assignment_solution = self.get_object()
		serializer = self.serializer_class(
			assignment_solution,
			many=True
			)
		return Response(
				res_codes.get_response_dict(
					res_codes.SUCCESS,
					serializer.data,
				),
				status=status.HTTP_200_OK,
			)


class AssignmentSolutionFileUploadAPIView(APIView):
	permission_classes = (IsAuthenticated,)
	serializer_class = AssignmentSolutionFileUploadSerializer

	def post(self, request, *args, **kwargs):
		"""
		### Body:
		```
		{
			"assignment_solution": "795108ee-810b-4659-98e7-34d70e836792",
	        "name": "Neural Network",
	        "comment": "This is NN file.",
	        "file": "/media/a26077a9-9a40-4f35-87a6-d5828c46baf6/630158a9-0490-4bd3-b787-5b43e23a4e92/853efbcc-9879-4426-a9a6-d63fae7a3bfd/views.py"
		}
		```
		#### Response (success):
		```
		{
		    "msg": "Assignment Solution File Uploaded successfully",
		    "code": 5007,
		    "data": {
		        "assignment_solution": "795108ee-810b-4659-98e7-34d70e836792",
		        "name": "Neural Network",
		        "comment": "This is NN file.",
		        "file": "/media/a26077a9-9a40-4f35-87a6-d5828c46baf6/630158a9-0490-4bd3-b787-5b43e23a4e92/853efbcc-9879-4426-a9a6-d63fae7a3bfd/views.py"
		    }
		}
		```
		#### Response (error):
		```
		{
		    "code": 1000,
		    "msg": "Invalid post data provided",
		    "data": {
		        "file": [
		            "No file was submitted."
		        ],
		        "comment": [
		            "This field is required."
		        ],
		        "assignment_solution": [
		            "This field is required."
		        ],
		        "name": [
		            "This field is required."
		        ]
		    }
		}
		```
		#### Response (error):
		```
		{
		    "msg": "Invalid post data provided",
		    "code": 1000,
		    "data": {
		        "assignment_solution": [
		            "'795108ee-810b-4659-98e7-34d70ef836792' is not a valid UUID."
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
					res_codes.ASSIGNMENT_SOLUTION_FILE_UPLOADED,
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