from rest_framework import serializers
from questions.models import Category, Question, Opinion

class CategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = Category
		fields = ('cat_name')

class QuestionSerializer(serializers.ModelSerializer):
	class Meta:
		model = Question
		fields = ('statement')

class OpinionSerializer(serializers.ModelSerializer):
	class Meta:
		model = Opinion
		fields = ('question','vote')

	def restore_object(self, attrs, instance=None):
		"""
		Create or update a new opinion instance, given a dictionary
		of deserialized field values.

		Note that if we don't define this method, then deserializing
		data will simply return a dictionary of items.
		"""
		if instance:
			# Update existing instance
			instance.title = attrs.get('question', instance.question)
			instance.vote = attrs.get('vote', instance.vote)
			return instance

		# Create new instance
		return Opinion(**attrs)