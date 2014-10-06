import datetime,json
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase

from StringIO import StringIO
from rest_framework.parsers import JSONParser

from django.utils import timezone
from django.core.urlresolvers import reverse
from django.test import Client

from django.contrib.gis.geoip import GeoIP

from questions.models import Question,Opinion,Category

#A couple helpers
def create_category(cat_name):
	"""
	Creates a category for use in testing
	"""
	return Category.objects.create(cat_name=cat_name)

def create_question(statement, category, pub_date=timezone.now()):
	"""
	Creates a question for use in testing, must pass in category
	"""
	return Question.objects.create(statement=statement, category=category, pub_date=timezone.now())

def create_opinion(vote, question, region=u'CA'):
	"""
	Creates an opinion for a question with the specifid vote
	"""
	return Opinion.objects.create(vote=vote,question=question,country_code=u'US',region=region)


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

	def test_get_json_friendly_usa_state_counts(self):
		"""
		Test that the result of the json is aggregated by state correctly and 
		by votes so that we get back a list of items who specify state and totals
		"""

		question = create_question("Test Aggregation", create_category("test"))
		states = ['VT','NH','MA','TX','GA','CA','WA','NC']
		for region in states:
			for opinion in Opinion.OPINIONS:
				create_opinion(opinion[0], question, region )

		#We strongly disagree with CA, for testing the majority key
		create_opinion(Opinion.STRONGLY_DISAGREE, question, 'CA' )

		results = question.get_json_friendly_usa_state_counts()
		#Assert key structure and that there are states.length items, with 1 vote each
		self.assertEqual(len(results), len(states))
		for result in results:
			self.assertTrue(result.get('totals'))
			if result.get('state') == 'US-CA':
				self.assertEqual(result.get('majority'), Opinion.vote_string(Opinion.STRONGLY_DISAGREE) )
			else:
				self.assertEqual(result.get('majority'), Question.MAJORITY_INCONCLUSIVE )
			totals = result.get('totals')
			self.assertEqual(len(totals), len(Opinion.OPINIONS))
			for vote in totals:
				if result.get('state') == 'US-CA':
					#majority vote in this test data so we have 4 1's and a 2.
					ones = [i for i in totals if i.get('votes') == 1]
					self.assertEqual(len(ones), 4 )
				else:
					self.assertEqual(vote.get('votes'), 1)

		


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
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertQuerysetEqual(response.data,[])

	def test_populated_index_listing(self):
		"""
		Test categories view when categories exist
		"""
		create_category("test")
		response = self.client.get(reverse('questions:categories'))
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		data = ["{'cat_name': u'test', 'id': 1}"]
		self.assertQuerysetEqual(response.data,data)


class QuestionViewTests(APITestCase):
	
	def test_no_questions_category(self):
		"""
		When there are no questions in a category it should return an
		empty list
		"""
		category = create_category("test")
		response = self.client.get(reverse(
			'questions:questions_for_category',args=(category.id,)))
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertQuerysetEqual(response.data, [])

	def test_bad_category_id(self):
		"""
		When the category id passed does not match any in the database 
		we should 404
		"""
		response = self.client.get(reverse(
			'questions:questions_for_category',args=(333,)))
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

	def test_questions_in_category(self):
		"""
		When a category contains questions they should be returned
		"""
		category = create_category("test")
		q1 = create_question(statement='one', category=category)
		q2 = create_question(statement='two', category=category)

		data = [
			{ 'statement' : q1.statement, 'category' : category.id, 'id' : q1.id },
			{ 'statement' : q2.statement, 'category' : category.id, 'id' : q2.id }
		]
		response = self.client.get(reverse(
			'questions:questions_for_category', args=(category.id,)))

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(data[0]['statement'], response.data[0]['statement'])
		self.assertEqual(data[1]['statement'], response.data[1]['statement'])
		self.assertEqual(data[0]['category'], response.data[0]['category'])
		self.assertEqual(data[0]['id'], response.data[0]['id'])
		self.assertEqual(data[1]['category'], response.data[1]['category'])
		self.assertEqual(data[1]['id'], response.data[1]['id'])

