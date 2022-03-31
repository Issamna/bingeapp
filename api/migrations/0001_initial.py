# Generated by Django 3.2.11 on 2022-02-20 16:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("bingeauth", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Genre",
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
                ("api_id", models.CharField(max_length=255)),
                ("name", models.CharField(max_length=255)),
            ],
            options={
                "unique_together": {("api_id", "name")},
            },
        ),
        migrations.CreateModel(
            name="TvShow",
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
                ("show_title", models.CharField(max_length=255)),
                ("api_id", models.CharField(default=None, max_length=255)),
                ("is_detailed", models.BooleanField(default=False)),
                ("first_air_date", models.DateField(blank=True, null=True)),
                (
                    "vote_average",
                    models.DecimalField(decimal_places=2, max_digits=5, null=True),
                ),
                ("vote_count", models.IntegerField(null=True)),
                ("overview", models.TextField(null=True)),
                ("poster_path", models.CharField(max_length=255, null=True)),
                ("in_production", models.BooleanField(null=True)),
                ("number_of_episodes", models.IntegerField(null=True)),
                ("number_of_seasons", models.IntegerField(null=True)),
                ("genres", models.ManyToManyField(to="api.Genre")),
            ],
        ),
        migrations.CreateModel(
            name="UserTvShow",
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
                ("rating", models.IntegerField(null=True)),
                (
                    "show",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="show_users",
                        to="api.tvshow",
                    ),
                ),
                (
                    "userprofile",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="user_shows",
                        to="bingeauth.userprofile",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ViewHistory",
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
                ("start_date", models.DateField()),
                ("end_date", models.DateField(blank=True, null=True)),
                (
                    "user_tvshow",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="view_histories",
                        to="api.usertvshow",
                    ),
                ),
            ],
            options={
                "ordering": ["start_date"],
            },
        ),
        migrations.AddConstraint(
            model_name="usertvshow",
            constraint=models.CheckConstraint(
                check=models.Q(("rating__range", (0, 5))),
                name="api_usertvshow_rating_range",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="usertvshow",
            unique_together={("userprofile", "show")},
        ),
    ]