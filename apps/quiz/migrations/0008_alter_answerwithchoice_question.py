# Generated by Django 3.2.8 on 2021-10-21 20:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0007_useranswerswithchoices_answer_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answerwithchoice',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ansver_in_question', to='quiz.question'),
        ),
    ]