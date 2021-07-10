from django.http import Http404
from django.shortcuts import get_object_or_404, render,redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import ListView, CreateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from .models import *
from .forms import CourseForm, LessonForm, CommentForm

from django.forms import inlineformset_factory

class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses/courses.html'
    context_object_name = 'course'

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        slug = self.kwargs.get(self.slug_url_kwarg)
        slug_field = self.get_slug_field()
        queryset = queryset.filter(**{slug_field: slug})
        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404("No %(verbose_name)s found matching the query" %
                          {'verbose_name': self.model._meta.verbose_name})
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = Course.objects.get(slug=self.kwargs['slug'])
        if self.request.user.is_authenticated:
            if CourseRegistration.objects.filter(course=course, user_id=self.request.user.id).exists():
                context['is_enrolled'] = True
                context['lessons'] = course.lessons.all()
            else:
                context['is_enrolled'] = False
                context['lessons'] = course.lessons.all()
        return context
    
    

class CoursesByCategoryListView(ListView):
    template_name = 'courses/courses_by_category.html'
    model = Course
    context_object_name = 'courses'

    def get_queryset(self):
        category = Category.objects.get(slug=self.kwargs['slug'])
        return self.model.objects.filter(category_id=category.id)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = Category.objects.get(slug=self.kwargs['slug'])
        context['category'] = category
        context['categories'] = Category.objects.all()
        return context

    
class CreateCourseView(LoginRequiredMixin, CreateView):
    template_name = 'courses/upload_course.html'
    form_class = CourseForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.instructor = self.request.user
        self.object.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('courses:create-lessons', kwargs={'slug': self.object.slug})

def createLesson(request, slug):
    LessonFormSet = inlineformset_factory(Course, Lesson, fields=('title', 'video'), extra=5)
    course = Course.objects.get(slug=slug)
    formset = LessonFormSet(queryset=Lesson.objects.none(), instance=course)

    if request.method == 'POST':
        form = LessonForm(request.POST, request.FILES)
        formset = LessonFormSet(request.POST, request.FILES, instance=course)
        if formset.is_valid():
            formset.save()
            return redirect('home')

    context = {'form':formset}
    return render(request, 'courses/upload_lessons.html', context)


def learn_lesson(request, lesson_id):
    try:
        lesson_obj = Lesson.objects.get(id=lesson_id)
        comments = LessonComment.objects.filter(lesson = lesson_obj)
    except ObjectDoesNotExist:
        return render(request, '404.html')
    
    if request.method == 'POST':
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.lesson = lesson_obj
                comment.user = request.user
                comment.save()
                messages.success(request, "Your comment has been posted successfully")
                return redirect(request.path)
    else:
        form = CommentForm()
    
    context = {
                'lesson':lesson_obj,
                'form':form,
                'comments':comments,
            }
    return render(request, 'courses/lessons.html', context)


def comment_remove(request, comment_id):
    comment = get_object_or_404(LessonComment, id=comment_id)
    lesson_id = comment.lesson.id
    comment.delete()
    return redirect('courses:lesson-page', lesson_id)


def search(request):
    query = request.GET.get('query')
    allCoursesTitle = Course.objects.filter(title__icontains=query)
    allCoursesInstructor = Course.objects.filter(instructor__username__icontains=query)
    allCourses = allCoursesTitle.union(allCoursesInstructor)
    if allCourses.count()==0:
        messages.warning(request,  "No search results found. Please refine your query.")
    context = {'allCourses': allCourses, 'query':query}
    return render(request, 'courses/search.html', context)

