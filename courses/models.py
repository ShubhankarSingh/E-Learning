from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
from django.utils.timezone import now
from django.utils.text import slugify
from django.contrib.auth import get_user_model
User = get_user_model()

class Category(models.Model):
    title = models.CharField(max_length=50, default='')
    slug = models.SlugField(max_length=200, unique=True, default='', blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Categories'


class Course(models.Model):
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, default='')
    title = models.CharField(max_length=100, default='')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, default='')
    slug = models.SlugField(max_length=200, unique=True, blank=True, primary_key=True, auto_created=False, default='')
    short_description = models.CharField(blank=False, max_length=150, default='')
    description = models.TextField(blank=False, default='')
    language = models.CharField(max_length=200, default='English')
    thumbnail = models.ImageField(upload_to='thumbnails/', default='')
    

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Course, self).save(*args, **kwargs)

    def add_user_to_list_of_students(self, user):
        registration = CourseRegistration.objects.create(user = user,
                                                    course = self)


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons', default='')
    title = models.CharField(max_length=100, default=None)
    video = models.FileField(upload_to='courses/')

    def __str__(self):
        return self.course.title
    

class LessonComment(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(max_length=200, default=None)
    reply = models.ForeignKey('self',on_delete=models.CASCADE, null=True, blank=True)
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.user.username, self.lesson)



class CourseRegistration(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'Students'
        unique_together = ('course','user')

# @receiver(pre_delete, sender=Course)
# def mymodel_delete(sender, instance, **kwrags):
#     instance.video.delete(False)







