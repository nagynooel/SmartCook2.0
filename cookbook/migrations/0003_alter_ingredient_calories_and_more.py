# Generated by Django 4.2 on 2023-05-30 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cookbook', '0002_rename_name_recipe_title_recipe_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='calories',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='carbohydrates',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='cholesterol',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='fat',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='fiber',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='protein',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='saturated_fat',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='sodium',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='sugar',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='trans_fat',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='servings',
            field=models.FloatField(),
        ),
    ]
