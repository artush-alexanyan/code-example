from django.contrib import admin, messages
from import_export import resources
from import_export.admin import ExportMixin

from gift.models import Gift, Event


def generate_codes(modeladmin, request, queryset):
    for v in queryset:
        for _ in range(10):
            new_v = Gift.objects.create(toy=v.toy, event=v.event, redeemed=v.redeemed, max_usages=v.max_usages,
                                        allow_ignore_quota=v.allow_ignore_quota
                                        )


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_datetime', 'end_datetime', 'number_of_codes',)
    search_fields = ['name', ]


class GiftResource(resources.ModelResource):
    class Meta:
        model = Gift
        fields = ('code', 'event', 'toy', 'redeemed', 'max_usages',)


class GiftAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = GiftResource
    list_display = (
        'code', 'user', 'event', 'toy', 'redeemed', 'max_usages', 'allow_ignore_quota', 'gifted', 'modified',)
    search_fields = ['code', 'user__email', ]
    list_filter = ['event', 'redeemed', 'allow_ignore_quota', 'gifted', ]
    actions = [generate_codes, ]
    raw_id_fields = (
        'user',
    )


admin.site.register(Gift, GiftAdmin)
