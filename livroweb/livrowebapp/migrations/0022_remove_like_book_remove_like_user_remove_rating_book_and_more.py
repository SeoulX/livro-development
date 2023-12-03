# Generated by Django 4.2.5 on 2023-12-03 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('livrowebapp', '0021_like'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='like',
            name='book',
        ),
        migrations.RemoveField(
            model_name='like',
            name='user',
        ),
        migrations.RemoveField(
            model_name='rating',
            name='book',
        ),
        migrations.RemoveField(
            model_name='rating',
            name='user',
        ),
        migrations.AddField(
            model_name='book',
            name='like',
            field=models.ManyToManyField(related_name='likes', to='livrowebapp.member'),
        ),
        migrations.AlterField(
            model_name='book',
            name='feedbacks',
            field=models.ManyToManyField(related_name='books', to='livrowebapp.comment'),
        ),
        migrations.DeleteModel(
            name='Feedback',
        ),
        migrations.DeleteModel(
            name='Like',
        ),
        migrations.DeleteModel(
            name='Rating',
        ),
    ]