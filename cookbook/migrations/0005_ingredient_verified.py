# Generated by Django 4.2 on 2023-06-07 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cookbook', '0004_recipeinstruction'),
    ]

    operations = [
        migrations.AddField(
            model_name='ingredient',
            name='verified',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]
