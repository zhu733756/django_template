# Generated by Django 2.1.4 on 2020-03-25 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TaskInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(blank=True, max_length=255, null=True)),
                ('xmlPath', models.CharField(blank=True, max_length=255, null=True)),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
                ('taskId', models.CharField(blank=True, max_length=255, null=True)),
                ('status', models.BooleanField(default=1)),
                ('fetch_datetime', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'task_info',
            },
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255)),
                ('total', models.IntegerField(default=0)),
                ('taskId', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
            ],
            options={
                'db_table': 'user_info',
            },
        ),
        migrations.CreateModel(
            name='VideoInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article_url', models.CharField(blank=True, max_length=255, null=True)),
                ('taskId', models.CharField(blank=True, max_length=255, null=True)),
                ('vid', models.CharField(blank=True, max_length=255, null=True)),
                ('video_file_name', models.CharField(blank=True, max_length=255, null=True)),
                ('src_video_url', models.CharField(blank=True, max_length=255, null=True)),
                ('src_video_image', models.CharField(blank=True, max_length=255, null=True)),
                ('uuid', models.CharField(blank=True, max_length=255, null=True)),
                ('status', models.IntegerField(default=0)),
                ('width', models.IntegerField(default=0)),
                ('height', models.IntegerField(default=0)),
                ('src_width', models.IntegerField(default=0)),
                ('src_height', models.IntegerField(default=0)),
                ('file_length', models.IntegerField(default=0)),
                ('file_size', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'video_info',
            },
        ),
        migrations.CreateModel(
            name='XinhuaWeb',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
                ('publish_date', models.DateTimeField(blank=True, null=True)),
                ('source', models.CharField(blank=True, max_length=255, null=True)),
                ('author', models.CharField(blank=True, max_length=255, null=True)),
                ('xml_file', models.CharField(blank=True, max_length=255, null=True)),
                ('content', models.TextField(blank=True, null=True)),
                ('images', models.TextField(blank=True, null=True)),
                ('video_url', models.TextField(blank=True, null=True)),
                ('video_image_url', models.TextField(blank=True, null=True)),
                ('article_type', models.CharField(blank=True, max_length=255, null=True)),
                ('fetch_date', models.DateTimeField(blank=True, null=True)),
                ('xml_content', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'xinhua_web',
            },
        ),
    ]
