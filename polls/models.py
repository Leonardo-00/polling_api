from django.db import models
from django.contrib.auth import get_user_model

class Category(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    
    class Meta:
        verbose_name_plural = "Categories"
    
    def __str__(self):
        return self.name

class Poll(models.Model):
    question = models.CharField(max_length=255)
    created_by = models.ForeignKey("useraccounts.Account", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return self.question

class Choice(models.Model):
    poll = models.ForeignKey(Poll, related_name='choices', on_delete=models.CASCADE)
    text = models.CharField(max_length=100)
    
    def __str__(self):
        return self.text

class Vote(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, related_name="votes", on_delete=models.CASCADE)
    voted_by = models.ForeignKey("useraccounts.Account", on_delete=models.CASCADE)
    
    unique_together = (('poll', 'voted_by'),)
    
    def __str__(self):
        return f"{self.voted_by.username} voted '{self.choice.text}'"