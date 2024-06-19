from django.db import models
from django.contrib.auth import get_user_model
from django_currentuser.db.models import CurrentUserField



User = get_user_model()

class Question(models.Model):
    created_date = models.DateField(auto_now_add=True)
    created_time = models.TimeField(auto_now_add=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    created_by = CurrentUserField(related_name='question_creator')
    updated_date = models.DateField(auto_now=True)
    updated_time = models.TimeField(auto_now=True)
    updated_by = CurrentUserField(on_update=True, related_name='question_updater')
    deleted = models.BooleanField(default=False)

    # sender = models.ForeignKey(User, related_name='sent_question', on_delete=models.CASCADE)
    # receiver = models.ForeignKey(User, related_name='received_question', on_delete=models.CASCADE)
    message = models.TextField()
    image = models.ImageField(upload_to='question_images/', blank=True, null=True)
    



    def __str__(self):
        return f"Question: {self.message}"




class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    respondent = CurrentUserField(related_name='answe_creator')
    message = models.TextField()
    image = models.ImageField(upload_to='answer_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True, blank=True)


    def __str__(self):
        return f"Answer: {self.message} by {self.respondent}"
    


class Complaint(models.Model):
    created_date = models.DateField(auto_now_add=True)
    created_time = models.TimeField(auto_now_add=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    created_by = CurrentUserField(related_name='complaint_creator')
    updated_date = models.DateField(auto_now=True)
    updated_time = models.TimeField(auto_now=True)
    updated_by = CurrentUserField(on_update=True, related_name='complaint_updater')
    deleted = models.BooleanField(default=False)

    message = models.TextField()
    image = models.ImageField(upload_to='complaint_images/', blank=True, null=True)

    def __str__(self):
        return f"Complaint: {self.message}"
    