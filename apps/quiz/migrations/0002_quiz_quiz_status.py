# Generated by Django 3.2.8 on 2021-10-21 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='quiz_status',
            field=models.CharField(choices=[('activ', 'activ'), ('not_activ', 'not_activ')], default='not_activ', max_length=255),
        ),
    ]