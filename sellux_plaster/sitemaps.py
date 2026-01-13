from django.contrib import sitemaps
from django.urls import reverse

class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        # Add the names of the URLs you want indexed
        return ['home', 'team_list', 'contact_us', 'catalogue'] 

    def location(self, item):
        return reverse(item)