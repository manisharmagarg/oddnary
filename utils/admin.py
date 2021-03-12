from django.contrib import admin

class CustomAdminFormMixin(object):
    readonly_fields = (
        'created_by', 'last_modified_by',
        'created_at', 'last_modified_at',
    )

