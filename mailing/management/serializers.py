from rest_framework import serializers
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from management.models import Client, Mailing, Message

from django.contrib.auth.models import User


class ClientAPISerializer(serializers.ModelSerializer):
    """ Client serializer """
    operator_code = serializers.CharField(read_only=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Client
        fields = ('__all__')


class MessageAPISerializer(serializers.ModelSerializer):
    """ Message serializer """
    class Meta:
        model = Message
        fields = ('__all__')


class MailingAPISerializer(serializers.ModelSerializer):
    """ Mailing serializer """
    all_messages = serializers.IntegerField(read_only=True)
    wait_messages = serializers.IntegerField(read_only=True)
    sent_messages = serializers.IntegerField(read_only=True)
    lost_messages = serializers.IntegerField(read_only=True)
    error_messages = serializers.IntegerField(read_only=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Mailing
        fields = ('id', 'user', 'date_time_start_sending', 'text', 'filter_operator_code', 'filter_tag', 'date_time_end_sending',
                  'active', 'all_messages', 'wait_messages', 'sent_messages', 'lost_messages', 'error_messages')
