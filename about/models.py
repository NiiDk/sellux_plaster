from django.db import models

class AboutPage(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200)
    image = models.ImageField(upload_to='about/')
    main_content = models.TextField()
    vision = models.TextField()
    mission = models.TextField()
    professional_pedigree = models.TextField()

    def __str__(self):
        return self.title

class CoreValue(models.Model):
    about_page = models.ForeignKey(AboutPage, related_name='core_values', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=100, help_text="e.g., 'bi-gem' for a diamond icon. Use Bootstrap Icons.")

    def __str__(self):
        return self.title
