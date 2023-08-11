from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from stock.models import PriceDown

from .library.customHtml import customHtml

import os

class Command(BaseCommand):
    help = 'price down daily ranking insert db.'

    @transaction.atomic
    def handle(self, *args, **options):
        '''
        del_db = PriceDown.objects.all()
        del_db.delete()
        '''
        DirPath = './DLfiles/2023-07-24/'
        FileList = os.listdir(DirPath)

        for fname in FileList:
            data = customHtml(DirPath + fname)
            dataf = data.getRank()

            for i in dataf.index:
                ins_db = PriceDown(TradeDate=dataf.loc[i][0], MarketCode=dataf.loc[i][1], 
                                    value=dataf.loc[i][2], DownValue=dataf.loc[i][3], 
                                    DownRate=dataf.loc[i][4], turnover=dataf.loc[i][5])
                ins_db.save()
