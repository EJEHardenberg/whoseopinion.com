import datetime
from django.test import TestCase
from rest_framework.test import APITestCase
from django.utils import timezone
from django.core.urlresolvers import reverse

from questions.models import Question,Opinion,Category

#A couple helpers
def create_category(cat_name):
	"""
	Creates a category for use in testing
	"""
	return Category.objects.create(cat_name=cat_name)

def create_question(statement, category):
	"""
	Creates a question for use in testing, must pass in category
	"""
	return Question.objects.create(statement=statement, category=category, pub_date=timezone.now())

def create_opinion(vote, question):
	"""
	Creates an opinion for a question with the specifid vote
	"""
	return Opinion.objects.create(vote=vote,question=question)


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

	def test_get_opinion_counts_with_no_opinions(self):
		"""
		Result of get_opinion_counts when there are no opinions should
		be an empty dictonary
		"""
		question = create_question("Test Question", create_category("test"))
		votes = question.get_opinion_counts()
		self.assertEqual(len(votes), 0)

	def test_get_opinion_counts_with_opinions(self):
		"""
		Result should contain the number of opinions created for each 
		opinion choice
		"""
		question = create_question("Test Question", create_category("test"))
		create_opinion(Opinion.STRONGLY_DISAGREE, question)
		create_opinion(Opinion.STRONGLY_DISAGREE, question)
		create_opinion(Opinion.STRONGLY_AGREE, question)

		votes = question.get_opinion_counts()
		
		self.assertEqual(len(votes), 2) #Two types of opinions
		self.assertEqual(votes[Opinion.STRONGLY_DISAGREE], 2)
		self.assertEqual(votes[Opinion.STRONGLY_AGREE], 1)

	def test_get_opinion_counts_with_opinions_errors_on_bad_index(self):
		"""
		If you try to access an AGREE when the question had no agreements
		it will throw an exception. This test is an example of what not
		to do.
		"""

		question = create_question("Test Question", create_category("test"))
		create_opinion(Opinion.STRONGLY_DISAGREE, question)
		create_opinion(Opinion.STRONGLY_DISAGREE, question)
		create_opinion(Opinion.STRONGLY_AGREE, question)

		votes = question.get_opinion_counts()
		with self.assertRaises(KeyError):
			votes[Opinion.AGREE]



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


class QuestionViewTests(APITestCase):
	pass


