# Generated by Django 4.1.5 on 2025-05-09 17:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0009_rename_timestamp_teachermessage_sent_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='LearningLevel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField()),
            ],
        ),
        migrations.RenameField(
            model_name='teachermessage',
            old_name='message',
            new_name='content',
        ),
        migrations.RenameField(
            model_name='teachermessage',
            old_name='sent_at',
            new_name='timestamp',
        ),
        migrations.AlterField(
            model_name='teachermessage',
            name='recipient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teacher_received_messages', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='teachermessage',
            name='sender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teacher_sent_messages', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_received_messages', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_sent_messages', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='student',
            name='learning_level',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.learninglevel'),
        ),
    ]
