from django.shortcuts import render, redirect

from django.apps import apps

model = apps.get_model('courses', 'Course')

def register_course(request, slug):
    this_course = model.objects.get(slug=slug)
    this_course.add_user_to_list_of_students(user=request.user)
    return redirect('home')
