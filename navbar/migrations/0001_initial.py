# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mptt.fields
from navbar.settings import STORAGE_CLASS


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NavBarEntry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('slug', models.SlugField(verbose_name='slug')),
                ('active', models.BooleanField(default=True, verbose_name='active')),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('title', models.CharField(help_text='mouse hover description', max_length=50, blank=True)),
                ('url', models.CharField(max_length=200)),
                ('order', models.IntegerField(default=0)),
                ('path_type', models.CharField(default=b'A', help_text="Control how this element is marked 'selected' based on the request path.", max_length=1, verbose_name='path match type', choices=[(b'N', 'Never'), (b'E', 'Exact'), (b'P', 'ExactOrParent'), (b'A', 'OnPathOrParent (default)')])),
                ('user_type', models.CharField(default=b'E', max_length=1, verbose_name='user login type', choices=[(b'E', 'Everybody'), (b'A', 'Anonymous Only'), (b'L', 'Logged In'), (b'S', 'Staff'), (b'X', 'Superuser')])),
                ('cssclass', models.CharField(max_length=100, verbose_name='Normal CSS Class', blank=True)),
                ('active_cssclass', models.CharField(max_length=100, verbose_name='Active CSS Class', blank=True)),
                ('img', models.FileField(storage=STORAGE_CLASS(), upload_to=b'navbar', null=True, verbose_name='Menu Image', blank=True)),
                ('new_window', models.BooleanField(default=False, verbose_name='Open in new window')),
                ('groups', models.ManyToManyField(to='auth.Group', null=True, blank=True)),
                ('parent', mptt.fields.TreeForeignKey(related_name='children', verbose_name='parent', blank=True, to='navbar.NavBarEntry', null=True)),
            ],
            options={
                'ordering': ('parent__id', 'order'),
                'verbose_name': 'navigation bar element',
                'verbose_name_plural': 'navigation bar elements',
            },
            bases=(models.Model,),
        ),
    ]
