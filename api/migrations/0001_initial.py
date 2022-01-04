# Generated by Django 3.2.11 on 2022-01-04 21:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('bingeauth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TvShow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('show_title', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='UserTvShow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_watched', models.DateTimeField()),
                ('times_watched', models.IntegerField(default=0)),
                ('show', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='show_users', to='api.tvshow')),
                ('user_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_shows', to='bingeauth.userprofile')),
            ],
        ),
    ]
