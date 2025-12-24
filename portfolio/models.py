from django.db import models

class Project(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    image = models.ImageField(upload_to='portfolio/')
    completion_date = models.DateField()
    is_featured = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-completion_date']

    def __str__(self):
        return self.title

class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='gallery')
    image = models.ImageField(upload_to='portfolio/gallery/')
    caption = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"Gallery image for {self.project.title}"
