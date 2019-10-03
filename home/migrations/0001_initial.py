# Generated by Django 2.0.7 on 2018-09-12 03:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FAQ',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=200)),
                ('response', models.CharField(max_length=1000)),
            ],
            options={
                'verbose_name_plural': 'FAQs',
            },
        ),
    ]
