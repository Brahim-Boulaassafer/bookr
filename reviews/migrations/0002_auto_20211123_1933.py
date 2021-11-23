# Generated by Django 3.2.8 on 2021-11-23 19:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='cover',
            field=models.ImageField(blank=True, null=True, upload_to='book_covers/'),
        ),
        migrations.AddField(
            model_name='book',
            name='sample',
            field=models.FileField(blank=True, null=True, upload_to='book_samples/'),
        ),
        migrations.AlterField(
            model_name='review',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, help_text='The date and time the review was created.'),
        ),
        migrations.AlterField(
            model_name='review',
            name='date_edited',
            field=models.DateTimeField(help_text='The date and time the review was last edited.', null=True),
        ),
    ]