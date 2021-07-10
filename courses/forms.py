from django import forms
from django.db.models import fields
from .models import Course, Lesson, LessonComment


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'thumbnail', 'category', 'short_description', 'description', 'language']


class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['title','video']

class CommentForm(forms.ModelForm):
    class Meta:
        model = LessonComment
        fields = ['comment']

        widgets = {
            'comment': forms.Textarea(attrs={
                'class': 'editable medium-editor-textarea',
                'rows':1, 
                'cols':100
            })
        }