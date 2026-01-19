from django.contrib import admin

from .models import Training, Set, Meal, Ingredient, Unit

admin.site.register(Training)
admin.site.register(Set)

admin.site.register(Meal)
admin.site.register(Ingredient)

admin.site.register(Unit)
