# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class Test(models.Model):
    tsid = models.AutoField(db_column='tsId', primary_key=True)
    epid = models.IntegerField(db_column='epid')
    name = models.CharField(db_column='name', max_length=92)
    level = models.CharField(db_column='level', max_length=20)
    pid = models.IntegerField(db_column='pId')
    projname = models.CharField(db_column='projName', max_length=45)
    loname = models.CharField(db_column='loName', max_length=100)
    pmname = models.CharField(db_column='pmName', max_length=91)
    cdate = models.DateField(db_column='cDate')  # Field name made lowercase.
    startday = models.DateTimeField(db_column='startDay')  # Field name made lowercase.
    endday = models.DateTimeField(db_column='endDay', blank=True, null=True)  # Field name made lowercase.
    startlunch = models.TimeField(db_column='startLunch', blank=True, null=True)  # Field name made lowercase.
    endlunch = models.TimeField(db_column='endLunch', blank=True, null=True)  # Field name made lowercase.
    startdinner = models.TimeField(db_column='startDinner', blank=True, null=True)  # Field name made lowercase.
    enddinner = models.TimeField(db_column='endDinner', blank=True, null=True)  # Field name made lowercase.
    daytotal = models.TimeField(db_column='dayTotal', blank=True, null=True)  # Field name made lowercase.
    model = models.CharField(max_length=255, blank=True, null=True)
    version = models.CharField(max_length=255, blank=True, null=True)
    testitem = models.CharField(max_length=255, blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = 'test'
   
    