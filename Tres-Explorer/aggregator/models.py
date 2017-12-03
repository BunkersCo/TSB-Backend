from __future__ import unicode_literals

from django.db import models
from django import forms
from jsonfield import JSONField
from django.utils import timezone

# Create your models here.

from django.contrib.auth.models import AbstractUser, User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

# class User(AbstractUser):

#     # TODO: add validator to phone_number
#     phone_number = models.CharField(verbose_name='Phone Number', max_length=15,
#                                     null=True, blank=True)
#     weixin_id = models.CharField(verbose_name='wid', max_length=100,
#                                  null=True, blank=False)
#     weixin_veri_mark = models.CharField(verbose_name='wvm', max_length=100,
#                                  null=True, blank=False)
#     #address = models.ForeignKey('products.Area', verbose_name="Address",
#     #                           null=True, blank=True)
#     shop_name   = models.CharField(verbose_name='Shop Name', max_length=200,
#                                    null=True, blank=True) 
#     shop_desc   = models.CharField(verbose_name='Shop Description', max_length=1000,
#                                    null=True, blank=True)
#     shop_notice = models.CharField(verbose_name='Sho Notice', max_length=1000,
#                                    null=True, blank=True)

#     #favors = models.ManyToManyField('products.Product', verbose_name='fans', related_name='fans')

#     #REQUIRED_FIELDS = ['phone_number', 'email']

#     class Meta:
#         db_table = 'accounts_user'
#         verbose_name = verbose_name_plural = "accounts"
#         pass


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    '''automatically generated Token for every new user'''
    if created:
        Token.objects.create(user=instance)

class Userfavorite(models.Model):

	entity_type = models.CharField(max_length=200)
	entity_id = models.CharField(max_length=200)
	user_id = models.CharField(max_length=200)
	created = models.DateTimeField('created date')
	def __str__(self):
		return self.created

class Userclasstrack(models.Model):

	class_id = models.CharField(max_length=200)
	user_id = models.CharField(max_length=200)
	def __str__(self):
		return self.user_id

class Usercontent(models.Model):

	title = models.CharField(max_length=200)
	body = models.TextField(max_length=2200)
	link = models.CharField(max_length=200)
	user_id = models.CharField(max_length=200)
	created = models.DateTimeField('created date')
	status = models.CharField(max_length=200)
	def __str__(self):
		return self.status

class Userreview(models.Model):

	title = models.CharField(max_length=200)
	body = models.TextField(max_length=2200)
	rating = models.CharField(max_length=200)
	entity_type = models.CharField(max_length=200)
	entity_id = models.CharField(max_length=200)
	user_id = models.CharField(max_length=200)
	created = models.DateTimeField('created date')
	def __str__(self):
		return self.created

class Usercheckin(models.Model):

	studio = models.CharField(max_length=200)
	date = models.CharField(max_length=200)
	user_id = models.CharField(max_length=200)
	created = models.DateTimeField('created date')
	def __str__(self):
		return self.created

class Classentry(models.Model):

	date = models.CharField(max_length=200)
	length = models.CharField(max_length=200)
	price = models.DecimalField(max_digits=6, decimal_places=2)
	level = models.CharField(max_length=200)
	instructor_type = models.CharField(max_length=200)
	facility_quality = models.CharField(max_length=200)
	overall_rating = models.CharField(max_length=200)
	created = models.DateTimeField('created date')
	updated = models.DateTimeField('updated date')
	def __str__(self):
		return self.updated

class Facebookfriend(models.Model):

	facebook_id = models.CharField(max_length=200)
	friend_id = models.CharField(max_length=200)
	created = models.DateTimeField('created date')
	def __str__(self):
		return self.created

class Instructorentry(models.Model):

	name = models.CharField(max_length=200)
	bio = models.TextField(max_length=2200)
	headshot = models.FileField(upload_to='InstructorEntry/headshot/%Y/%m/%d')
	created = models.DateTimeField('created date')
	updated = models.DateTimeField('updated date')
	def __str__(self):
		return self.updated

