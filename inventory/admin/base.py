from reversion_compare.admin import CompareVersionAdmin


class BaseUserAdmin(CompareVersionAdmin):
    def get_changelist(self, request, **kwargs):
        self.user = request.user
        return super().get_changelist(request, **kwargs)

    def save_model(self, request, obj, form, change):
        if obj.user_id is None:
            obj.user = request.user

        super().save_model(request, obj, form, change)
