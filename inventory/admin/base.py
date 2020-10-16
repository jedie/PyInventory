from reversion_compare.admin import CompareVersionAdmin


class BaseUserAdmin(CompareVersionAdmin):
    def save_model(self, request, obj, form, change):
        if obj.user_id is None:
            obj.user = request.user

        super().save_model(request, obj, form, change)