class Userprofile(models.Model):

	user_id = models.CharField(max_length=200)
	admin_status = models.CharField(max_length=200)
	profile_visible_to = models.CharField(max_length=200)
	allow_followers = models.CharField(max_length=200)
	profile_picture = models.FileField(upload_to='UserProfile/profile_picture/%Y/%m/%d')
	updated = models.DateTimeField('updated date')
	created = models.DateTimeField('created date')
	def __str__(self):
		return self.created

class Usertag(models.Model):

	entity_type = models.CharField(max_length=200)
	entity_id = models.CharField(max_length=200)
	tag = models.CharField(max_length=200)
	user_id = models.CharField(max_length=200)
	created = models.DateTimeField('created date')
	def __str__(self):
		return self.created

class Newsfeed(models.Model):

	date = models.CharField(max_length=200)
	title = models.CharField(max_length=200)
	body = models.TextField(max_length=2200)
	link = models.CharField(max_length=200)
	user_id = models.CharField(max_length=200)
	def __str__(self):
		return self.user_id

class Studioentry(models.Model):

	name = models.CharField(max_length=200)
	classpass_id = models.CharField(max_length=200)
	slug = models.SlugField(max_length=255, unique=True, default=name)
	description = models.TextField(max_length=2200)
	latitude = models.CharField(max_length=200)
	longitude = models.CharField(max_length=200)
	address = models.CharField(max_length=200)
	address_2 = models.CharField(max_length=200)
	city = models.CharField(max_length=200)
	state = models.CharField(max_length=200)
	zipcode = models.CharField(max_length=200)
	country = models.CharField(max_length=200)
	website = models.CharField(max_length=200)
	username = models.CharField(max_length=200,default=0)
	phone = models.CharField(max_length=200)
	studio_picture = models.FileField(upload_to='StudioEntry/studio_picture/%Y/%m/%d')
	updated = models.DateTimeField(default=timezone.now())
	created = models.DateTimeField(default=timezone.now())
	def __str__(self):
		return self.name

class StudioentryForm(forms.ModelForm):

	class Meta:
		model = Studioentry
		fields = ['name', 'classpass_id', 'slug', 'description', 'latitude', 'longitude', 'address', 'address_2', 'city', 'state', 'zipcode', 'country', 'website', 'phone', 'studio_picture', 'updated', 'created']

class NewsfeedForm(forms.ModelForm):

	class Meta:
		model = Newsfeed
		fields = ['date', 'title', 'body', 'link', 'user_id']

class UsertagForm(forms.ModelForm):

	class Meta:
		model = Usertag
		fields = ['entity_type', 'entity_id', 'tag', 'user_id', 'created']

class UserprofileForm(forms.ModelForm):

	class Meta:
		model = Userprofile
		fields = ['user_id', 'admin_status', 'profile_visible_to', 'allow_followers', 'profile_picture', 'updated', 'created']

class InstructorentryForm(forms.ModelForm):

	class Meta:
		model = Instructorentry
		fields = ['name', 'bio', 'headshot', 'created', 'updated']

class FacebookfriendForm(forms.ModelForm):

	class Meta:
		model = Facebookfriend
		fields = ['facebook_id', 'friend_id', 'created']

class ClassentryForm(forms.ModelForm):

	class Meta:
		model = Classentry
		fields = ['date', 'length', 'price', 'level', 'instructor_type', 'facility_quality', 'overall_rating', 'created', 'updated']

class UsercheckinForm(forms.ModelForm):

	class Meta:
		model = Usercheckin
		fields = ['studio', 'date', 'user_id', 'created']

class UserreviewForm(forms.ModelForm):

	class Meta:
		model = Userreview
		fields = ['title', 'body', 'rating', 'entity_type', 'entity_id', 'user_id', 'created']

class UsercontentForm(forms.ModelForm):

	class Meta:
		model = Usercontent
		fields = ['title', 'body', 'link', 'user_id', 'created', 'status']

class UserclasstrackForm(forms.ModelForm):

	class Meta:
		model = Userclasstrack
		fields = ['class_id', 'user_id']

class UserfavoriteForm(forms.ModelForm):

	class Meta:
		model = Userfavorite
		fields = ['entity_type', 'entity_id', 'user_id', 'created']
