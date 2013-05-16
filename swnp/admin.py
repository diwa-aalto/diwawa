from django.contrib import admin
from django.contrib.flatpages.admin import FlatpageForm, FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from models import *


class CompanyInline(admin.StackedInline):
    model = Company

    
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name','company','dir',)
    list_display_links = ('name',)
    list_editable = ('dir',)
    def get_readonly_fields(self, request, obj=None):
        if obj: # editing an existing object
            return self.readonly_fields + ('company',)
        return self.readonly_fields
 
 
class ExtendedFlatPageForm(FlatpageForm):
    class Meta:
        model = ExtendedFlatPage


class ExtendedFlatPageAdmin(FlatPageAdmin):
    form = ExtendedFlatPageForm
    fieldsets = (
        (None, {'fields': ('url', 'title', 'content', 'sites', 'show_after', 'alt_text')}),
    )     


admin.site.register(Project, ProjectAdmin)
admin.site.register(Session)
admin.site.register(Event)
admin.site.register(Action)
admin.site.register(User)
admin.site.register(File)
admin.site.register(Activity)
admin.site.register(Fileaction)
admin.site.register(Computer)
admin.site.register(Company)
admin.site.unregister(FlatPage)
admin.site.register(ExtendedFlatPage, ExtendedFlatPageAdmin)

