# Generated by Django 5.0.4 on 2024-05-27 14:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0004_remove_tags_choice_vote'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tags',
            old_name='tags',
            new_name='tag',
        ),
    ]