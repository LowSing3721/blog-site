# Generated by Django 3.2.3 on 2021-06-02 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20210531_1638'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='content_html',
            field=models.TextField(blank=True, editable=False, verbose_name='HTML格式正文'),
        ),
    ]
