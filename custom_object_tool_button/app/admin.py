from django.contrib import admin
from django.contrib import messages
from app.forms import AnnouncementForm
from .models import Notification
from django.template.response import TemplateResponse
from django.urls import path, reverse 
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User 
from django.db import transaction


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['title', 'body', 'user']
    allow_tags = True
    change_list_template = "admin/app/change_list.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                'announcement/',
                self.admin_site.admin_view(self.make_announcement),
                name='announcement',
            )
        ]
        return custom_urls + urls

    def make_announcement(self, request, *args, **kwargs):
        form = AnnouncementForm()
        context = self.admin_site.each_context(request)
        context['opts'] = self.model._meta
        context['form'] = form

        if request.method != 'POST':
            form = AnnouncementForm()
        else:
            form = AnnouncementForm(request.POST)
            if form.is_valid():
                try:
                    title = form.cleaned_data['title']
                    body = form.cleaned_data['body']      

                    # send the notification to all the user 
                    with transaction.atomic():
                        for user in  User.objects.all() :
                            Notification.objects.create(title=title, body=body, user=user)
                            
                except Exception as e:
                    messages.error(request, e)
                else:
                    self.message_user(request, 'Success')
                    url = reverse(
                        'admin:app_notification_changelist',
                        current_app=self.admin_site.name,
                    )
                    return HttpResponseRedirect(url)
        
        return TemplateResponse(
            request,
            'admin/app/app_action.html',
            context,
        )

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['custom_form_link'] = 'announcement'
        return super().changelist_view(request, extra_context)


