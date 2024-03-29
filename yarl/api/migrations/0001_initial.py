# Generated by Django 3.1.7 on 2021-03-28 03:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Kanji',
            fields=[
                ('kanji', models.CharField(max_length=1, primary_key=True, serialize=False)),
                ('strokes', models.IntegerField()),
                ('frequency', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Radical',
            fields=[
                ('radical', models.CharField(max_length=1, primary_key=True, serialize=False)),
                ('strokes', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Synset_def',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('synset', models.TextField()),
                ('lang', models.TextField()),
                ('definition', models.TextField()),
                ('sid', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Word',
            fields=[
                ('wordid', models.IntegerField(primary_key=True, serialize=False)),
                ('lang', models.TextField()),
                ('lemma', models.TextField()),
                ('pron', models.TextField(null=True)),
                ('pos', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Krad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kanji', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.kanji')),
                ('radical', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.radical')),
            ],
        ),
        migrations.AddField(
            model_name='kanji',
            name='radicals',
            field=models.ManyToManyField(through='api.Krad', to='api.Radical'),
        ),
    ]
