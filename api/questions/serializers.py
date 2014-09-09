from rest_framework import serializers
from questions.models import Category, Question, Opinion

class CategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = Category
		fields = ('cat_name','id')

class QuestionSerializer(serializers.ModelSerializer):
	class Meta:
		model = Question
		fields = ('statement','category','pub_date','id')

class OpinionSerializer(serializers.ModelSerializer):
	class Meta:
		model = Opinion
		fields = ('question','vote')