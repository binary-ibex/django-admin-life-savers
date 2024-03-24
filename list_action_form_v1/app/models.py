from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    asof = models.DateTimeField(null=True, blank=True, default=timezone.now)
    last_deposited_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="last_deposit_account", null=True, blank=True)
    last_withdrawn_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="last_withdraw_account",null=True, blank=True)

    def __str__(self) -> str:
        return str(self.user.first_name)
    
    @staticmethod
    def deposit(id, amount, deposited_by, asof):
        account = Account.objects.get(id=id)
        account.balance += amount
        account.last_deposited_by = deposited_by
        account.asof = asof
        account.save()
        return account
    
    @staticmethod
    def withdraw(id, amount, withdrawn_by, asof):
        account = Account.objects.get(id=id)
        if account.balance < amount:
            raise ValueError("Insufficient balance")
        account.balance -= amount
        account.last_withdrawn_by = withdrawn_by
        account.asof = asof
        account.save()
        return account 
