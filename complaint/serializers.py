from rest_framework import serializers
from .models import Complaint, Question, Answer

class ComplaintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complaint
        fields = ['message', 'image','created_by', 'created_time', 'created_date', 'timestamp']


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['message', 'image', 'created_by', 'created_time', 'created_date', 'timestamp']
        




class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'

class ComplaintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complaint
        fields = '__all__'


# from rest_framework import serializers
# from django.utils import timezone
# from .models import Complaint

# class ComplaintSerializer(serializers.ModelSerializer):
#     created_time = serializers.SerializerMethodField()

#     class Meta:
#         model = Complaint
#         fields = ['message', 'image', 'created_by', 'created_time']

#     def get_created_time(self, obj):
#         now = timezone.now()
#         time_diff = now - obj.created_time

#         if time_diff.total_seconds() < 60:
#             return 'now'
#         elif time_diff.total_seconds() < 3600:
#             minutes = int(time_diff.total_seconds() / 60)
#             return f'{minutes} {"minute" if minutes == 1 else "minutes"} ago'
#         elif time_diff.total_seconds() < 86400:
#             hours = int(time_diff.total_seconds() / 3600)
#             return f'{hours} {"hour" if hours == 1 else "hours"} ago'
#         elif time_diff.total_seconds() < 604800:
#             days = int(time_diff.total_seconds() / 86400)
#             return f'{days} {"day" if days == 1 else "days"} ago'
#         elif time_diff.total_seconds() < 2628000:
#             weeks = int(time_diff.total_seconds() / 604800)
#             return f'{weeks} {"week" if weeks == 1 else "weeks"} ago'
#         elif time_diff.total_seconds() < 31536000:
#             months = int(time_diff.total_seconds() / 2628000)
#             return f'{months} {"month" if months == 1 else "months"} ago'
#         else:
#             years = int(time_diff.total_seconds() / 31536000)
#             return f'{years} {"year" if years == 1 else "years"} ago'






# serializers.py



class LatestQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('id', 'message', 'created_date', 'created_by')

# class UserActivitySerializer(serializers.Serializer):
#     user_id = serializers.IntegerField()
#     username = serializers.CharField()
#     full_name = serializers.CharField()
#     phone_number = serializers.CharField()
#     questions_asked = serializers.IntegerField()
#     latest_question_asked = LatestQuestionSerializer()



#     def get_latest_question_asked(self, obj):
#         latest_question = obj['latest_question_asked']
#         if len(latest_question['message']) > 20:
#             latest_question['message'] = latest_question['message'][:20] + "..."
#         return latest_question


class UserActivitySerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    username = serializers.CharField()
    full_name = serializers.CharField()
    phone_number = serializers.CharField()
    questions_asked = serializers.IntegerField()
    latest_question_asked = serializers.SerializerMethodField()  # Bind method to the field

    def get_latest_question_asked(self, obj):
        latest_question = obj['latest_question_asked']
        if isinstance(latest_question, dict):
            if len(latest_question['message']) > 20:
                latest_question['message'] = latest_question['message'][:40] + "..."
            return latest_question
        elif isinstance(latest_question, Question):
            latest_question_data = LatestQuestionSerializer(latest_question).data
            if len(latest_question_data['message']) > 20:
                latest_question_data['message'] = latest_question_data['message'][:40] + "..."
            return latest_question_data
        else:
            return None  # Handle other cases gracefully, like when latest_question_asked is None
