from django.urls import path

from api import views

app_name = 'api'
urlpatterns = [
    path('courses/', views.all_courses, name='all-courses'),
    path('courses/new/', views.new_course, name='new-course'),
    path('courses/<slug:course_slug>/', views.single_course, name='single-course'),
]