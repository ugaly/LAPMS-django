from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Message, ChatGroup, SystemUser, Shapefile


User = get_user_model()


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def get_token(self, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['full_name'] = user.full_name
        token['phone_number'] = user.phone_number
        token['is_citizen'] = user.is_citizen
        token['is_landvaluer'] = user.is_landvaluer
        token['is_indemnity_payer'] = user.is_indemnity_payer
        token['is_landofficer'] = user.is_landofficer
        token['is_admin'] = user.is_admin
        token['thumbnail'] = user.thumbnail.url if user.thumbnail else None

        return token

class CitizenSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'full_name', 'phone_number', 'email', 'password', 'is_citizen']

    def create(self, validated_data):
        user = User.objects.create_user(
            full_name=validated_data['full_name'],
            phone_number=validated_data['phone_number'],
            email=validated_data['email'],
            password=validated_data['password'],
            username=validated_data['phone_number'],
            is_citizen=True
        )
        return user




from .models import ChatGroup, SystemUser
from rest_framework import serializers



class GroupSerializer(serializers.ModelSerializer):
    members = serializers.PrimaryKeyRelatedField(queryset=SystemUser.objects.all(), many=True, required=False)

    class Meta:
        model = ChatGroup
        fields = ['id', 'name', 'members']

    def create(self, validated_data):
        # Get all users with is_landvaluer set to True
        landvaluers = SystemUser.objects.filter(is_landvaluer=True)
        # Get all users with is_citizen set to True
        citizens = SystemUser.objects.filter(is_citizen=True)
        
        # Extract members from validated_data if present, otherwise initialize as an empty list
        members = validated_data.pop('members', [])

        # Add all landvaluers and citizens to the members list
        members.extend(landvaluers)
        members.extend(citizens)

        # Create the group
        group = ChatGroup.objects.create(**validated_data)

        # Add all members to the group
        group.members.set(members)

        return group
    


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'chat_group', 'sender', 'text', 'file', 'timestamp']




class ChatGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatGroup
        fields = ['id', 'name', 'members', 'thumbnailUrl']
        read_only_fields = ['members']


# serializers.py
from rest_framework import serializers
from django.contrib.gis.gdal import DataSource
from geojson import Feature, FeatureCollection, Polygon

class ShapefileSerializer(serializers.Serializer):
    def to_representation(self, shapefile_instance):
        try:
            # Open the uploaded shapefile data source
            ds = DataSource(shapefile_instance.shp_file.path)
            
            # Initialize a list to store GeoJSON features
            features = []
    
            # Iterate over each feature in the shapefile
            for layer in ds:
                for feature in layer:
                    geom = feature.geom
                    polygons = []
                    
                    # Convert each geometry (polygon) to GeoJSON format
                    for i in range(len(geom)):
                        rings = geom[i].tuple
                        polygon = []
                        for ring in rings:
                            coords = [(ring[j][0], ring[j][1]) for j in range(len(ring))]
                            polygon.append(coords)
                        polygons.append(polygon)
                    
                    # Create a GeoJSON feature and add to the features list
                    geojson_feature = Feature(geometry=Polygon(polygons), properties={})
                    features.append(geojson_feature)
    
            # Create a GeoJSON feature collection
            feature_collection = FeatureCollection(features)
    
            return feature_collection

        except Exception as e:
            raise serializers.ValidationError(str(e))
