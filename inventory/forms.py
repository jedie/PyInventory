from django import forms
from django.core.exceptions import FieldDoesNotExist

from inventory.request_dict import get_request_dict


class OnlyUserRelationsModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Filter all related fields that has a "user" attribute for the current user
        # e.g.:
        #   The user should only select his own "location" and "items"

        user = get_request_dict()['user']  # get current user via threading.local()
        for formfield in self.fields.values():
            if not hasattr(formfield, 'queryset'):
                continue

            queryset = formfield.queryset
            opts = queryset.model._meta
            try:
                opts.get_field('user')
            except FieldDoesNotExist:
                continue

            formfield.queryset = queryset.filter(user=user)

    def save(self, commit=True):
        instance = super().save(commit=False)
        if instance.user_id is None:
            user = get_request_dict()['user']  # get current user via threading.local()
            instance.user_id = user.pk

        instance.save()
        return instance
