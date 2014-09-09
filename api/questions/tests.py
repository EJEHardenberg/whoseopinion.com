import datetime
from django.test import TestCase
from rest_framework.test import APITestCase
from django.utils import timezone
from django.core.urlresolvers import reverse

from questions.models import Question,Opinion,Category

# Create your tests here.
class QuestionMethodTests(TestCase):
	
	def test_is_recent_with_future_question(self):
		"""
		is_recent() should return False for questions whose
		pub_date is in the future
		"""
		time = timezone.now() + datetime.timedelta(days=30)
		future_question = Question(pub_date=time)
		self.assertEqual(future_question.is_recent(),False)
	
	def test_is_recent_with_old_questions(self):
		"""
		is_recent() should return False for questions 
		whose pub_date is older than 1 day
		"""
		time = timezone.now() - datetime.timedelta(days=30)
		old_question = Question(pub_date=time)
		self.assertEqual(old_question.is_recent(), False)
	
	def test_is_recent_with_recent_question(self):
		"""
		is_recent() should return True for
		questions whose pub_date is within the last day
		"""
		time = timezone.now() - datetime.timedelta(hours=1)
		recent_question = Question(pub_date=time)
		self.assertEqual(recent_question.is_recent(), True)

class OpinionMethodTests(TestCase):

	def test_unicode_method_valid_votes(self):
		"""
		Test __unicode__ str output when Opinion's are valid
		should return strings within the Opinion.OPINION static
		"""
		strong_disagree = Opinion(vote=Opinion.STRONGLY_DISAGREE)
		disagree = Opinion(vote=Opinion.DISAGREE)
		neutral = Opinion(vote=Opinion.NEUTRAL)
		agree = Opinion(vote=Opinion.AGREE)
		strong_agree = Opinion(vote=Opinion.STRONGLY_AGREE)

		self.assertEqual(strong_disagree.__unicode__(), Opinion.vote_string(Opinion.STRONGLY_DISAGREE) )
		self.assertEqual(disagree.__unicode__(), Opinion.vote_string(Opinion.DISAGREE) )
		self.assertEqual(neutral.__unicode__(), Opinion.vote_string(Opinion.NEUTRAL) )
		self.assertEqual(agree.__unicode__(), Opinion.vote_string(Opinion.AGREE) )
		self.assertEqual(strong_agree.__unicode__(), Opinion.vote_string(Opinion.STRONGLY_AGREE) )

	def test_unicode_method_invalid_vote(self):
		"""
		Test __unicode__ str output when Opinion is invalid numerically
		"""
		invalid = Opinion(vote=-9999)

		self.assertEqual(invalid.__unicode__(), 'Invalid' )

def create_category(cat_name):
	"""
	Creates a category for use in testing
	"""
	Category.objects.create(cat_name=cat_name)

class CategoryViewTests(APITestCase):
	def test_index_listing(self):
		"""
		Test categories view with an empty list of categories
		"""
		response = self.client.get(reverse('questions:categories'))
		self.assertEqual(response.status_code, 200)
		self.assertQuerysetEqual(response.data,[])

	def test_populated_index_listing(self):
		"""
		Test categories view when categories exist
		"""
		create_category("test")
		response = self.client.get(reverse('questions:categories'))
		self.assertEqual(response.status_code, 200)
		data = ["{'cat_name': u'test', 'id': 1}"]
		self.assertQuerysetEqual(response.data,data)

