# Generated by Django 3.0.1 on 2019-12-29 00:11

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('sig_health', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('member_slack_id', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_regular', models.BooleanField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Workout',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('thread_ts', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='workout_set', to='sig_health.Member')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='WorkoutAdmit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('thread_ts', models.CharField(max_length=100)),
                ('admitted_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='admit_set', to='sig_health.Member')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='admitted_set', to='sig_health.Member')),
            ],
            options={
                'unique_together': {('thread_ts', 'admitted_by')},
            },
        ),
    ]