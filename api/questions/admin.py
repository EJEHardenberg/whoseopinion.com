from django.contrib import admin

from django.contrib import admin
from questions.models import Question, Category, Opinion

# Register your models here.
class Opinioninline(admin.TabularInline):
	model = Opinion
	extra = 1
	fk_name = 'question'

class QuestionAdmin(admin.ModelAdmin):
	fieldsets = [
		(None, {'fields' : ['statement', 'category']}),
		('Date information', {'fields' : ['pub_date'], 'classes': ['collapse']}),
	]
	list_display = ('statement', 'pub_date', 'is_recent', 'get_human_opinion_counts')
	list_filter = ['pub_date']
	search_fields = ['statement']

admin.site.register(Category)
admin.site.register(Question, QuestionAdmin)