from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

from autoslug import AutoSlugField

# Create your models here.
class Course(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(verbose_name='Course Title', max_length=200)
    price = models.FloatField(verbose_name='Course Price', default=1.00)
    duration = models.PositiveIntegerField(verbose_name="Course Duration", default=1)
    currency = models.CharField(verbose_name='Course Currency', default='NGN')
    slug_title = AutoSlugField(populate_from='title', verbose_name='Course Slug', max_length=200, unique=True)
    date_uploaded = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_updated', '-date_uploaded']
        get_latest_by = ['-date_updated', '-date_uploaded']
    
    def __str__(self):
        return f'`{self.title}` by {self.author.username}'
    
    def get_absolute_url(self):
        return reverse('courses:get_course', kwargs={'course_slug': self.slug_title})
    
    def get_display_currency(self):
        return f'{self.currency}{self.price}'
