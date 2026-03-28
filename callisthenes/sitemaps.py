from django.contrib import sitemaps
from django.urls import reverse

class StaticViewSitemap(sitemaps.Sitemap):
    def items(self):
        return ["index", "signup", "login", "logout", "password_change", "training_list", "training_new", "meal_list", "meal_new", "unit_list", "unit_new"]

    def location(self, item):
        return reverse(item)
