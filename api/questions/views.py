from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer

from questions.models import Opinion,Question,Category
from questions.serializers import OpinionSerializer,QuestionSerializer,CategorySerializer


# curl http://127.0.0.1:8000/questions/categories/
class CategoryList(APIView):
	"""
	List all Categories
	"""
	def get(self, request, format=None):
		categories = Category.objects.all()
		serializer = CategorySerializer(categories, many=True)
		return Response(serializer.data)

# curl http://127.0.0.1:8000/questions/category/1/
class QuestionList(APIView):
	"""
	List all Questions from a specific category based on Category pk
	"""
	def get(self, request, category_pk, format=None):
		questions = Question.objects.filter(category=category_pk)
		if not questions:
			get_object_or_404(Category, pk=category_pk)
		serializer = QuestionSerializer(questions, many=True)
		return Response(serializer.data)

# curl http://127.0.0.1:8000/questions/1/opinions/
class OpinionList(APIView):
	"""
	Retrieves an aggregated list of opinion information for a Question
	"""
	def get(self, request, question_pk, format=None):
		question = get_object_or_404(Question, pk=question_pk)
		output = {}
		totals =  question.get_json_friendly_counts()
		output['totals'] = totals
		content = JSONRenderer().render(output)
		return Response(content)

	"""
	Count a vote towards an opinion on a question.
	Note: This needs work for ensuring no duplicate votes as best as possible
	"""
	def post(self, request, question_pk, format=None):
		serializer = OpinionSerializer(data=request.DATA)
		#Do checks like question_pk == serialized q pk, exists, etc
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)