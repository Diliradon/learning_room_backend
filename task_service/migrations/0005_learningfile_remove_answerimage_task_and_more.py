# Generated by Django 5.0.6 on 2024-07-23 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("task_service", "0004_alter_answerfile_file_alter_answerimage_image_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="LearningFile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("model", models.CharField(max_length=30)),
                ("type", models.CharField(max_length=30)),
                ("instance_id", models.IntegerField()),
                ("file", models.FileField(upload_to="")),
            ],
        ),
        migrations.RemoveField(
            model_name="answerimage",
            name="task",
        ),
        migrations.RemoveField(
            model_name="taskfile",
            name="task",
        ),
        migrations.RemoveField(
            model_name="taskimage",
            name="task",
        ),
        migrations.RemoveField(
            model_name="review",
            name="task",
        ),
        migrations.DeleteModel(
            name="AnswerFile",
        ),
        migrations.DeleteModel(
            name="AnswerImage",
        ),
        migrations.DeleteModel(
            name="TaskFile",
        ),
        migrations.DeleteModel(
            name="TaskImage",
        ),
    ]
