from django.db import models
from django.conf import settings


class Ad(models.Model):
	id = models.AutoField(primary_key=True)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,  verbose_name="Пользователь")
	title = models.CharField(max_length=80, verbose_name="Название")
	description = models.CharField(max_length=1000, verbose_name="Описание")
	image_url = models.CharField(max_length=255, verbose_name="Ссылка на изображение")
	category = models.CharField(max_length=80, verbose_name="Категория")
	condition = models.CharField(max_length=80, verbose_name="Состояние")
	created_at = models.DateField(blank=True, null=True, verbose_name="Дата создания")


class ExchangeProposal(models.Model):
	id = models.AutoField(primary_key=True)
	ad_sender = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='ad_sender', verbose_name="Отправитель")
	ad_receiver = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='ad_receiver', verbose_name="Получатель")
	comment = models.CharField(max_length=1000, verbose_name="Категория")
	status = models.CharField(max_length=20, verbose_name="Состояние")
	created_at = models.DateField(blank=True, null=True, verbose_name="Дата создания")