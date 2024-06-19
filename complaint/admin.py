from django.contrib import admin
from .models import Question, Answer, Complaint


admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Complaint)