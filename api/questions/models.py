import datetime
from django.utils import timezone
from django.db import models
from django.db.models import Count

MAX_POPULAR=10

class Category(models.Model):
	cat_name = models.CharField(max_length=20,verbose_name='Category Name')

	def __unicode__(self):
		return self.cat_name

class QuestionManager(models.Manager):
	def get_queryset(self):
		return QuestionQuerySet(self.model, using=self._db)

	def most_opinions(self):
		return self.get_queryset().most_opinions(MAX_POPULAR)

	def recent_questions(self):
		return self.get_queryset().recent_questions()

	def popular(self):
		return self.get_queryset().recent_questions().most_opinions(MAX_POPULAR)

class QuestionQuerySet(models.query.QuerySet):
	def count_opinion(self):
		return self.annotate(count_opinion=models.Count('opinions'))
 
	def most_opinions(self, count):
		"""
		The <count> questions with the most opinions.
		"""
		return self.count_opinion().order_by('-count_opinion')[:count]
 
	def recent_questions(self):
		now = timezone.now()
		previousDay = now - datetime.timedelta(days=1) 
		return self.filter(pub_date__range=(previousDay, now))



class Question(models.Model):
	statement = models.CharField(max_length=255)
	category = models.ForeignKey(Category)
	pub_date = models.DateTimeField('date published')
	objects = QuestionManager()

	def __unicode__(self):
		return "%s - %s" % (self.category, self.statement)

	def is_recent(self):
		"""
		Find out if the Question was asked recently or not
		"""
		now = timezone.now()
		return now - datetime.timedelta(days=1) <= self.pub_date <= now


	def get_opinion_counts(self):
		"""
		Retrieve the number of votes for each type of Opinion,
		Note: might not include an opinion
		"""
		votes = self.opinions.values('vote').annotate(total=Count('vote')).order_by()
		indexed = {}
		for v in votes:
			indexed[v['vote']] = v['total']
		#Human readable would be something like this: [(Opinion.vote_string(x), q.get_opinion_counts()[x] ) for x in q.get_opinion_counts()]
		return indexed

	def get_human_opinion_counts(self):
		votes = self.get_opinion_counts()
		return ' ,'.join( ["%s : %d" % (Opinion.vote_string(x), votes[x] ) for x in votes] )

	def get_json_friendly_counts(self):
		votes = self.get_opinion_counts()
		keys = [o[0] for o in Opinion.OPINIONS]
		output = {}
		for key in keys:
			if key not in votes:
				votes[key] = 0
				output[Opinion.vote_string(key)] = 0
			else:
				output[Opinion.vote_string(key)] = votes[key]
		return output

	#Admin Settings
	get_human_opinion_counts.short_description = 'Opinion Vote Count'

	is_recent.admin_order_field = 'pub_date'
	is_recent.boolean = True
	is_recent.short_description = 'Published recently?'


class Opinion(models.Model):
	question = models.ForeignKey(Question, related_name='opinions')	

	STRONGLY_DISAGREE = -2
	DISAGREE = -1
	NEUTRAL = 0
	AGREE = 1
	STRONGLY_AGREE = 2
	OPINIONS = (
		(STRONGLY_DISAGREE, 'Strongly Disagree'),
		(DISAGREE, 'Disagree'),
		(NEUTRAL, 'Neutral'),
		(AGREE, 'Agree'),
		(STRONGLY_AGREE, 'Strongly Agree')
	)
	#usage: op.vote = Opinion.NEUTRAL

	vote = models.IntegerField(default=0, choices=OPINIONS)

	ip_addr = models.CharField(max_length=64, default="127.0.0.1",null=True, blank=True)
	#max is 45 +\0 chars according to headers
	#null and blank is true since we need to validate with a serializer and will
	#set the value serverside anyway

	def __unicode__(self):
		return Opinion.vote_string(self.vote)

	@classmethod
	def vote_string(cls, numeric_vote):
		strs = [op[1] for op in Opinion.OPINIONS if op[0] == numeric_vote]
		return "%s" % strs[0] if len(strs) > 0 else 'Invalid'
	
