from django.shortcuts import render

# Create your views here.
from .serializers import CitizenSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny
from .serializers import MyTokenObtainPairSerializer
from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework import generics, permissions

from .models import ChatGroup
from .serializers import ChatGroupSerializer




class MyTokenObtainPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer

# class CitizenCreateAPIView(generics.CreateAPIView):
#     serializer_class = CitizenSerializer

# class CitizenCreateAPIView(generics.CreateAPIView):
#     serializer_class = CitizenSerializer

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             self.perform_create(serializer)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class CitizenCreateAPIView(generics.CreateAPIView):
    serializer_class = CitizenSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Check if user already exists by username and full name
            username = serializer.validated_data.get('phone_number')
            full_name = serializer.validated_data.get('full_name')
            User = get_user_model()
            if User.objects.filter(username=username).exists() or User.objects.filter(full_name=full_name).exists():
                return Response({"error": "User with this username or full name already exists."}, status=status.HTTP_400_BAD_REQUEST)
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



from .models import ChatGroup
from .serializers import GroupSerializer
from rest_framework.views import APIView


class GroupCreateAPIView(APIView):
    def post(self, request, format=None):
        serializer = GroupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # Save the group with an empty members list
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

from .serializers import  MessageSerializer
from django.core.files.base import ContentFile
import os


from django.core.files.base import ContentFile
import os

from django.core.files.base import ContentFile
from rest_framework import status
from django.core.files.base import ContentFile
import base64

class MessageCreateAPIView(APIView):

    def post(self, request, format=None):
        # Get the request data
        data = request.data.copy()  # Make a copy of the mutable QueryDict
        print(data)  # For debugging purposes

        # Extract file content and name from the request data
        file_content = data.pop('file_content', None)
        file_name = data.pop('file_name', None)

        # If file content exists, decode and create a ContentFile from it
        if file_content and file_name:
            try:
                # Decode the base64 encoded file content. Remove brackets around file_content.
                decoded_content = base64.b64decode(file_content[0])
                file_data = ContentFile(decoded_content, name=file_name[0])
                data['file'] = file_data

            except Exception as e:
                # Handle any exceptions and return an error response
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Serialize the data
        serializer = MessageSerializer(data=data)

        # Validate and save the serialized data
        if serializer.is_valid():
            # Assuming request.user is properly set and available
            serializer.save(sender=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        # Return validation errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from django.shortcuts import get_object_or_404

class ChatGroupMessagesAPIView(APIView):
    def get(self, request, group_id, format=None):
        group = get_object_or_404(ChatGroup, pk=group_id)
        messages = group.messages.all()
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)
    


class UserChatGroupListView(generics.ListAPIView):
    serializer_class = ChatGroupSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ChatGroup.objects.filter(members=self.request.user)
    


# from rest_framework import viewsets
# from .models import Shapefile
# from .serializers import ShapefileSerializer
# from rest_framework.decorators import action
# from rest_framework.response import Response
# import shapefile as pyshp  # Import the pyshp library
# import json
# class ShapefileViewSet(viewsets.ModelViewSet):
#     queryset = Shapefile.objects.all()
#     serializer_class = ShapefileSerializer

#     @action(detail=True, methods=['get'])
#     def data(self, request, pk=None):
#         shapefile_instance = self.get_object()
#         try:
#             with open(shapefile_instance.shp_file.path, 'rb') as shp:
#                 reader = pyshp.Reader(shp=shp)
#                 features = []
#                 for shape in reader.shapes():
#                     geom = shape.__geo_interface__
#                     features.append(dict(type="Feature", geometry=geom, properties={}))
#                 return Response({
#                     'type': 'FeatureCollection',
#                     'features': features,
#                 })
#         except Exception as e:
#             return Response({"error": str(e)}, status=500)
    
# from rest_framework.decorators import api_view

# @api_view(['GET'])
# def list_shapefiles(request):
#     shapefiles = Shapefile.objects.all()
#     data = [{'id': shapefile.id, 'name': shapefile.name} for shapefile in shapefiles]
#     return Response(data)

# # views.py
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Shapefile
from .serializers import ShapefileSerializer
from .custom_shp_reader import CustomShapefileReader
from shapely.geometry import mapping

# class ShapefileListView(APIView):
#     def get(self, request):
#         shapefiles = Shapefile.objects.all()
#         polygons = []

#         for shapefile_instance in shapefiles:
#             try:
#                 reader = CustomShapefileReader(shapefile_instance.shp_file.path)
#                 reader.read()
#                 shapes = reader.get_shapes()

#                 # Convert shapes to latitude and longitude
#                 transformed_shapes = reader.convert_to_latlon()

#                 for shape in transformed_shapes:
#                     if shape.geom_type == 'Polygon':
#                         polygons.append(mapping(shape))
#             except Exception as e:
#                 return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
#         return Response(polygons, status=status.HTTP_200_OK)



class GeoJSONListView(generics.ListAPIView):
    serializer_class = ShapefileSerializer

    def get_queryset(self):
        # Assuming you want to fetch the latest uploaded shapefile
        shapefile_instance = Shapefile.objects.latest('uploaded_at')
        return [shapefile_instance]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)