# Generated by Django 4.2.17 on 2024-12-27 09:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
        ('hunts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='playerprogress',
            name='player',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='progress', to='users.player'),
        ),
        migrations.AddField(
            model_name='playerprogress',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hunts.question'),
        ),
        migrations.AlterUniqueTogether(
            name='question',
            unique_together={('game', 'order')},
        ),
    ]
