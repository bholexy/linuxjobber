# Generated by Django 2.0.1 on 2018-09-11 15:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('staticscrumy', '0003_scrumygoals_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='scrumygoals',
            old_name='task_id',
            new_name='goal_id',
        ),
        migrations.RenameField(
            model_name='scrumygoals',
            old_name='task_name',
            new_name='goal_name',
        ),
        migrations.RenameField(
            model_name='scrumyhistory',
            old_name='task',
            new_name='goal',
        ),
    ]
