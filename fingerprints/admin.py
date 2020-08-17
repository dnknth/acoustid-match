from .models import *
from .forms import *
from django.contrib import admin, messages


def lookup(modeladmin, request, queryset):
    n = 0
    for fp in queryset.iterator():
        fp.lookup()
        if fp.acoustid: n += 1
    if n == 0: messages.warning(request, 'Identified no fingerprints')
    elif n == 1: messages.info(request, 'Identified 1 fingerprint')
    else: messages.info(request, 'Identified %d fingerprints' % n)
lookup.short_description = 'Identify with MusicBrainz'


@admin.register(Fingerprint)
class FingerprintAdmin(admin.ModelAdmin):
    "Custom admin settings for audio fingerprints"
            
    def unique(self, obj):
        "Is this track unique (i.e. no duplicates)?"
        return not bool(obj.cluster)
    unique.boolean = True
    
    def identified(self, obj):
        "Does this track have an AcoustID record?"
        return bool(obj.acoustid)
    identified.boolean = True
    
    class AcoustidFilter(admin.SimpleListFilter):
        "Filter for identified tracks"

        title = 'identified'
        parameter_name = 'identified'

        def lookups(self, request, model_admin):
            return (('1', 'Yes'),
                    ('0', 'No'))

        def queryset(self, request, queryset):
            if self.value() == '0':
                return queryset.filter(acoustid__isnull=True)
            if self.value() == '1':
                return queryset.filter(acoustid__isnull=False)
            return queryset

    class UniqueFilter(admin.SimpleListFilter):
        "Filter unique vs. duplicate tracks"

        title = 'unique'
        parameter_name = 'unique'

        def lookups(self, request, model_admin):
            return (('1', 'Yes'),
                    ('0', 'No'))

        def queryset(self, request, queryset):
            if self.value() == '0':
                return queryset.filter(cluster__isnull=False)
            elif self.value() == '1':
                return queryset.filter(cluster__isnull=True)
            return queryset
            
    def has_add_permission(self, request):
        "No point in manually adding tracks, use ./manage scan instead"
        return False

    def has_change_permission(self, request, obj=None):
        "No point in manually changing tracks"
        return False

    list_display = ('__str__', 'identified', 'unique' )
    list_filter = (AcoustidFilter, UniqueFilter )
    change_form_template = 'fingerprint-admin/change_form.html'
    search_fields = ('path', 'cluster' )
    form = FingerprintForm
    actions = (lookup, )
