# Generated by Django 5.0.1 on 2024-03-13 20:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newapp', '0005_alter_validationtask_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='validationtask',
            name='status',
            field=models.CharField(choices=[('Assigned', 'Assigned'), ('Validated', 'Validated')], default='Assigned', max_length=50),
        ),
    ]