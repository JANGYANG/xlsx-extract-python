# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-04-03 15:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AuthGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80, unique=True)),
            ],
            options={
                'db_table': 'auth_group',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthGroupPermissions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'auth_group_permissions',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthPermission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('codename', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'auth_permission',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128)),
                ('last_login', models.DateTimeField(blank=True, null=True)),
                ('is_superuser', models.IntegerField()),
                ('username', models.CharField(max_length=150, unique=True)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('email', models.CharField(max_length=254)),
                ('is_staff', models.IntegerField()),
                ('is_active', models.IntegerField()),
                ('date_joined', models.DateTimeField()),
            ],
            options={
                'db_table': 'auth_user',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUserGroups',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'auth_user_groups',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUserUserPermissions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'auth_user_user_permissions',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoAdminLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action_time', models.DateTimeField()),
                ('object_id', models.TextField(blank=True, null=True)),
                ('object_repr', models.CharField(max_length=200)),
                ('action_flag', models.SmallIntegerField()),
                ('change_message', models.TextField()),
            ],
            options={
                'db_table': 'django_admin_log',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoContentType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app_label', models.CharField(max_length=100)),
                ('model', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'django_content_type',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoMigrations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('applied', models.DateTimeField()),
            ],
            options={
                'db_table': 'django_migrations',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoSession',
            fields=[
                ('session_key', models.CharField(max_length=40, primary_key=True, serialize=False)),
                ('session_data', models.TextField()),
                ('expire_date', models.DateTimeField()),
            ],
            options={
                'db_table': 'django_session',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Matchassister',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('matchuid', models.CharField(db_column='matchUID', max_length=36)),
                ('scoretime', models.IntegerField(db_column='scoreTime')),
                ('useruid', models.CharField(db_column='userUID', max_length=36)),
            ],
            options={
                'db_table': 'matchAssister',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Matchcomment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('matchcommentuid', models.CharField(db_column='matchCommentUID', max_length=36)),
                ('content', models.TextField()),
                ('commentdate', models.DateTimeField(db_column='commentDate')),
                ('matchuid', models.CharField(db_column='matchUID', max_length=36)),
                ('useruid', models.CharField(db_column='userUID', max_length=36)),
            ],
            options={
                'db_table': 'matchComment',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Matchscorer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('matchuid', models.CharField(db_column='matchUID', max_length=36)),
                ('scoretime', models.IntegerField(db_column='scoreTime')),
                ('useruid', models.CharField(db_column='userUID', max_length=36)),
            ],
            options={
                'db_table': 'matchScorer',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Matchuser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('matchuid', models.CharField(db_column='matchUID', max_length=36)),
                ('useruid', models.CharField(db_column='userUID', max_length=36)),
                ('teamuid', models.CharField(db_column='teamUID', max_length=36)),
            ],
            options={
                'db_table': 'matchUser',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Reqmatch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reqteamuid', models.CharField(db_column='reqTeamUID', max_length=36)),
                ('resteamuid', models.CharField(db_column='resTeamUID', max_length=36)),
                ('matchdate', models.DateTimeField(db_column='matchDate')),
                ('subregion', models.CharField(db_column='subRegion', max_length=36)),
                ('mainregion', models.CharField(db_column='mainRegion', max_length=36)),
                ('requestdate', models.DateTimeField(db_column='requestDate')),
                ('confirm', models.IntegerField()),
            ],
            options={
                'db_table': 'reqMatch',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Reqteamjoin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('teamuid', models.CharField(db_column='teamUID', max_length=36)),
                ('useruid', models.CharField(db_column='userUID', max_length=36)),
                ('confirm', models.IntegerField(blank=True, null=True)),
                ('requestdate', models.DateTimeField(db_column='requestDate')),
            ],
            options={
                'db_table': 'reqTeamJoin',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Smatch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('matchuid', models.CharField(db_column='matchUID', max_length=36)),
                ('homescore', models.IntegerField(db_column='homeScore')),
                ('awayscore', models.IntegerField(db_column='awayScore')),
                ('stadium', models.CharField(blank=True, max_length=50, null=True)),
                ('playingtime', models.IntegerField(blank=True, db_column='playingTime', null=True)),
                ('matchdate', models.DateTimeField(db_column='matchDate')),
                ('hometeamuid', models.CharField(db_column='homeTeamUID', max_length=36)),
                ('awayteamuid', models.CharField(db_column='awayTeamUID', max_length=36)),
                ('matchtype', models.CharField(blank=True, db_column='matchType', max_length=30, null=True)),
            ],
            options={
                'db_table': 'sMatch',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('teamuid', models.CharField(db_column='teamUID', max_length=50)),
                ('teamemblem', models.CharField(blank=True, db_column='teamEmblem', max_length=100, null=True)),
                ('teambirth', models.IntegerField(blank=True, db_column='teamBirth', null=True)),
                ('teamcolor', models.IntegerField(blank=True, db_column='teamColor', null=True)),
                ('captainuid', models.CharField(db_column='captainUID', max_length=36)),
                ('teamname', models.CharField(blank=True, db_column='teamName', max_length=50, null=True)),
            ],
            options={
                'db_table': 'team',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Teamformation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('teamuid', models.CharField(db_column='teamUID', max_length=36)),
                ('formation', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'teamFormation',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Teammanager',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('teamuid', models.CharField(db_column='teamUID', max_length=36)),
                ('playeruid', models.CharField(db_column='playerUID', max_length=36)),
            ],
            options={
                'db_table': 'teamManager',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Teamregion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('teamuid', models.CharField(db_column='teamUID', max_length=36)),
                ('mainregion', models.CharField(db_column='mainRegion', max_length=30)),
                ('subregion', models.CharField(db_column='subRegion', max_length=30)),
            ],
            options={
                'db_table': 'teamRegion',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=36, null=True)),
                ('date', models.DateField(blank=True, null=True)),
                ('startday', models.TimeField(blank=True, db_column='startDay', null=True)),
                ('endday', models.TimeField(blank=True, db_column='endDay', null=True)),
                ('startlunch', models.TimeField(blank=True, db_column='startLunch', null=True)),
                ('endlunch', models.TimeField(blank=True, db_column='endLunch', null=True)),
            ],
            options={
                'db_table': 'test',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('useruid', models.CharField(db_column='userUID', max_length=36)),
                ('username', models.CharField(db_column='userName', max_length=50)),
                ('encryptedpw', models.CharField(db_column='encryptedPW', max_length=80)),
                ('email', models.CharField(max_length=80)),
                ('height', models.IntegerField(blank=True, null=True)),
                ('weight', models.IntegerField(blank=True, null=True)),
                ('teamuid', models.CharField(blank=True, db_column='teamUID', max_length=36, null=True)),
                ('salt', models.CharField(blank=True, max_length=36, null=True)),
                ('userbirth', models.DateField(blank=True, db_column='userBirth', null=True)),
                ('job', models.CharField(blank=True, max_length=50, null=True)),
                ('created_at', models.DateTimeField()),
                ('phonenum', models.CharField(db_column='phoneNum', max_length=36)),
            ],
            options={
                'db_table': 'user',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Userposition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.CharField(max_length=30)),
                ('useruid', models.CharField(db_column='userUID', max_length=36)),
            ],
            options={
                'db_table': 'userPosition',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Userregion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mainregion', models.CharField(db_column='mainRegion', max_length=30)),
                ('subregion', models.CharField(db_column='subRegion', max_length=30)),
                ('useruid', models.CharField(db_column='userUID', max_length=36)),
            ],
            options={
                'db_table': 'userRegion',
                'managed': False,
            },
        ),
    ]