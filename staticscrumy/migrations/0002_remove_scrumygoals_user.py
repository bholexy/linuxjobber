# Generated by Django 2.0.1 on 2018-09-05 16:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('staticscrumy', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='scrumygoals',
            name='user',
        ),
    ]
