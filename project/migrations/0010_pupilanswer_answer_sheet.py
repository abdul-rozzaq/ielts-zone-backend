# Generated by Django 5.0.6 on 2024-07-05 07:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0009_answersheet_pupilanswer'),
    ]

    operations = [
        migrations.AddField(
            model_name='pupilanswer',
            name='answer_sheet',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='project.answersheet'),
            preserve_default=False,
        ),
    ]
