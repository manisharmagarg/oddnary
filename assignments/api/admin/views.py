# restframework imports
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
#djnago imports
from django.conf import settings
from django.contrib.auth import get_user_model
from .serializers import (
	AssignmentCreateSerializer,
	AssignmentUpdateSerializer,
	AssignmentFileCreateSerializer,
	AssignmentFilleUpdateSerializer,
)
from assignments.models import (
	Assignment,
	AssignmentFile,
)
from utils.permissions import IsAdmin
from utils import res_codes

User = get_user_model()


class AssignmentCreateAPIView(APIView):
	permission_classes = (IsAuthenticated, IsAdmin)
	serializer_class = AssignmentCreateSerializer

	def post(self, request, *args, **kwargs):
		"""
		### Body(With Course Section):
		```
		{
		    "course": "8b30e0cc-e70e-48f8-a0ec-245c6134fb45",
		    "course_section": "c4cd2d9d-277e-439f-8958-1a1a6f1be62e",
		    "name": "AI Assignment",
		    "description": "Assignment",
		    "index": "3",
		    "is_active": false
		}
		```
		### Body(Without Course Section)
		```
		{
		    "course": "8b30e0cc-e70e-48f8-a0ec-245c6134fb45",
		    "name": "AI Assignment",
		    "description": "Assignment",
		    "index": "3",
		    "is_active": false
		}
		```
		#### Response (success):
		```
		{
		    "code": 5000,
		    "data": {
		        "course": "8b30e0cc-e70e-48f8-a0ec-245c6134fb45",
		        "course_section": "c4cd2d9d-277e-439f-8958-1a1a6f1be62e",
		        "name": "AI Assignment",
		        "description": "Assignment",
		        "index": 3,
		        "is_active": false
		    },
		    "msg": "Assignment created successfully"
		}
		```
		#### Response (success without course section)
		```
		{
		    "code": 5000,
		    "data": {
		        "course": "8b30e0cc-e70e-48f8-a0ec-245c6134fb45",
		        "course_section": null,
		        "name": "AI Assignment",
		        "description": "Assignment",
		        "index": 3,
		        "is_active": false
		    },
		    "msg": "Assignment created successfully"
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
		        ],
		        "course": [
		            "This field may not be null."
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
		    "data": {
		        "course": [
		            "'8b30e0cc-e70e-48f8-a0ec-245c6134fb5' is not a valid UUID."
		        ]
		    },
		    "code": 1000,
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
					res_codes.ASSIGNMENT_CREATED,
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


class AssignmentUpdateApiView(APIView):
	"""
	Retrieve, update or delete a course section instance.
	"""
	permission_classes = (IsAuthenticated, IsAdmin)
	serializer_class = AssignmentUpdateSerializer

	def get_object(self):
		try:
			return Assignment.objects.get(pk=self.kwargs.get('pk'))
		except Assignment.DoesNotExist:
			return None

	def get(self, request, *args, **kwargs):
		"""
		#Response
		```
		{
		    "msg": "Request processed successfully",
		    "data": {
		        "course": "8b30e0cc-e70e-48f8-a0ec-245c6134fb45",
		        "course_section": null,
		        "name": "AI Assignment",
		        "description": "Assignment",
		        "index": 3,
		        "is_active": false
		    },
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

	def patch(self, request, *args, **kwargs):
		"""
		### Body(With Course Section):
		```
		{
		    "course": "8b30e0cc-e70e-48f8-a0ec-245c6134fb45",
		    "course_section": "c4cd2d9d-277e-439f-8958-1a1a6f1be62e",
		    "name": "New AI Assignment",
		    "description": "Assignment for Users",
		    "index": "2",
		    "is_active": true
		}
		```
		### Body(Without Course Section)
		```
		{
		    "course": "8b30e0cc-e70e-48f8-a0ec-245c6134fb45",
		    "name": "New AI Assignment",
		    "description": "Assignment For Users",
		    "index": "3",
		    "is_active": true
		}
		```
		#### Response (success):
		```
		{
		    "msg": "Assignment updated successfully",
		    "data": {
		        "course": "8b30e0cc-e70e-48f8-a0ec-245c6134fb45",
		        "course_section": "c4cd2d9d-277e-439f-8958-1a1a6f1be62e",
		        "name": "New AI Assignment",
		        "description": "Assignment for Users",
		        "index": 2,
		        "is_active": true
		    },
		    "code": 5001
		}
		```
		#### Response (success without course section)
		```
		{
		    "msg": "Assignment updated successfully",
		    "data": {
		        "course": "8b30e0cc-e70e-48f8-a0ec-245c6134fb45",
		        "course_section": "c4cd2d9d-277e-439f-8958-1a1a6f1be62e",
		        "name": "New AI Assignment",
		        "description": "Assignment For Users",
		        "index": 3,
		        "is_active": true
		    },
		    "code": 5001
		}
		```
		# Response(Error)
		```
		{
		    "msg": "Invalid post data provided",
		    "data": {
		        "course": [
		            "'8b30e0cc-e70e-48f8-a0ec-245c6134fb5' is not a valid UUID."
		        ]
		    },
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
		assignment = self.get_object()
		if assignment:
			serializer = self.serializer_class(
				assignment,
				data=request.data,
				partial=True,
			)
			if serializer.is_valid():
				serializer.save()
				return Response(
					res_codes.get_response_dict(
						res_codes.ASSIGNMENT_UPDATED,
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
		    "code": 5002,
		    "msg": "Assignment deleted successfully"
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
		assignment = self.get_object()
		if assignment:
			assignment.is_active = False
			assignment.is_deleted = True
			assignment.save()
			return Response(
				res_codes.get_response_dict(
					res_codes.ASSIGNMENT_DELETED
				),
				status=status.HTTP_204_NO_CONTENT,
			)
		return Response(
			res_codes.get_response_dict(
				res_codes.PK_NOT_FOUND
			),
			status=status.HTTP_400_BAD_REQUEST
		)


class AssignmentFileCreateAPIView(APIView):
	permission_classes = (IsAuthenticated, IsAdmin)
	serializer_class = AssignmentFileCreateSerializer

	def post(self, request, *args, **kwargs):
		"""
		### Body:
		```
		{
		    "assignment": "1b817199-71f4-45ec-a1ab-2b388bc421ce",
		    "file": "serializers.py",
		    "name": "AI sub assignment",
		    "description": "AI assignment",
		    "index": "5",
		    "is_active": false
		}
		```
		#### Response (success):
		```
		{
		    "data": {
		        "assignment": "1b817199-71f4-45ec-a1ab-2b388bc421ce",
		        "name": "AI sub assignment",
		        "file": "/media/8b30e0cc-e70e-48f8-a0ec-245c6134fb45/1b817199-71f4-45ec-a1ab-2b388bc421ce/1f118585-5cca-40fd-ac6f-b6cbab1ecd14/serializers.py",
		        "description": "AI assignment",
		        "index": 5,
		        "is_active": false
		    },
		    "msg": "Assignment File saved successfully",
		    "code": 5003
		}
		```
		#### Response (error):
		```
		{
		    "code": 1000,
		    "data": {
		        "file": [
		            "No file was submitted."
		        ],
		        "assignment": [
		            "This field may not be null."
		        ],
		        "name": [
		            "This field may not be blank."
		        ],
		        "index": [
		            "A valid integer is required."
		        ],
		        "description": [
		            "This field may not be blank."
		        ]
		    },
		    "msg": "Invalid post data provided"
		}
		```
		#### Response (error):
		```
		{
		    "msg": "Invalid post data provided",
		    "code": 1000,
		    "data": {
		        "assignment": [
		            "'1b817199-71f4-45ec-a1ab-2b388b421ce' is not a valid UUID."
		        ],
		        "file": [
		            "No file was submitted."
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
					res_codes.ASSIGNMENT_FILE_CREATED,
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


class AssignmentFileUpdateApiView(APIView):
	"""
	Retrieve, update or delete a course section instance.
	"""
	permission_classes = (IsAuthenticated, IsAdmin)
	serializer_class = AssignmentFilleUpdateSerializer

	def get_object(self, pk):
		try:
			return AssignmentFile.objects.get(pk=pk)
		except AssignmentFile.DoesNotExist:
			return None

	def get(self, request, pk, format=None):
		"""
		#Response
		```
		{
		    "msg": "Request processed successfully",
		    "code": 2000,
		    "data": {
		        "assignment": "1b817199-71f4-45ec-a1ab-2b388bc421ce",
		        "name": "AI sub assignment",
		        "file": "/media/8b30e0cc-e70e-48f8-a0ec-245c6134fb45/1b817199-71f4-45ec-a1ab-2b388bc421ce/1f118585-5cca-40fd-ac6f-b6cbab1ecd14/serializers.py",
		        "description": "AI assignment",
		        "index": 5,
		        "is_active": false
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
		assignment_file = self.get_object(pk)
		if assignment_file:
			serializer = self.serializer_class(assignment_file)
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

	def put(self, request, pk, format=None):
		"""
		### Body(With Course Section):
		```
		{
		    "assignment": "1b817199-71f4-45ec-a1ab-2b388bc421ce",
		    "file": "test.py",
		    "name": "AI sub assignment",
		    "description": "AI assignment",
		    "index": "5",
		    "is_active": false
		}
		```
		#Response(Success)
		```
		{
		    "data": {
		        "assignment": "1b817199-71f4-45ec-a1ab-2b388bc421ce",
		        "name": "AI sub assignment",
		        "file": "/media/8b30e0cc-e70e-48f8-a0ec-245c6134fb45/1b817199-71f4-45ec-a1ab-2b388bc421ce/1f118585-5cca-40fd-ac6f-b6cbab1ecd14/test.py",
		        "description": "AI assigment",
		        "index": 5,
		        "is_active": false
		    },
		    "code": 5004,
		    "msg": "Assignment File updated successfully"
		}
		```
		# Response(Error)
		```
		{
		    "msg": "Invalid post data provided",
		    "code": 1000,
		    "data": {
		        "assignment": [
		            "'1b817199-71f4-45ec-a1ab-2b38bc421ce' is not a valid UUID."
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
		assignment_file = self.get_object(pk)
		if assignment_file:
			serializer = self.serializer_class(
				assignment_file,
				data=request.data
			)
			if serializer.is_valid():
				serializer.save()
				return Response(
					res_codes.get_response_dict(
						res_codes.ASSIGNMENT_FILE_UPDATED,
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

	def delete(self, request, pk, format=None):
		"""
		#Response(Success)
		{
		    "msg": "Assignment File deleted successfully",
		    "code": 5005
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
		assignment_file = self.get_object(pk)
		if assignment_file:
			assignment_file.is_active = False
			assignment_file.is_deleted = True
			assignment_file.save()
			return Response(
				res_codes.get_response_dict(
					res_codes.ASSIGNMENT_FILE_DELETED
				),
				status=status.HTTP_204_NO_CONTENT,
			)
		return Response(
			res_codes.get_response_dict(
				res_codes.PK_NOT_FOUND
			),
			status=status.HTTP_400_BAD_REQUEST
		)