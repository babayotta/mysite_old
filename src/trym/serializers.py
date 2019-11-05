from rest_framework import serializers
from trym.models import Transaction


class TransactionSerializer(serializers.Serializer):
    date = serializers.DateField()
    description = serializers.CharField(max_length=300)
    value = serializers.FloatField()
    transaction_type = serializers.CharField(max_length=1)
    user_id = serializers.IntegerField()

    def create(self, validated_data):
        return Transaction.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.date = validated_data.get('date', instance.date)
        instance.description = validated_data.get('description', instance.description)
        instance.value = validated_data.get('value', instance.value)
        instance.transaction_type = validated_data.get('transaction_type', instance.transaction_type)
        instance.user_id = validated_data.get('', instance.user_id)

        instance.save()
        return instance
