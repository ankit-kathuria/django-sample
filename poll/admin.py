from django.contrib import admin

from .models import Question, Choices

# Register your models here.

# admin.site.register(Question)
# admin.site.register(Choices)

class ChoicesInline(admin.TabularInline):
	model = Choices
	exclude = ['votes']
	extra = 3

class QuestionAdmin(admin.ModelAdmin):
	list_display = ('question_text', 'pub_date')
	list_filter = ['pub_date']
	search_fields = ['question_text']
	fieldsets = [
		(None, {'fields': ['question_text']})
	]
	inlines = [ChoicesInline]

admin.site.register(Question, QuestionAdmin)
