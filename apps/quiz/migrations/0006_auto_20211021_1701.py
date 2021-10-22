# Generated by Django 3.2.8 on 2021-10-21 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0005_alter_useranswerswithtext_answer_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='useranswerswithchoices',
            name='answer',
        ),
        migrations.AddField(
            model_name='useranswerswithchoices',
            name='answer',
            field=models.ManyToManyField(related_name='answer_choice', to='quiz.AnswerWithChoice'),
        ),
    ]