class OpinionViewTests(APITestCase):

	def test_get_opinions_on_non_existent_question(self):
		"""
		When the GET request is called with an ID of a question that
		does not exist, then we should 404
		"""
		response = self.client.get(reverse(
			'questions:opinions_for_question', args=(333,)))
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

	def test_get_opinions_for_question_with_none(self):
		"""
		When we get opinions for a question that has no votes yet, all
		the fields should be zero.
		"""
		category = create_category("test")
		q = create_question(statement='one', category=category)

		response = self.client.get(reverse(
			'questions:opinions_for_question', args=(q.id,)))

		self.assertEqual(response.status_code, status.HTTP_200_OK)

		stream = StringIO(response.data)
		data = JSONParser().parse(stream)

		self.assertTrue('totals' in data)
		for total in data['totals']:
			count = total.get('votes')
			self.assertEqual(0, count)

	def test_get_opinions_for_question_with_votes(self):
		"""
		When we get opinions for a question that has votes, they should
		be there. 
		"""
		category = create_category('test')
		q = create_question(statement='test', category=category)


		strong_disagree = create_opinion(question=q, vote=Opinion.STRONGLY_DISAGREE)
		disagree = create_opinion(question=q, vote=Opinion.DISAGREE)
		neutral = create_opinion(question=q, vote=Opinion.NEUTRAL)
		agree = create_opinion(question=q, vote=Opinion.AGREE)
		strong_agree = create_opinion(question=q, vote=Opinion.STRONGLY_AGREE)

		response = self.client.get(reverse(
			'questions:opinions_for_question', args=(q.id,)))

		self.assertEqual(response.status_code, status.HTTP_200_OK)

		stream = StringIO(response.data)
		data = JSONParser().parse(stream)

		self.assertTrue('totals' in data)

		for total in data['totals']:
			count = total.get('votes')


			self.assertEqual(1, count)


	def test_create_opinion_on_non_existent_question(self):
		"""
		POSTing to opinions endpoint should 404 without a valid question 
		specified
		"""

		url = reverse('questions:opinions_for_question', args=(333,))
		data = {'question' : 333, 'vote' : Opinion.NEUTRAL }
		self.client = Client(enforce_csrf_checks=True)
		response = self.client.post(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

	def test_create_opinion_on_question(self):
		"""
		POSTing to opinions endpoint with valid
		"""

		self.assertEqual(list(Opinion.objects.all()),[])

		category = create_category('test')
		q = create_question(statement='test', category=category)

		url = reverse('questions:opinions_for_question', args=(q.id,))
		data = {'question' : q.id, 'vote' : Opinion.NEUTRAL }
		self.client = Client(enforce_csrf_checks=True)
		response = self.client.post(url, data, format='json',REMOTE_ADDR='8.8.8.8')
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(response.data, data)
		self.assertEqual(len(list(Opinion.objects.all())),1)

	def test_create_opinion_list_400_response(self):
		"""
		Test that POSTing to opinion_list without matching question id's 
		in the url and post data will return 400
		"""

		self.assertEqual(list(Opinion.objects.all()),[])

		category = create_category('test')
		q = create_question(statement='test', category=category)

		url = reverse('questions:opinions_for_question', args=(99999,))
		data = {'question' : q.id, 'vote' : Opinion.NEUTRAL }
		self.client = Client(enforce_csrf_checks=True)
		response = self.client.post(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

		self.assertEqual(list(Opinion.objects.all()),[])

	def test_creation_after_auth(self):
		"""
		requesting authentication should allow creation of an opinion 
		via the POST to opinions_for_question afterwards.
		"""

		response = self.client.get(reverse('questions:auth'))
		self.assertTrue('csrftoken' in self.client.cookies)

		csrf_token = self.client.cookies['csrftoken'].value

		category = create_category('test')
		q = create_question(statement='test', category=category)
		data = {'question' : q.id, 'vote' : Opinion.NEUTRAL }
		url = reverse('questions:opinions_for_question', args=(q.id,))

		mkResponse = self.client.post(url, data, format='json', cookies=self.client.cookies, REMOTE_ADDR='8.8.8.8')
		
		self.assertEqual(mkResponse.status_code, status.HTTP_201_CREATED)
		self.assertEqual(mkResponse.data, data)
		self.assertEqual(len(list(Opinion.objects.all())),1)

	def test_create_opinion_without_ip_addr(self):
		"""
		Attempting to create an adress without an ip_addr should fail
		"""
		response = self.client.get(reverse('questions:auth'))
		self.assertTrue('csrftoken' in self.client.cookies)

		csrf_token = self.client.cookies['csrftoken'].value

		category = create_category('test')
		q = create_question(statement='test', category=category)
		data = {'question' : q.id, 'vote' : Opinion.NEUTRAL }
		url = reverse('questions:opinions_for_question', args=(q.id,))

		mkResponse = self.client.post(url, data, format='json', cookies=self.client.cookies,REMOTE_ADDR='')

		self.assertEqual(mkResponse.status_code, status.HTTP_400_BAD_REQUEST)

	def test_create_opinion_with_invalid_ip_addr(self):
		"""
		Attempting to create an adress without an ip_addr should fail
		"""
		response = self.client.get(reverse('questions:auth'))
		self.assertTrue('csrftoken' in self.client.cookies)

		csrf_token = self.client.cookies['csrftoken'].value

		category = create_category('test')
		q = create_question(statement='test', category=category)
		data = {'question' : q.id, 'vote' : Opinion.NEUTRAL }
		url = reverse('questions:opinions_for_question', args=(q.id,))

		mkResponse = self.client.post(url, data, format='json', cookies=self.client.cookies,REMOTE_ADDR='this_is_not_a_real_ip_addr')

		self.assertEqual(mkResponse.status_code, status.HTTP_400_BAD_REQUEST)

	def test_create_opinion_with_invalid_ip_addr_again(self):
		"""
		Attempting to create an adress without an ip_addr should fail
		"""
		response = self.client.get(reverse('questions:auth'))
		self.assertTrue('csrftoken' in self.client.cookies)

		csrf_token = self.client.cookies['csrftoken'].value

		category = create_category('test')
		q = create_question(statement='test', category=category)
		data = {'question' : q.id, 'vote' : Opinion.NEUTRAL }
		url = reverse('questions:opinions_for_question', args=(q.id,))

		mkResponse = self.client.post(url, data, format='json', cookies=self.client.cookies,REMOTE_ADDR='127.0..2.1')

		self.assertEqual(mkResponse.status_code, status.HTTP_400_BAD_REQUEST)

	def test_create_opinion_with_an_ip_addr_thats_not_local(self):
		"""
		Attempting to create an adress without an ip_addr should not fail
		"""
		response = self.client.get(reverse('questions:auth'))
		self.assertTrue('csrftoken' in self.client.cookies)

		csrf_token = self.client.cookies['csrftoken'].value

		category = create_category('test')
		q = create_question(statement='test', category=category)
		data = {'question' : q.id, 'vote' : Opinion.NEUTRAL }
		url = reverse('questions:opinions_for_question', args=(q.id,))

		mkResponse = self.client.post(url, data, format='json', cookies=self.client.cookies,REMOTE_ADDR='8.8.8.8')

		self.assertEqual(mkResponse.status_code, status.HTTP_201_CREATED)

		op = Opinion.objects.get(question_id=q.id)

		self.assertEqual(op.ip_addr, '8.8.8.8')

	def test_create_opinion_with_an_ip_addr_thats_not_local(self):
		"""
		Attempting to create an opinion should record country/region data
		"""
		response = self.client.get(reverse('questions:auth'))
		self.assertTrue('csrftoken' in self.client.cookies)

		csrf_token = self.client.cookies['csrftoken'].value

		category = create_category('test')
		q = create_question(statement='test', category=category)
		data = {'question' : q.id, 'vote' : Opinion.NEUTRAL }
		url = reverse('questions:opinions_for_question', args=(q.id,))

		mkResponse = self.client.post(url, data, format='json', cookies=self.client.cookies,REMOTE_ADDR='8.8.8.8')

		self.assertEqual(mkResponse.status_code, status.HTTP_201_CREATED)

		op = Opinion.objects.get(question_id=q.id)

		self.assertEqual(op.ip_addr, '8.8.8.8')
		self.assertEqual(op.country_code, u'US')
		self.assertEqual(op.region, u'CA')





class AuthView(TestCase):

	def test_heartbeat_returned(self):
		"""
		Asking the auth endpoint for a heartbeat also serves back an authentication
		cookie.
		"""
		response = self.client.get(reverse('questions:auth'))
		self.assertTrue('csrftoken' in response.cookies)

class PopularQuestions(TestCase):

	def test_popular_questions(self):
		"""
		Requesting the popular questions returns question that have 
		many votes that are recent.
		"""
		category = create_category('test')
		q = create_question(statement='popular', category=category)
		for i in xrange(10):
			create_question(statement='not-popular-bulk', category=category)
		notPopular = create_question(statement='not-popular', category=category)

		time = timezone.now() - datetime.timedelta(days=30)
		q3 = create_question(statement='old', category=category,pub_date=time)

		for i in range(100):
			create_opinion(Opinion.STRONGLY_AGREE, q)
			create_opinion(Opinion.STRONGLY_DISAGREE, q)
			create_opinion(Opinion.STRONGLY_AGREE, q3)
			create_opinion(Opinion.STRONGLY_DISAGREE, q3)

		response = self.client.get(reverse('questions:popular'))

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		questions = response.content
		
		for question in json.loads(questions):
			self.assertFalse(question['statement'] == 'not-popular')