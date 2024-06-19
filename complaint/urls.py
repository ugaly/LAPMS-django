from django.urls import path
from .views import ComplaintCreateAPIView, QuestionCreateAPIView, ModelCountsViewSet, UserActivityAPIView, post_answer

urlpatterns = [
    path('complaints/', ComplaintCreateAPIView.as_view(), name='complaint-create'),
    path('questions/', QuestionCreateAPIView.as_view(), name='question-create'),
    path('model_count/', ModelCountsViewSet.as_view({'get': 'list'}), name='model_count'),
    path('user_activity/', UserActivityAPIView.as_view(), name='user_activity'),
    path('post_answer/', post_answer, name='post_answer'),
]
