# Generated by Django 4.2.5 on 2023-12-05 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompilerSubmission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.TextField()),
                ('result', models.TextField()),
                ('submission_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
