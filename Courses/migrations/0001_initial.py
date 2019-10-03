# Generated by Django 2.0.7 on 2018-09-13 05:40

import Courses.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_title', models.CharField(max_length=200)),
                ('lab_submission_type', models.IntegerField(choices=[(1, 'submit by uploading document'), (2, 'submit by machine ID'), (3, 'submit from repo')], default=1)),
            ],
            options={
                'verbose_name_plural': 'Courses',
            },
        ),
        migrations.CreateModel(
            name='CourseTopic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic_number', models.IntegerField(default=0)),
                ('topic', models.CharField(max_length=200)),
                ('lab_name', models.CharField(max_length=50)),
                ('video', models.TextField()),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='topics', related_query_name='topic', to='Courses.Course')),
            ],
            options={
                'verbose_name_plural': 'Course Topics',
            },
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document', models.FileField(upload_to=Courses.models.content_file_name)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('course_topic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Courses.CourseTopic')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='GradesReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('task_no', models.IntegerField()),
                ('score', models.IntegerField()),
                ('grade', models.CharField(default='not graded', max_length=20)),
                ('course_topic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='grades', related_query_name='grade', to='Courses.CourseTopic')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Grades Reports',
            },
        ),
        migrations.CreateModel(
            name='LabTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_number', models.IntegerField()),
                ('comment', models.TextField()),
                ('note', models.TextField(blank=True, null=True)),
                ('task', models.TextField()),
                ('xpected', models.TextField(default='Not Needed')),
                ('hint', models.TextField(blank=True, null=True)),
                ('instruction', models.TextField()),
                ('lab', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', related_query_name='task', to='Courses.CourseTopic')),
            ],
            options={
                'verbose_name_plural': 'Lab Tasks',
                'ordering': ('lab_id', 'task_number'),
            },
        ),
        migrations.CreateModel(
            name='MainModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=42)),
                ('document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Courses.Document')),
            ],
        ),
    ]