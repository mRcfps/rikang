from django.db import models
from django.core.validators import MaxValueValidator


class Post(models.Model):

    title = models.CharField(max_length=100, verbose_name='标题')
    photo = models.ImageField(upload_to='posts/', blank=True, verbose_name='图片')
    body = models.TextField(verbose_name='正文')
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
    phone = models.IntegerField(verbose_name='电话')
    description = models.TextField(verbose_name='医院介绍', blank=True)
    photo = models.ImageField(upload_to='hospitals/', blank=True, verbose_name='图片')

    class Meta:
        verbose_name = '医院'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def doctor_num(self):
        return self.doctors.count()


class DoctorComment(models.Model):

    patient = models.ForeignKey('users.Patient', related_name='comments', verbose_name='全部评价')
    doctor = models.ForeignKey('users.Doctor', related_name='comments', verbose_name='全部评价')
    anonymous = models.BooleanField(default=False, verbose_name='匿名回答')
    ratings = models.PositiveIntegerField(validators=[MaxValueValidator(5)], verbose_name='评分')
    created = models.DateField(auto_now_add=True, verbose_name='创建时间')
    body = models.TextField(verbose_name='评论内容')

    class Meta:
        verbose_name = '医生评论'
        verbose_name_plural = verbose_name
