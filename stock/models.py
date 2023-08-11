from django.db import models

# Create your models here.
class DownRank(models.Model):
    class Meta:
        db_table = 'downrank'

    tradedate = models.DateField(verbose_name='取引日')
    marketcode = models.CharField(verbose_name='証券コード', null=False, max_length=5)
    value = models.DecimalField(verbose_name='取引値', max_digits=20, decimal_places=2)
    downvalue = models.DecimalField(verbose_name='前日比(値)', max_digits=20, decimal_places=2)
    downrate = models.DecimalField(verbose_name='前日比(率)', max_digits=5, decimal_places=2)
    turnover = models.IntegerField(verbose_name='出来高')

    def __str__(self):
        return self.marketcode