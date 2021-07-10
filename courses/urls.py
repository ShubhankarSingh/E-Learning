from django.urls import path
from .views import *

app_name = 'courses'

urlpatterns = [
    
    path('courses/<slug:slug>', CourseDetailView.as_view(), name='course-details'),
    path('courses/<slug:slug>/category', CoursesByCategoryListView.as_view(), name='course-by-category'),
    path('upload/', CreateCourseView.as_view(), name='create-course'),
    path('upload/<slug:slug>/lessons/', createLesson , name='create-lessons'),
    path('learn/lesson/<int:lesson_id>/', learn_lesson , name='lesson-page'),
    path('remove/<int:comment_id>/', comment_remove, name='comment_remove'),
    path('search', search, name="search"),
]

