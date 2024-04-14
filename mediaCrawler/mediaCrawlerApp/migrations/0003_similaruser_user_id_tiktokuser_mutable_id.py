# Generated by Django 5.0.4 on 2024-04-14 02:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mediaCrawlerApp', '0002_remove_similaruser_jj'),
    ]

    operations = [
        migrations.AddField(
            model_name='similaruser',
            name='user_id',
            field=models.CharField(blank=True, max_length=50, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='tiktokuser',
            name='mutable_id',
            field=models.CharField(blank=True, max_length=50, null=True, unique=True),
        ),
    ]
