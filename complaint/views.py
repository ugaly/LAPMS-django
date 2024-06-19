# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from .serializers import ComplaintSerializer

# class ComplaintCreateAPIView(APIView):
#     def post(self, request, format=None):
#         serializer = ComplaintSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




import json
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.http import JsonResponse
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from .serializers import ComplaintSerializer
from .models import Question, Answer, Complaint
from .serializers import QuestionSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from django.contrib.auth import get_user_model

User = get_user_model()




class ComplaintCreateAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, format=None):
        # Extract data from the request
        message = request.data.get('message')
        image = request.data.get('image')
        

        # Check if the message is provided
        if not message:
            return JsonResponse({'error': 'Message is required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Create a complaint object
        # complaint_data = {'message': message}

        created_by_id = request.user.id
       

        complaint_data = {
            'message': message,
            'created_by': created_by_id  # Pass the user's primary key
        }


        # Check if the image is provided
        if image:
            complaint_data['image'] = image

        serializer = ComplaintSerializer(data=complaint_data)
        # if serializer.is_valid():
        #     complaint = serializer.save()

        #     # Broadcast the new complaint data to WebSocket consumers
        #     channel_layer = get_channel_layer()
        #     async_to_sync(channel_layer.group_send)(
        #         'complaint_group',  # Group name for WebSocket consumers
        #         {
        #             'type': 'new_complaint',
        #             'complaint': serializer.data
        #         }
        #     )

        if serializer.is_valid():
            complaint = serializer.save()

            # Get serialized data with created_by username
            serialized_data = serializer.data
            # Replace created_by with created_by_username
            serialized_data['created_by'] = serializer.validated_data['created_by'].username

            # Broadcast the new complaint data to WebSocket consumers
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                'complaint_group',  # Group name for WebSocket consumers
                {
                    'type': 'new_complaint',
                    'complaint': serialized_data
                }
            )
            
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    




class QuestionCreateAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, format=None):
        # Extract data from the request
        message = request.data.get('message')
        image = request.data.get('image')
        
        # Check if the message is provided
        if not message:
            return JsonResponse({'error': 'Message is required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Create a question object
        created_by_id = request.user.id
        question_data = {
            'message': message,
            'created_by': created_by_id  # Pass the user's primary key
        }

        # Check if the image is provided
        if image:
            question_data['image'] = image

        serializer = QuestionSerializer(data=question_data)
        if serializer.is_valid():
            question = serializer.save()

            # Get serialized data with created_by username
            serialized_data = serializer.data
            # Replace created_by with created_by_username
            serialized_data['created_by'] = serializer.validated_data['created_by'].username

            # Broadcast the new question data to WebSocket consumers
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                'question_group',  # Group name for WebSocket consumers
                {
                    'type': 'new_question',
                    'question': serialized_data
                }
            )
            
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class ModelCountsViewSet(viewsets.ModelViewSet):
    def list(self, request):
        question_count = Question.objects.count()
        answer_count = Answer.objects.count()
        complaint_count = Complaint.objects.count()
        data = {
            'question_count': question_count,
            'complaint_count': complaint_count,
            'answer_count': answer_count,
            
        }
        return Response(data)
    



from .serializers import UserActivitySerializer
from django.db.models import Count

class UserActivityAPIView(APIView):
    def get(self, request):
        # Get users who have asked at least one question
        answered_users = User.objects.filter(question_creator__answers__isnull=False).distinct()

        # Get top 7 users with the most questions asked
        top_users = User.objects.annotate(num_questions=Count('question_creator')).order_by('-num_questions')[:7]

        response_data = {
            "answered_users_count": answered_users.count(),
            "top_users_with_most_questions": []
        }

        for user in top_users:
            latest_question = user.question_creator.order_by('-timestamp').first()
            serializer = UserActivitySerializer({
                "user_id": user.id,
                "username": user.username,
                "full_name": user.full_name,
                "phone_number": user.phone_number,
                "questions_asked": user.num_questions,
                "latest_question_asked": latest_question
            })
            response_data["top_users_with_most_questions"].append(serializer.data)

        return Response(response_data)
    



from rest_framework.decorators import api_view
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

@api_view(['POST'])
def post_answer(request):
    question_id = request.data.get('question_id')
    message = request.data.get('message')
    image = request.data.get('image')

    # Validate input and save answer
    if question_id and message:
        question = Question.objects.get(pk=question_id)
        answer = Answer.objects.create(question=question, message=message, image=image, respondent=request.user)
        
        # Get the channel layer
        channel_layer = get_channel_layer()
        
        # Broadcast new answer to WebSocket clients
        async_to_sync(channel_layer.group_send)("question_group", {
            'type': 'new_answer',
            'answer': {
                'id': answer.id,
                'question_id': answer.question.id,
                'message': answer.message,
                'respondent': answer.respondent.full_name,
                'created_at': answer.created_at.isoformat()
            }
        })
        return Response(status=status.HTTP_201_CREATED)
    else:
        return Response({'error': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)

