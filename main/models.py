from django.db import models
from decimal import Decimal
# Create your models here.

class Cinema(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    discription = models.TextField()
    cite_url = models.URLField(max_length=200)
    star = models.DecimalField(max_digits=2, decimal_places=1)
    like_cnt = models.IntegerField(default=0)
    location = models.CharField(max_length=50, default='')
    view_url = models.URLField(max_length=200, blank = True)
    latitude = models.FloatField(default=37.579472)     # use x
    longitude = models.FloatField(default=126.976872)   # use x
    rating_sum = models.DecimalField(max_digits = 10, decimal_places=2, default=0.0) # rating 합
    rating_cnt = models.IntegerField(default=0) # rating 등록 횟수
    tel = models.CharField(max_length=100, blank=True) # 연락처
    detail_loc = models.TextField(blank = True) # 상세 위치
    class Meta:
        db_table = 'Cinema'

    def update_rating(self, new_rating):
        new_rating = Decimal(new_rating)
        self.rating_sum += new_rating
        self.rating_cnt += 1
        self.star = self.rating_sum / self.rating_cnt
        self.save()

class Movie(models.Model):
    id = models.AutoField(primary_key=True)
    cinema = models.ForeignKey(Cinema, related_name='movies', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    poster_url = models.URLField(max_length=200, blank=True)
    class Meta:
        db_table = 'Movie'