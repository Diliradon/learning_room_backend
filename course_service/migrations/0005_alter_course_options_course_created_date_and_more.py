# Generated by Django 5.0.6 on 2024-07-09 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("course_service", "0004_alter_course_teachers_alter_course_unique_key"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="course",
            options={"ordering": ["name", "-created_date"]},
        ),
        migrations.AddField(
            model_name="course",
            name="created_date",
            field=models.DateField(auto_now=True),
        ),
        migrations.AddField(
            model_name="course",
            name="number_of_classroom",
            field=models.CharField(default="Online only!"),
        ),
    ]
