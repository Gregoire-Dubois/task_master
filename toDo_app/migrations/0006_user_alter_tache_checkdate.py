# Generated by Django 4.0.4 on 2022-05-05 18:21

import datetime
from django.db import migrations, models
import toDo_app.models


class Migration(migrations.Migration):

    dependencies = [
        ('toDo_app', '0005_alter_tache_checkdate'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstName', models.CharField(max_length=35)),
                ('lastName', models.CharField(max_length=35)),
                ('compagny', models.CharField(max_length=35)),
            ],
            options={
                'ordering': ['firstName'],
            },
        ),
        migrations.AlterField(
            model_name='tache',
            name='checkDate',
            field=models.DateField(default=datetime.date(2022, 5, 5), validators=[toDo_app.models.validate_checkDate]),
        ),
    ]
