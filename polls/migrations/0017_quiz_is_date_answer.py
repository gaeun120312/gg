# Generated by Django 4.2.6 on 2023-11-17 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0016_alter_useranswer_quiz'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='is_date_answer',
            field=models.BooleanField(default=False),
        ),
    ]
