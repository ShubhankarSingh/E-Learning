# Generated by Django 3.0 on 2021-06-01 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0006_course_thumbnail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='short_description',
            field=models.CharField(default='', max_length=60),
        ),
    ]