from datetime import timedelta, date
from django.contrib.admin import SimpleListFilter

class CustomDateFilter(SimpleListFilter):
    """
    Custom filter to filter books by published date.
    """
    title = 'Published Date'
    parameter_name = 'published_date'

    def lookups(self, request, model_admin):
        return [
            ('last_7_days', 'Last 7 Days'),
            ('this_year', 'This Year'),
            ('today', 'Today'),
        ]

    def queryset(self, request, queryset):
        today = date.today()
        if self.value() == 'last_7_days':
            return queryset.filter(published_date__gte=today - timedelta(days=7))
        elif self.value() == 'this_year':
            return queryset.filter(published_date__year=today.year)
        elif self.value() == 'today':
            return queryset.filter(published_date=today)
        return queryset

class PriceRangeFilter(SimpleListFilter):
    title = 'Price Range'
    parameter_name = 'price_range'

    def lookups(self, request, model_admin):
        """
        Return a list of the options shown in the admin filter dropdown.
        """
        return [
            ('cheap', 'Under $20'),
            ('moderate', '$20 - $50'),
            ('expensive', 'Above $50')
        ]

    def queryset(self, request, queryset):
        """
        Modify the queryset based on the selected filter option.
        """
        if self.value() == 'cheap':
            return queryset.filter(price__lt=20)
        elif self.value() == 'moderate':
            return queryset.filter(price__gte=20, price__lte=50)
        elif self.value() == 'expensive':
            return queryset.filter(price__gt=50)
        return queryset