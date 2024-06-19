# from django.urls import path
# from .views import CitizenCreateAPIView, GroupCreateAPIView, ChatGroupMessagesAPIView, MessageCreateAPIView, UserChatGroupListView, ShapefileViewSet, list_shapefiles
# from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register(r'shapefiles', ShapefileViewSet)

# urlpatterns = [
#     path('citizens/', CitizenCreateAPIView.as_view(), name='create-citizen'),

#     path('groups/create/', GroupCreateAPIView.as_view(), name='group-create'),

#      path('chatgroups/<int:group_id>/messages/', ChatGroupMessagesAPIView.as_view(), name='chatgroup-messages'),
#     path('messages/', MessageCreateAPIView.as_view(), name='message-create'),
#      path('user-chat-groups/', UserChatGroupListView.as_view(), name='user-chat-groups'),

#     path('shapefiles/', ShapefileViewSet.as_view({'get': 'list'}), name='shapefiles'),

#     path('list-shapefiles/', list_shapefiles, name='list-shapefiles'),
# ]
# urlpatterns += router.urls



from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import CitizenCreateAPIView, GroupCreateAPIView, ChatGroupMessagesAPIView, MessageCreateAPIView, UserChatGroupListView,GeoJSONListView

# router = DefaultRouter()
# router.register(r'shapefiles', ShapefileViewSet)

urlpatterns = [
    path('citizens/', CitizenCreateAPIView.as_view(), name='create-citizen'),
    path('groups/create/', GroupCreateAPIView.as_view(), name='group-create'),
    path('chatgroups/<int:group_id>/messages/', ChatGroupMessagesAPIView.as_view(), name='chatgroup-messages'),
    path('messages/', MessageCreateAPIView.as_view(), name='message-create'),
    path('user-chat-groups/', UserChatGroupListView.as_view(), name='user-chat-groups'),
    # path('list-shapefiles/', list_shapefiles, name='list-shapefiles'),
   path('geojson/', GeoJSONListView.as_view(), name='geojson-list'),
]

# urlpatterns += router.urls
