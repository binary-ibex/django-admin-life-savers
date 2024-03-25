from django import forms

class AnnouncementForm(forms.Form):

    title = forms.CharField(
        max_length=100,
        required=True
    )

    body = forms.CharField(
        max_length=300,
        required=True
    )


