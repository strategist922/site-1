# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-01-31 22:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


def move_submission_source(apps, schema_editor):
    Submission = apps.get_model('judge', 'Submission')
    SubmissionSource = apps.get_model('judge', 'SubmissionSource')
    SubmissionSource.objects.bulk_create(SubmissionSource(source=sub.source, submission=sub) for sub in Submission.objects.using(schema_editor.connection.alias))


def restore_submission_source(apps, schema_editor):
    Submission = apps.get_model('judge', 'Submission')
    for sub in Submission.objects.using(schema_editor.connection.alias):
        sub.source = sub.link.source


class Migration(migrations.Migration):

    dependencies = [
        ('judge', '0080_contest_banned_users'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubmissionSource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source', models.TextField(max_length=65536, verbose_name='source code')),
                ('submission', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='link', to='judge.Submission', verbose_name='associated submission')),
            ],
        ),
        migrations.RunPython(move_submission_source, restore_submission_source),
        migrations.RemoveField(
            model_name='submission',
            name='source',
        ),
        migrations.AlterField(
            model_name='submissionsource',
            name='submission',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='source', to='judge.Submission', verbose_name='associated submission')
        ),
    ]
