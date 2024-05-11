# Generated by Django 5.0.1 on 2024-03-13 20:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newapp', '0004_alter_validationtask_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='validationtask',
            name='status',
            field=models.CharField(choices=[('Assigned', 'Assigned'), ('Validated', 'Validated')], default='not-validated', max_length=50),
        ),
    ]