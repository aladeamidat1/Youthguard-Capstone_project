from rest_framework import serializers
from decimal import Decimal
from .models import MicroTask, TaskSubmission, Wallet, Transaction


class MicroTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = MicroTask
        fields = ['id', 'created_by', 'title', 'description', 'task_type', 'reward', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']


class TaskSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskSubmission
        fields = ['id', 'task', 'user', 'submission', 'status', 'submitted_at']
        read_only_fields = ['id', 'submitted_at']


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['user', 'balance']


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['wallet', 'amount', 'type', 'timestamp', 'description']
        read_only_fields = ['timestamp']