from django.db import models

from ckeditor.fields import RichTextField


class Post(models.Model):

    title = models.CharField(max_length=100, verbose_name='标题')
    photo = models.ImageField(upload_to='posts/', blank=True, verbose_name='图片')
    body = RichTextField(verbose_name='正文')
    created = models.DateField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        ordering = ('-created',)
        verbose_name = '文章'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class Hospital(models.Model):

    # Hospital ranks
    GRADE_ONE_LEVEL_A = '1A'
    GRADE_ONE_LEVEL_B = '1B'
    GRADE_ONE_LEVEL_C = '1C'
    GRADE_TWO_LEVEL_A = '2A'
    GRADE_TWO_LEVEL_B = '2B'
    GRADE_TWO_LEVEL_C = '2C'
    GRADE_THREE_LEVEL_A = '3A'
    GRADE_THREE_LEVEL_B = '3B'
    GRADE_THREE_LEVEL_C = '3C'

    RANK_CHOICES = (
        (GRADE_THREE_LEVEL_A, '三级甲等'),
        (GRADE_THREE_LEVEL_B, '三级乙等'),
        (GRADE_THREE_LEVEL_C, '三级丙等'),
        (GRADE_TWO_LEVEL_A, '二级甲等'),
        (GRADE_TWO_LEVEL_B, '二级乙等'),
        (GRADE_TWO_LEVEL_C, '二级丙等'),
        (GRADE_ONE_LEVEL_A, '一级甲等'),
        (GRADE_ONE_LEVEL_B, '一级乙等'),
        (GRADE_ONE_LEVEL_C, '一级丙等'),
    )

    name = models.CharField(max_length=50, verbose_name='名称')
    location = models.CharField(max_length=100, blank=True, verbose_name='地址')
    rank = models.CharField(choices=RANK_CHOICES, max_length=10, verbose_name='医院等级')
    doctor_num = models.IntegerField(null=True, blank=True, verbose_name='医生人数')
    phone = models.IntegerField(verbose_name='电话')
    description = models.TextField(verbose_name='医院介绍', blank=True)
    photo = models.ImageField(upload_to='hospitals/', blank=True, verbose_name='图片')

    class Meta:
        verbose_name = '医院'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
