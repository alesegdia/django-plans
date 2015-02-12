# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_countries.fields
from decimal import Decimal
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BillingInfo',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('tax_number', models.CharField(max_length=200, blank=True, db_index=True, verbose_name='VAT ID')),
                ('name', models.CharField(max_length=200, db_index=True, verbose_name='name')),
                ('street', models.CharField(max_length=200, verbose_name='street')),
                ('zipcode', models.CharField(max_length=200, verbose_name='zip code')),
                ('city', models.CharField(max_length=200, verbose_name='city')),
                ('country', django_countries.fields.CountryField(max_length=2, verbose_name='country')),
                ('shipping_name', models.CharField(max_length=200, blank=True, help_text='optional', verbose_name='name (shipping)')),
                ('shipping_street', models.CharField(max_length=200, blank=True, help_text='optional', verbose_name='street (shipping)')),
                ('shipping_zipcode', models.CharField(max_length=200, blank=True, help_text='optional', verbose_name='zip code (shipping)')),
                ('shipping_city', models.CharField(max_length=200, blank=True, help_text='optional', verbose_name='city (shipping)')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name_plural': 'Billing infos',
                'verbose_name': 'Billing info',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(db_index=True)),
                ('full_number', models.CharField(max_length=200)),
                ('type', models.IntegerField(choices=[(1, 'Invoice'), (2, 'Invoice Duplicate'), (3, 'Order confirmation')], db_index=True, default=1)),
                ('issued', models.DateField(db_index=True)),
                ('issued_duplicate', models.DateField(blank=True, null=True, db_index=True)),
                ('selling_date', models.DateField(blank=True, null=True, db_index=True)),
                ('payment_date', models.DateField(db_index=True)),
                ('unit_price_net', models.DecimalField(decimal_places=2, max_digits=7)),
                ('quantity', models.IntegerField(default=1)),
                ('total_net', models.DecimalField(decimal_places=2, max_digits=7)),
                ('total', models.DecimalField(decimal_places=2, max_digits=7)),
                ('tax_total', models.DecimalField(decimal_places=2, max_digits=7)),
                ('tax', models.DecimalField(blank=True, decimal_places=2, null=True, db_index=True, max_digits=4)),
                ('rebate', models.DecimalField(decimal_places=2, max_digits=4, default=Decimal('0'))),
                ('currency', models.CharField(max_length=3, default='EUR')),
                ('item_description', models.CharField(max_length=200)),
                ('buyer_name', models.CharField(max_length=200, verbose_name='Name')),
                ('buyer_street', models.CharField(max_length=200, verbose_name='Street')),
                ('buyer_zipcode', models.CharField(max_length=200, verbose_name='Zip code')),
                ('buyer_city', models.CharField(max_length=200, verbose_name='City')),
                ('buyer_country', django_countries.fields.CountryField(max_length=2, default='PL', verbose_name='Country')),
                ('buyer_tax_number', models.CharField(max_length=200, blank=True, verbose_name='TAX/VAT number')),
                ('shipping_name', models.CharField(max_length=200, verbose_name='Name')),
                ('shipping_street', models.CharField(max_length=200, verbose_name='Street')),
                ('shipping_zipcode', models.CharField(max_length=200, verbose_name='Zip code')),
                ('shipping_city', models.CharField(max_length=200, verbose_name='City')),
                ('shipping_country', django_countries.fields.CountryField(max_length=2, default='PL', verbose_name='Country')),
                ('require_shipment', models.BooleanField(db_index=True, default=False)),
                ('issuer_name', models.CharField(max_length=200, verbose_name='Name')),
                ('issuer_street', models.CharField(max_length=200, verbose_name='Street')),
                ('issuer_zipcode', models.CharField(max_length=200, verbose_name='Zip code')),
                ('issuer_city', models.CharField(max_length=200, verbose_name='City')),
                ('issuer_country', django_countries.fields.CountryField(max_length=2, default='PL', verbose_name='Country')),
                ('issuer_tax_number', models.CharField(max_length=200, blank=True, verbose_name='TAX/VAT number')),
            ],
            options={
                'verbose_name_plural': 'Invoices',
                'verbose_name': 'Invoice',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('flat_name', models.CharField(blank=True, max_length=200, null=True)),
                ('created', models.DateTimeField(db_index=True, verbose_name='created')),
                ('completed', models.DateTimeField(blank=True, null=True, db_index=True, verbose_name='completed')),
                ('amount', models.DecimalField(max_digits=7, decimal_places=2, db_index=True, verbose_name='amount')),
                ('tax', models.DecimalField(blank=True, max_digits=4, decimal_places=2, null=True, db_index=True, verbose_name='tax')),
                ('currency', models.CharField(max_length=3, default='EUR', verbose_name='currency')),
                ('status', models.IntegerField(choices=[(1, 'new'), (2, 'completed'), (3, 'not valid'), (4, 'canceled'), (5, 'returned')], default=1, verbose_name='status')),
            ],
            options={
                'verbose_name_plural': 'Orders',
                'verbose_name': 'Order',
                'ordering': ('-created',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField(editable=False, db_index=True)),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('default', models.BooleanField(db_index=True, default=False)),
                ('available', models.BooleanField(verbose_name='available', db_index=True, default=False, help_text='Is still available for purchase')),
                ('visible', models.BooleanField(verbose_name='visible', db_index=True, default=True, help_text='Is visible in current offer')),
                ('created', models.DateTimeField(db_index=True, verbose_name='created')),
                ('url', models.CharField(max_length=200, blank=True, help_text='Optional link to page with more information (for clickable pricing table headers)')),
                ('customized', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True, verbose_name='customized')),
            ],
            options={
                'verbose_name_plural': 'Plans',
                'verbose_name': 'Plan',
                'ordering': ('order',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PlanPricing',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, db_index=True, max_digits=7)),
                ('plan', models.ForeignKey(to='plans.Plan')),
            ],
            options={
                'verbose_name_plural': 'Plans pricings',
                'verbose_name': 'Plan pricing',
                'ordering': ('pricing__period',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PlanQuota',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField(blank=True, null=True, default=1)),
                ('plan', models.ForeignKey(to='plans.Plan')),
            ],
            options={
                'verbose_name_plural': 'Plans quotas',
                'verbose_name': 'Plan quota',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Pricing',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('period', models.PositiveIntegerField(blank=True, null=True, db_index=True, default=30, verbose_name='period')),
                ('url', models.CharField(max_length=200, blank=True, help_text='Optional link to page with more information (for clickable pricing table headers)')),
            ],
            options={
                'verbose_name_plural': 'Pricings',
                'verbose_name': 'Pricing',
                'ordering': ('period',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Quota',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField(editable=False, db_index=True)),
                ('codename', models.CharField(unique=True, max_length=50, db_index=True, verbose_name='codename')),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('unit', models.CharField(max_length=100, blank=True, verbose_name='unit')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('is_boolean', models.BooleanField(default=False, verbose_name='is boolean')),
                ('url', models.CharField(max_length=200, blank=True, help_text='Optional link to page with more information (for clickable pricing table headers)')),
            ],
            options={
                'verbose_name_plural': 'Quotas',
                'verbose_name': 'Quota',
                'ordering': ('order',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserPlan',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('expire', models.DateField(blank=True, null=True, db_index=True, default=None, verbose_name='expire')),
                ('active', models.BooleanField(db_index=True, default=True, verbose_name='active')),
                ('plan', models.ForeignKey(to='plans.Plan', verbose_name='plan')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name_plural': 'Users plans',
                'verbose_name': 'User plan',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='planquota',
            name='quota',
            field=models.ForeignKey(to='plans.Quota'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='planpricing',
            name='pricing',
            field=models.ForeignKey(to='plans.Pricing'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='plan',
            name='quotas',
            field=models.ManyToManyField(to='plans.Quota', through='plans.PlanQuota', verbose_name='quotas'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='order',
            name='plan',
            field=models.ForeignKey(related_name='plan_order', to='plans.Plan', verbose_name='plan'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='order',
            name='pricing',
            field=models.ForeignKey(blank=True, to='plans.Pricing', null=True, verbose_name='pricing'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='user'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='invoice',
            name='order',
            field=models.ForeignKey(to='plans.Order'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='invoice',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
