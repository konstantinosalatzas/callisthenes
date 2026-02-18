from django.utils import timezone
from datetime import timedelta
from collections import defaultdict

from .models import Set

def training_heatmap(user, weeks_range=52):
    """
    Return a list of weeks containing days with training set counts.
    """

    today = timezone.now().date()
    start_date = today - timedelta(days=weeks_range*7)
    
    # Get sets of the user in the date range
    sets = Set.objects.filter(
        training__user=user,
        training__training_date__isnull=False,
        training__training_date__gte=start_date,
        training__training_date__lte=today
    )
    # Count trainings by date
    activity_count = defaultdict(int)
    for set in sets:
        activity_count[set.training.training_date] += 1
    
    # Create heatmap structure
    heatmap = []
    current_date = start_date
    days_of_week = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    
    while current_date <= today:
        week_start = current_date - timedelta(days=current_date.weekday())
        week_data = {
            'start_date': week_start,
            'days': []
        }
        for day_offset in range(7):
            day_date = week_start + timedelta(days=day_offset)
            if day_date > today:
                break
            count = activity_count[day_date]
            week_data['days'].append({
                'date': day_date,
                'count': count,
                'day_name': days_of_week[day_offset],
                'intensity': min(count, 4) # Level 0-4 for CSS classes
            })
        heatmap.append(week_data)
        current_date = week_start + timedelta(days=7)
    
    return heatmap
