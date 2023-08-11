from datetime import datetime as dt
import os
import time

from django.core.management.base import BaseCommand, CommandError

from .library.getHtml import getHtml
from .library.customHtml import customHtml

class Command(BaseCommand):
    help = 'yahoo finance price down daily ranking.'

    def handle(self, *args, **options):
        baseurl = 'https://finance.yahoo.co.jp/stocks/ranking/down?market=tokyoAll&term=daily'
        path = './DLfiles'

        loop_flg = True

        # url生成用パラメータ
        pageCNT = 1
        url_elem = '&page='

        # file名＋fileパス生成用パラメータ
        dirname = str(dt.now().strftime('%Y-%m-%d'))

        # 下落率設定パラメータ
        dwn_ratio = -1.0
        
        while loop_flg:
            url = baseurl + url_elem + str(pageCNT)
    
            filename = dirname + '_' + str(pageCNT) + '.html'
            filepath = path + '/' + dirname + '/' + filename
    
            html = getHtml(url)

            html.html2file(filepath)

            data = customHtml(filepath)

            if data.existTBL:
                data.getRank()
                if data.ranking.at[49, 4] > dwn_ratio:
                    loop_flg = False
                else:
                    pageCNT += 1
            else:
                loop_flg = False
                os.remove(filepath)

            time.sleep(2)


# ファイル数を数える
# ファイル数だけ以下を繰り返す
# ファイルを読み込む
# データフレームを作る
# DBへインサートする
# もし明細が重複していたら処理を終了する。
