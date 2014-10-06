from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import requires_csrf_token,ensure_csrf_cookie

from questions.models import Opinion,Question,Category
from questions.serializers import OpinionSerializer,QuestionSerializer,CategorySerializer

from api import settings
import logging
logger = logging.getLogger(__name__)

from ipware.ip import get_ip
from django.contrib.gis.geoip import GeoIP


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

		output['states'] = question.get_json_friendly_usa_state_counts()
		output['totals'] = totals
		content = JSONRenderer().render(output)
		return Response(content)

	"""
	Count a vote towards an opinion on a question.
	Note: This needs work for ensuring no duplicate votes as best as possible
	"""
	@method_decorator(requires_csrf_token)
	def post(self, request, question_pk, format=None):
		geo = GeoIP(settings.GEOIP_PATH, settings.GEOIP_CACHE_SETTING)
		ip = get_ip(request)
		if ip is None:
			logger.debug("No IP Address given in post")

		if settings.DEBUG and ip == '127.0.0.1':
			ip = '72.15.24.78'


		serializer = OpinionSerializer(data=request.DATA)

		questionIdsMatch = int(question_pk) == int(request.DATA['question'])
		if serializer.is_valid() and questionIdsMatch and ip:
			serializer.object.ip_addr = ip
			#Retrieve information for the objects IP adress
			ipData = geo.city(ip)
			if not ipData:
				return Response({u'error' : u'Could not lookup location data for your IP'},status=status.HTTP_400_BAD_REQUEST)

			serializer.object.country_code = ipData.get('country_code')
			serializer.object.region = ipData.get('region')

			try:
				serializer.object.clean_fields()
			except ValidationError, e:
				return Response(e,status=status.HTTP_400_BAD_REQUEST)
			
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)

		if 'question' in request.DATA and question_pk == request.DATA['question']:
			if not Question.objects.filter(pk=question_pk):
				return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def if_header_exists(request, header):
	return request.META[header] if header in request.META else ''


@ensure_csrf_cookie
def get_auth(request):
	host = if_header_exists(request, 'HTTP_HOST')
	agent = if_header_exists(request, 'HTTP_USER_AGENT')
	ref = if_header_exists(request, 'HTTP_REFERER')
	content_type= if_header_exists(request, 'CONTENT_TYPE')
	logger.debug("New Auth %s %s %s %s" % (host, agent, ref, content_type))
	return HttpResponse(u"{'heartbeat' : '%s' }" % timezone.now(),content_type='application/json')

def get_popular(request):
	questions = Question.objects.popular()
	serializer = QuestionSerializer(questions, many=True)
	content= JSONRenderer().render(serializer.data)
	return HttpResponse(content, content_type='application/json')