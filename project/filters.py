from django.contrib import admin

class HighPercentageFilter(admin.SimpleListFilter):
    title = 'High Percentage'
    parameter_name = 'high_percentage'

    def lookups(self, request, model_admin):
        return (
            ('90+', '90% and above'),
            ('75+', '75% and above'),
        )

    def queryset(self, request, queryset):
        if self.value() == '90+':
            return queryset.filter(computed_percentage__gte=90)
        elif self.value() == '75+':
            return queryset.filter(computed_percentage__gte=75)
        
        