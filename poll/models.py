from __future__ import unicode_literals

from django.db import models

# Create your models here.

# class User(models.Model):
# 	email = models.CharField(max_length=60)
# 	password = models.CharField(max_length=255)

class Question(models.Model):
    question_text = models.CharField(max_length=300)
    pub_date = models.DateTimeField('date published')
    # pub_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
    	return str(self.id) + self.question_text

class Choices(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=60)
    votes = models.IntegerField(default=0)

# class Voted(models.Model):
# 	question = models.ForeignKey(Question, on_delete=models.CASCADE)
# 	user = models.ForeignKey(User, on_delete=models.CASCADE)
