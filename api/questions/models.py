import datetime
from django.utils import timezone
from django.db import models
from operator import itemgetter

class Category(models.Model):
	cat_name = models.CharField(max_length=20,verbose_name='Category Name')

	def __unicode__(self):
		return self.cat_name

class Question(models.Model):
	statement = models.CharField(max_length=255)
	category = models.ForeignKey(Category)
	pub_date = models.DateTimeField('date published')

	def __unicode__(self):
		return "%s - %s" % (self.category, self.statement)

	def is_recent(self):
		now = timezone.now()
		return now - datetime.timedelta(days=1) <= self.pub_date <= now

class Opinion(models.Model):
	question = models.ForeignKey(Question)	

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
		(STRONGLY_DISAGREE, 'Strongly Agree')
	)
	#usage: op.vote = Opinion.NEUTRAL

	vote = models.IntegerField(default=0, choices=OPINIONS)

	def __unicode__(self):
		return "%s" % map(itemgetter(1),Opinion.OPINIONS)[self.vote + 2]
	
