from django.test import TestCase
from django.contrib.auth import get_user_model
from decimal import Decimal
from .models import MicroTask, TaskSubmission, Wallet, Transaction

User = get_user_model()

class MicroTaskTest(TestCase):
    def setUp(self):
        self.employer = User.objects.create_user(
            username='employer',
            email='employer@example.com',
            password='testpass123',
            is_employer=True
        )

    def test_create_microtask(self):
        task = MicroTask.objects.create(
            created_by=self.employer,
            title='Data Entry Task',
            description='Enter data from images',
            reward=Decimal('10.00')
        )
        self.assertEqual(task.title, 'Data Entry Task')
        self.assertEqual(task.created_by, self.employer)
        self.assertEqual(task.reward, Decimal('10.00'))

class WalletTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_create_wallet(self):
        wallet = Wallet.objects.create(user=self.user)
        self.assertEqual(wallet.user, self.user)
        self.assertEqual(wallet.balance, Decimal('0.00'))

    def test_wallet_transaction(self):
        wallet = Wallet.objects.create(user=self.user)
        transaction = Transaction.objects.create(
            wallet=wallet,
            amount=Decimal('50.00'),
            type='credit',
            description='Task completion reward'
        )
        self.assertEqual(transaction.wallet, wallet)
        self.assertEqual(transaction.amount, Decimal('50.00'))
        self.assertEqual(transaction.type, 'credit')
