# Generated by Django 2.2.9 on 2020-01-07 04:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0003_auto_20200107_1240'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wechatstudent',
            name='student',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='student.Student'),
        ),
    ]