from django.db import models


class Post(models.Model):

    title = models.CharField(max_length=100, verbose_name='标题')
    photo = models.ImageField(upload_to='posts/', verbose_name='图片')
    body = models.TextField(verbose_name='正文')
    created = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        ordering = ('-created',)
        verbose_name = '文章'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class Hospital(models.Model):

    name = models.CharField(max_length=50, verbose_name='名称')
    location = models.CharField(max_length=100, blank=True, verbose_name='地址')
    doctor_num = models.IntegerField(verbose_name='医生人数')
    description = models.TextField(verbose_name='医院介绍', blank=True)
    photo = models.ImageField(upload_to='hospitals/', blank=True, verbose_name='图片')

    class Meta:
        verbose_name = '医院'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
