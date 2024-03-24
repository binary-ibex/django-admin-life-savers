from django import forms
from django.utils import timezone
from .models import Account


class WithdrawForm(forms.Form):

    amount = forms.IntegerField(
        min_value=0,
        required=True,
        help_text='How much to withdraw?',
    )

    def form_action(self, account, user):
        return Account.withdraw(
            id=account.pk,
            amount=self.cleaned_data['amount'],
            withdrawn_by=user,
            asof=timezone.now(),
        )

    def save(self, account, user):
        try:
            account = self.form_action(account, user)
        except Exception as e:
            error_message = str(e)
            self.add_error(None, error_message)
            raise
        return account


class DepositForm(forms.Form):

    amount = forms.IntegerField(
        min_value=0,
        required=True,
        help_text="How much to deposit?",
    )

    def form_action(self, account, user):
        return Account.deposit(
            id=account.pk,
            amount=self.cleaned_data['amount'],
            deposited_by=user,
            asof=timezone.now()
        )

    def save(self, account, user):
        account = self.form_action(account, user)
        return account