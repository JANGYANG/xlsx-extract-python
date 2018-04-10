# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desidered behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Matchassister(models.Model):
    matchuid = models.CharField(db_column='matchUID', max_length=36)  # Field name made lowercase.
    scoretime = models.IntegerField(db_column='scoreTime')  # Field name made lowercase.
    useruid = models.CharField(db_column='userUID', max_length=36)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'matchAssister'


class Matchcomment(models.Model):
    matchcommentuid = models.CharField(db_column='matchCommentUID', max_length=36)  # Field name made lowercase.
    content = models.TextField()
    commentdate = models.DateTimeField(db_column='commentDate')  # Field name made lowercase.
    matchuid = models.CharField(db_column='matchUID', max_length=36)  # Field name made lowercase.
    useruid = models.CharField(db_column='userUID', max_length=36)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'matchComment'


class Matchscorer(models.Model):
    matchuid = models.CharField(db_column='matchUID', max_length=36)  # Field name made lowercase.
    scoretime = models.IntegerField(db_column='scoreTime')  # Field name made lowercase.
    useruid = models.CharField(db_column='userUID', max_length=36)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'matchScorer'


class Matchuser(models.Model):
    matchuid = models.CharField(db_column='matchUID', max_length=36)  # Field name made lowercase.
    useruid = models.CharField(db_column='userUID', max_length=36)  # Field name made lowercase.
    teamuid = models.CharField(db_column='teamUID', max_length=36)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'matchUser'


class Reqmatch(models.Model):
    reqteamuid = models.CharField(db_column='reqTeamUID', max_length=36)  # Field name made lowercase.
    resteamuid = models.CharField(db_column='resTeamUID', max_length=36)  # Field name made lowercase.
    matchdate = models.DateTimeField(db_column='matchDate')  # Field name made lowercase.
    subregion = models.CharField(db_column='subRegion', max_length=36)  # Field name made lowercase.
    mainregion = models.CharField(db_column='mainRegion', max_length=36)  # Field name made lowercase.
    requestdate = models.DateTimeField(db_column='requestDate')  # Field name made lowercase.
    confirm = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'reqMatch'


class Reqteamjoin(models.Model):
    teamuid = models.CharField(db_column='teamUID', max_length=36)  # Field name made lowercase.
    useruid = models.CharField(db_column='userUID', max_length=36)  # Field name made lowercase.
    confirm = models.IntegerField(blank=True, null=True)
    requestdate = models.DateTimeField(db_column='requestDate')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'reqTeamJoin'


class Smatch(models.Model):
    matchuid = models.CharField(db_column='matchUID', max_length=36)  # Field name made lowercase.
    homescore = models.IntegerField(db_column='homeScore')  # Field name made lowercase.
    awayscore = models.IntegerField(db_column='awayScore')  # Field name made lowercase.
    stadium = models.CharField(max_length=50, blank=True, null=True)
    playingtime = models.IntegerField(db_column='playingTime', blank=True, null=True)  # Field name made lowercase.
    matchdate = models.DateTimeField(db_column='matchDate')  # Field name made lowercase.
    hometeamuid = models.CharField(db_column='homeTeamUID', max_length=36)  # Field name made lowercase.
    awayteamuid = models.CharField(db_column='awayTeamUID', max_length=36)  # Field name made lowercase.
    matchtype = models.CharField(db_column='matchType', max_length=30, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'sMatch'


class Team(models.Model):
    teamuid = models.CharField(db_column='teamUID', max_length=50)  # Field name made lowercase.
    teamemblem = models.CharField(db_column='teamEmblem', max_length=100, blank=True, null=True)  # Field name made lowercase.
    teambirth = models.IntegerField(db_column='teamBirth', blank=True, null=True)  # Field name made lowercase.
    teamcolor = models.IntegerField(db_column='teamColor', blank=True, null=True)  # Field name made lowercase.
    captainuid = models.CharField(db_column='captainUID', max_length=36)  # Field name made lowercase.
    teamname = models.CharField(db_column='teamName', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'team'


class Teamformation(models.Model):
    teamuid = models.CharField(db_column='teamUID', max_length=36)  # Field name made lowercase.
    formation = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'teamFormation'


class Teammanager(models.Model):
    teamuid = models.CharField(db_column='teamUID', max_length=36)  # Field name made lowercase.
    playeruid = models.CharField(db_column='playerUID', max_length=36)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'teamManager'


class Teamregion(models.Model):
    teamuid = models.CharField(db_column='teamUID', max_length=36)  # Field name made lowercase.
    mainregion = models.CharField(db_column='mainRegion', max_length=30)  # Field name made lowercase.
    subregion = models.CharField(db_column='subRegion', max_length=30)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'teamRegion'


class Test(models.Model):
    name = models.CharField(max_length=36, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    startday = models.TimeField(db_column='startDay', blank=True, null=True)  # Field name made lowercase.
    endday = models.TimeField(db_column='endDay', blank=True, null=True)  # Field name made lowercase.
    startlunch = models.TimeField(db_column='startLunch', blank=True, null=True)  # Field name made lowercase.
    endlunch = models.TimeField(db_column='endLunch', blank=True, null=True)  # Field name made lowercase.
    tsid = models.AutoField(db_column='tsId', primary_key=True)  # Field name made lowercase.
    epid = models.IntegerField(db_column='epId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'test'


class User(models.Model):
    useruid = models.CharField(db_column='userUID', max_length=36)  # Field name made lowercase.
    username = models.CharField(db_column='userName', max_length=50)  # Field name made lowercase.
    encryptedpw = models.CharField(db_column='encryptedPW', max_length=80)  # Field name made lowercase.
    email = models.CharField(max_length=80)
    height = models.IntegerField(blank=True, null=True)
    weight = models.IntegerField(blank=True, null=True)
    teamuid = models.CharField(db_column='teamUID', max_length=36, blank=True, null=True)  # Field name made lowercase.
    salt = models.CharField(max_length=36, blank=True, null=True)
    userbirth = models.DateField(db_column='userBirth', blank=True, null=True)  # Field name made lowercase.
    job = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField()
    phonenum = models.CharField(db_column='phoneNum', max_length=36)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'user'


class Userposition(models.Model):
    position = models.CharField(max_length=30)
    useruid = models.CharField(db_column='userUID', max_length=36)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'userPosition'


class Userregion(models.Model):
    mainregion = models.CharField(db_column='mainRegion', max_length=30)  # Field name made lowercase.
    subregion = models.CharField(db_column='subRegion', max_length=30)  # Field name made lowercase.
    useruid = models.CharField(db_column='userUID', max_length=36)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'userRegion'
