from rest_framework import serializers
from .models import Mess,MembershipRequest


class MessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mess
        fields = ['id', 'name', 'location', 'description', 'manager', 'created_at']
        read_only_fields = ['manager', 'created_at']



class MembershipSendSerializer(serializers.ModelSerializer):
    """
    Serializer for MembershipRequest.
    """
    class Meta:
        model = MembershipRequest
        fields = ['id', 'user', 'mess', 'status', 'created_at']
        read_only_fields = ['user', 'status', 'created_at']


class MembershipRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = MembershipRequest
        fields = ['id', 'user', 'status', 'created_at']
        read_only_fields = ['user', 'created_at']
