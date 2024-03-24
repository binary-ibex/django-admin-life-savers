from django.contrib import admin
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from app.forms import DepositForm, WithdrawForm
from .models import Account
from django.urls import path
from django.utils.html import format_html
from django.urls import reverse
from django.contrib import messages


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    date_heirarchy = (
        'asof',
    )
    list_display = (
        'id',
        'user',
        'balance',
        'asof',
        'account_actions'
    )
    readonly_fields = (
        'id',
        'asof',
        'balance',
        'account_actions'
    )
    list_select_related = (
        'user',
    )
    fields = [
        'user',
        'balance',
        'asof',
        'last_withdrawn_by',
        'last_deposited_by',
    ]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                '<str:account_id>/deposit/',
                self.admin_site.admin_view(self.process_deposit),
                name='account-deposit',
            ),
            path(
                '<str:account_id>/withdraw/',
                self.admin_site.admin_view(self.process_withdraw),
                name='account-withdraw',
            ),
        ]
        return custom_urls + urls

    def account_actions(self, obj):
        return format_html(
            '<a class="button" href="{}">Deposit</a>&nbsp;'
            '<a class="button" href="{}">Withdraw</a>',
            reverse('admin:account-deposit', args=[obj.pk]),
            reverse('admin:account-withdraw', args=[obj.pk]),
        )

    account_actions.short_description = 'Account Actions'
    account_actions.allow_tags = True

    def process_deposit(self, request, account_id, *args, **kwargs):
        return self.process_action(
            request=request,
            account_id=account_id,
            action_form=DepositForm,
            action_title='Deposit',
        )

    def process_withdraw(self, request, account_id, *args, **kwargs):
        return self.process_action(
            request=request,
            account_id=account_id,
            action_form=WithdrawForm,
            action_title='Withdraw',
        )

    def process_action(self,request,account_id,action_form,action_title):
        account = self.get_object(request, account_id)
        if request.method != 'POST':
            form = action_form()
        else:
            form = action_form(request.POST)
            if form.is_valid():
                try:
                    form.save(account, request.user)
                except Exception as e:
                    messages.error(request, e)
                else:
                    self.message_user(request, 'Success')
                    url = reverse(
                        'admin:app_account_changelist',
                        current_app=self.admin_site.name,
                    )
                    return HttpResponseRedirect(url)
        context = self.admin_site.each_context(request)
        context['opts'] = self.model._meta
        context['form'] = form
        context['account'] = account
        context['title'] = action_title

        return TemplateResponse(
            request,
            'admin/app/account_action.html',
            context,
        )

