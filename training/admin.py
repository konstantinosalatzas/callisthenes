from django.contrib import admin

from .models import Training, Performance

class PerformanceInline(admin.TabularInline):
    model = Performance
    extra = 3

class TrainingAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["training_title"]}),
        ("Date information", {"fields": ["training_date"], "classes": ["collapse"]}),
    ]
    inlines = [PerformanceInline]
    list_display = ["training_title", "training_date", "was_posted_recently"]
    list_filter = ["training_date"]
    search_fields = ["training_title"]

admin.site.register(Training, TrainingAdmin)
