from django.db import models
from django.urls import reverse

class Project(models.Model):
    PROJECT_TYPES = [
        ('residential', 'Residential'),
        ('commercial', 'Commercial'),
        ('institutional', 'Institutional'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    project_type = models.CharField(max_length=20, choices=PROJECT_TYPES, default='residential')
    location = models.CharField(max_length=100, help_text="e.g. East Legon, Accra", blank=True)
    description = models.TextField()
    
    # Main Image
    image = models.ImageField(upload_to='portfolio/after/', help_text="The final result (After)")
    
    # Optional Before Image for Comparison Slider
    before_image = models.ImageField(upload_to='portfolio/before/', blank=True, null=True, help_text="Optional: The original state (Before)")
    
    completion_date = models.DateField()
    is_featured = models.BooleanField(default=False)
    
    # Linked Materials from Catalogue
    materials_used = models.ManyToManyField('catalogue.Product', blank=True, related_name='used_in_projects')
    
    class Meta:
        ordering = ['-completion_date']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('portfolio:project_detail', kwargs={'slug': self.slug})

class ProjectImage(models.Model):
    """ Secondary gallery images for lightbox """
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='gallery')
    image = models.ImageField(upload_to='portfolio/gallery/')
    caption = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"Gallery for {self.project.title}"
