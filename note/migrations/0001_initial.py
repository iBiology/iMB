# Generated by Django 3.2.4 on 2021-06-10 02:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Word',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('words', models.TextField(help_text='Query word.')),
                ('audio', models.TextField(help_text='Audio file.')),
                ('label', models.TextField(help_text='Functional label.')),
                ('sense', models.TextField(help_text='Senses of the query word.')),
                ('ymd', models.DateTimeField(auto_now_add=True, help_text='Entry creating date and time.')),
                ('favorite', models.BooleanField(default=False, help_text='Add to favorite.')),
            ],
        ),
    ]
