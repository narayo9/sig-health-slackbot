# Generated by Django 3.0.1 on 2019-12-29 06:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('slack_outbound', '0002_auto_20191229_1000'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emojitask',
            name='execute_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='실행 일시'),
        ),
        migrations.AlterField(
            model_name='messagetask',
            name='execute_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='실행 일시'),
        ),
        migrations.AlterField(
            model_name='replytask',
            name='execute_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='실행 일시'),
        ),
    ]
