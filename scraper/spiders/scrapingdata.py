from scrapy.conf import settings
from urllib import urlencode
from scrapy import Request
import scrapy
import re
import json
import csv
import os
import time
import requests

# from pyvirtualdisplay import Display
# CWD = os.path.dirname(os.path.abspath(__file__))
# driver_path = os.path.join(CWD, 'bin', 'chromedriver')
# driver_log_path = os.path.join(CWD, 'bin', 'driver.log')

keys_EMC = []
keys_HMM = []
keys_COSCO = []
keys_MAERSK = []
keys_ZIM = []
# keys_ZIM = ['TCKU1509890']
keys_YANG = ['SESU2127602', 'SESU2127618', 'SESU2127665', 'SESU2127670', 'SESU2127686', 'SESU2127691']

try:
    with open(os.path.abspath('inputData.csv'), 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[2] == "EMC":
                keys_EMC.append(row[0])
            if row[2] == "HMM":
                keys_HMM.append(row[0])
            if row[2] == "COSCO-SHA":
                keys_COSCO.append(row[0])
            if row[2] == "MAERSK":
                keys_MAERSK.append(row[0])
            if row[2] == "ZIM":
                keys_ZIM.append(row[0])

except Exception as e:
    print('parse_csv Function => Got Error: {}'.format(e))

    with open('/home/ubuntu/Marin-Guru/container_scraping/ScrapingContainer-MySQL/inputdata/inputData.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[2] == "EMC":
                keys_EMC.append(row[0])
            if row[2] == "HMM":
                keys_HMM.append(row[0])
            if row[2] == "COSCO-SHA":
                keys_COSCO.append(row[0])
            if row[2] == "MAERSK":
                keys_MAERSK.append(row[0])
            if row[2] == "ZIM":
                keys_ZIM.append(row[0])


class SiteProductItem(scrapy.Item):
    container_num = scrapy.Field()
    container_sizetype = scrapy.Field()
    date = scrapy.Field()
    container_moves = scrapy.Field()
    location = scrapy.Field()
    vessel_voyage = scrapy.Field()
    vgm = scrapy.Field()
    weight = scrapy.Field()
    origin = scrapy.Field()
    landing_port = scrapy.Field()
    TS_port = scrapy.Field()
    discharging_port = scrapy.Field()
    destination = scrapy.Field()
    ServiceTerm = scrapy.Field()


class NewEvents (scrapy.Spider):

    name = "scrapingdata"
    allowed_domains = ['www.shipmentlink.com', 'www.hmm.co.kr', 'elines.coscoshipping.com',
                       'www.cosco-usa.com/', 'my.maerskline.com', 'www.zim.com']

    # start_urls = ['http://www.zim.com/pages/findcontainer.aspx?searchvalue1=TCKU1509890']

    start_urls = [
        'https://www.shipmentlink.com/servlet/TDB1_CargoTracking.do',
        'http://www.hmm.co.kr/ebiz/track_trace/trackCTPv8.jsp?'
        'blFields=undefined&cnFields=undefined&numbers=&numbers='
        '&numbers=&numbers=&numbers=&numbers=&numbers=&numbers='
        '&numbers=&numbers={}&numbers=&numbers=&numbers=&numbers='
        '&numbers=&numbers=&numbers=&numbers=&numbers=&numbers=&numbers=&numbers=&numbers=&numbers=',
        'https://my.maerskline.com/tracking/search?searchNumber={}',
        'http://www.zim.com/pages/findcontainer.aspx?searchvalue1={}',
        'http://www.yangming.com/e-service/Track_Trace/mul_ctnr.aspx?str={},&rdolType=CT'
                  ]

    def start_requests(self):
        for start_url in self.start_urls:

            if 'www.shipmentlink.com' in start_url:
                for key in keys_EMC:
                    form_data = {'CNTR': key, 'TYPE': 'CNTR', 'blFields': '1', 'cnFields': '1', 'is-quick': 'Y'}
                    yield Request(url=start_url,
                                  headers={
                                            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                            'Chrome/64.0.3282.186 Safari/537.36',
                                            'Content-Type': 'application/x-www-form-urlencoded'
                                           },
                                  callback=self.parse_product,
                                  method='POST',
                                  body=urlencode(form_data),
                                  dont_filter=True)

            if 'www.hmm.co.kr' in start_url:
                for key in keys_HMM:
                    form_data = {'number': key, 'numbers': key}
                    yield Request(url=start_url.format(key),
                                  headers={
                                      'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)'
                                                    ' Chrome/64.0.3282.186 Safari/537.36',
                                      'Content-Type': 'application/x-www-form-urlencoded',
                                      'Referer': 'http://www.hmm.co.kr/ebiz/track_trace/main_new.jsp?type=2&number=SESU2195470'
                                                 '&is_quick=Y&quick_params='
                                  },
                                  method='POST',
                                  callback=self.parse_product,
                                  body=urlencode(form_data),
                                  dont_filter=True)

            if 'elines.coscoshipping.com' in start_url:
                for key in keys_COSCO:
                    form_data = {'mainForm': 'mainform', 'cargoTrackSearchId': 'CONTAINER', 'cargoTrackingPara': '1',
                                 'cnFields': 'SESU2198951', 'num': '0', 'onlyFirstAndLast': 'false',
                                 'num1': '1', 'num2': '0', 'num3': '0', 'num4': '0', 'num5': '0', 'num6': '0',
                                 'onlyFirstAndLast2': 'false', 'validateCargoTracking': 'true',
                                 'cargoTrackingRedirect': 'true', 'numberType': 'CONTAINER', 'containerSize': '1',
                                 'bookingNumbers': '0',
                                 'javax.faces.ViewState': 'H4sIAAAAAAAAANVdXYwkx13v2739uL3z3d6nHZ/tnOOzz77Ys9PdM93' \
                                                          'TdoK99yUv2fMt3ouFHYlN70zfbt/NTPd19+zOBnFyJHAEPACCPCCZDwmEgp' \
                                                          'Q3BE8EBYFARgoSRigSUqTgJx4AISQUQkSgq6u656Orq3t2q3r/7MPM7N1s16/+/' \
                                                          '3/9v6vqm/8qzbi+J52+b+6YlV5gtytvmv72bdOdmfvHP/+LC1/+u2lp6pa00HbM1i2' \
                                                          'zGTjeinQs2PYsf9tpt/ru629I4c+0tDsvSUfDT0f+J5CO3d+wW4Es16o9Tzr7pdXo0W2' \
                                                          'zu1W5s3nfagav/erf/vTvLPovtackqe+GfzTjhj+9h9Kj8EHhb488qYL+pl+5ZzYtv9J' \
                                                          '0Oq7TtbpB5Ysr1+PPl9c8x7W8YO8L1p4vkZ8z4QM96eRgwJvdXmf4P91AWjCDwLM3e4Hl' \
                                                          'h/M+O5j3sueZe6u2H/S/+vHTv/nX5m9NS0dWpKO+/RUrQjm9iyY4Hf7RC3R064EZWG+GZL' \
                                                          'G8dXPH8t79mz/6/K9/+J3bU9LUqnSs2TZ9/y2zYwXSmYgkSwjh0noIprv12qq04Id/04qeEUg' \
                                                          'X8DdsZ2nd8myzbX/F3Gxbr/VddweRSfLR64lwNs+Ew1f8XpeAQa9tK/Ary2trqys3b5DvhZjrG' \
                                                          'V+0O267csO6Z/bawS38j5eXXbe9d9d5YHX/8xsvv/vhG/ffOIFot/uK9NyS29ts282lpultOXc' \
                                                          '9s/kgRL+0Y1u7P+luVfrbQacdCoH5yfesv+/3Q0bWJ2PkmmfvhAQYZhmawVwgnRuw7e62GSx71no' \
                                                          'IH/3nQvjFqYg3U2S6EY0WyC/o9Qxi/KURzNedbmDaXctb6d5zENV7/kACR+TxGPownwwVi8Hg6YvDI' \
                                                          '8UUR2/ndnXpFTrFRn67ZrfbI7T7s4h2L2XR7oYZmJnyT+g17zm7K92W1U8Wd7QgVrqBtWV5Zz75' \
                                                          '3d//wVe/1phCIj6zY7Z7VrhwFgffe6vX2bS8D7759aeP/8b3fzlaqP8b/qCHP55BdfR6cYToj9' \
                                                          'Db84E0E4l28mcz0Z/NUCgYSFoek16tvtqM/xWDvNU2twZyfiljbSaL68UPPv6p7x7/+rtT0sx70mN' \
                                                          'tp2m230HzD8XpPemY39vs2EFgtd6LyGK3VqWTyb9F3xtdvkSjrRIiIhga0hZHXDeZUy13TowZobd6' \
                                                          '9Dwkw/PRN5uBkiGrM/uRVfR6vj8Za0MsL9Kn9WaoQR1vT30VW4GqXD0o1lCAdsNHbQ9+leWqGy2RWt' \
                                                          'YSCRXtMKi81TIbKudgBYvoi+F/zU4wvxoPXqwmkzuqobmh39bQy9vhP80RrvNm+uXJmf5YIqrroV1MI' \
                                                          'BxNPk1lgJwLuXU1i1srXbeXbdEJj/B6HFVn1xynbZnd71zy3v+HD//730J19l6sztwjkfq5H4wt8mhGH' \
                                                          'SmE89ksOHd6QUE8PWvHk47uOHZLGvyEVtolo6DXXWymh1b9RoCseY1IUE2ROUuQmpIg9vj1Qx7fED7+S7' \
                                                          'kqOMKi1A6srPhB0YRDuVIIitJIhp4dXdLFFfjzGd7nyu3QTb2+cndjbfmtmzFWvHaOYPdhNpBOeFboyHiWd' \
                                                          '3fPjSzsziRq6w+iOT8MdTyeTI4wqioUshsHJXs0+6HP34hg/OFBKWgE0mJCwdthFGVuWTwtE3GdPycpBVzn' \
                                                          'hHoj/vNH/cktG1sqdOFSsS8vcRIDjD48QC9d9OJEPEUvEagd9N0QxenYq9GjqcvVKjgpnCPAKGBlqGBlClgFK' \
                                                          'lhlEGdkxcTT6MML6OUqikqiqTWGyM9BHNHbbvQygdGscwmMOGhvFd66mcW4Cs8A3mLCM5ALzwDeCsMzUArPQAU' \
                                                          '6A7XwDGpAZ1CbQKk0oCiVOlBi1gPpMjNbEsHXgWoUPdQoc7a/6mzZXQAploKyoMEkpqoVkwWgullXciKBmvhkTUE' \
                                                          'B0GFSUNWLCQBQ06arxeADtWt6LU9+xSf7SP23Ws/KYI1GD0+mamEJxQFoYzYx4WQuNfF5KxzmGWrWpEfZ+hSFcLhoI' \
                                                          'tfg+TFzBNgEBBfP++ObaDFsm90ti0uR6YBLgcVReN4I4ajGxg3PiBLc+gj7udQCBLL/wCUCUWTMS/fXxatNFt3g5fgJ' \
                                                          '3Yw8uolPiD/hWW3L9K0NNLzXMQPb6W6gJQFgLZxFOJx7q2YrtBEbdyOWshKd+2/JwPZ0YoBPjzDv2t619lu9Tsw88b' \
                                                          'xjyHwdXmZ0jgBj44aXvSC45eJOiy7e+2eREF7QT0iosHHDi1UJbpWNG16QSnCHUerTFBUaK6iq+IzrsyMr5o7XsjwU' \
                                                          'eg7ZGgBm5mJ2aMwlDXXADkCWkamLz5ORsuNQqY132ZE5QfGq9HQccOMhjRrn6uaMrO8739AQz99TmL8Gnr4OL2mAM27' \
                                                          '1HDkRnycYIxS8WBwTSouXrD7UM8t7yY7RAl58j2mhU1Y354a/GbWWJynwwnZMnQbbPZDFq94X8ksAQaPBufWbpo+LAeH' \
                                                          'sL9FEh6XjSkg+j6+WoTCSE+3l1Jhnk0JG3OzPW5nTOM4ktPjQPUVo8fsbni+w08IAav6NekH8QK2yoRXED9SSGnpB/EBt' \
                                                          'ndGIl5zWIAZOa/D2BChaJi7SGsWKtIXMkME9Pknr5MXRNloDXgYds9UoSjPe2zzS6vUptHXMbK86kS+FjIoexya8HQeKP' \
                                                          'UkbUd7ewqTeis4MXfEj4r0n85t2F1HNnxCV70kvZ+x5sdqVu+ZWtB3tZt/1LN+3na6Ef46ciHawP4F3poXfHPva7sL7X/' \
                                                          'r+t3/8a1PR184mXxt84/d+4ZfW/+O9jz8XbdkNUTzreFsV0zWb2xbleSsdt/3B1dapfzr6V986gbe2TX9r9yekq8/97EB' \
                                                          '4l29Xui0kPTcC5dLrl66ExL5y6dVLVxCvr/zc8K5hvBvWdfu796XtiTY+X3qj1lBfbtQvRTs9P/+Z4uN/po9SUSdbTrPX' \
                                                          'sboBcyt3qSWitNxzdt5o6pEp98ywCT8CCcCfTCrr6I/+NHr99u7r0mdTvLth+83tCYTngWRPKjxG9eWGlik82QCw9JBMY' \
                                                          'ubugVFbeGbw9HXL9JrbKy3u6Qw3j5fMQIQTL7P1gCpQDxh6vh6gjI85Oe5KGbzDRIqtOUfjE+9q8OWDVINJ55aeZe1H5T' \
                                                          'tFQ+5pjrTeSo3J2zGZyC3i7cjSyqSM0cXv/E0bJ7ZTxIXgC81u4L1tdUzvgcCKDbWsd3vvVugfQHALWEq9wXSMxRvowlp' \
                                                          '9cgNdr9YKGOhMtc6kmvicGClb1FRhcnt6hHJrpmcKcSk+PU7HB1sDQqpV8WrvfHSIhxlY14fnK2SuGdsoSPitkPQm92C' \
                                                          'UkmvJobp4dT8TdV3k0hadvPZK1qEo79jW7tuOk3ssymx02orlx8dJRWerrUb/9ui/Tn/5w+oP/2VKOroizW+b/nbTaVm' \
                                                          'r6HybXmga9tATHluV5pG26ZlbFvl9bsf0bLMbRL/ic6gCaeqL6+FLCE2SUKx+dCd1iM8RdQIp4B2aTZiSMMRX05nDl9A' \
                                                          'WlvJ3YtejXkK3D3Py4gv0bAVw8BOycgEUWwW8fUCao59DCt7Fpn2TgveKSLvDOZQQvygYS1I+jABoMLp4i/ip1OiY8yr' \
                                                          'QMpHaYGAGWgNRjTwhV8SL2ek4tUfqLSW07eEmG02rRkPWgRZO63oKKVDZrzcobCyrqy4hDtBFVjeYqlQR71uMNSk7Dno' \
                                                          'TlHDZR5MyizjivY040WbEg8rVEqqfrDmL9ytItmToiAfe2ZIsSzh0fCOoRVqrMjDD21eEMctU6S2hhplJKXjbhzClFAZ' \
                                                          'meFuHMGY14W69llQeeDdVTuB41+DtVcKEqiXl4cxEwWj5LHOGQDsY0aEHmZiBdi2ibf2ZmIE63GhLP2XJifdBRh1ZDai' \
                                                          'N1KppL7+EvnIKR8R7SKl5ii9hPZlRb5Yb8NTSHAGGjpvvBl5UxUVnP0/gTx5HHwb+5P6Lu+Oe6CQTCuOPUb81mwnw9Cx' \
                                                          'hgsZCDU/TEtQ6CzW8NAdB3WChhpd/IKiN8a6L8Zx6Ia+JEbKq4rOEz1HPGsGpjI0dy/MF7AffRy4jHY/J4tt2WJwRn6i' \
                                                          'fj52XQlJ0Mk4/8T+W/mAsG/IvtPKT3tybuybwLwx4/uYcAUbljniRziYVvFQQIZXMQg0vLUNQK5SVwLv8U5+AvfByQYR' \
                                                          'QakioFGpWprb0DubFnegOGJ9UPKvcg5YuF1KGwNJYufv2vLBqaazcPXpeWHWmI1LCvU2s0curI8mxoaryruzRGhfnY+n' \
                                                          'grQsOdLZd2mjr4tlPYQDvbRGUQh5lqocia7zPl8g+bGF4quITcedsn0R5+E6lm/0wZOVetkR9qLTTNOMDTVSVM1OnUxN' \
                                                          '9PKW9orHhuW5Rq7KSCRieCxUBVjMBwytrRYBrmYDhpYMjwPVMwPBSpxFgLRMwvKxpBFjPBAwvYRoBbgTSBZJ4jPKOt+x' \
                                                          'u61ovCDJTddOPPGkZ7Yd3PbtjjW9xCD91zG5rM3pC5Tr+DT8vb8/DsV27tWUF75heID2NP2/QkWWrYnj53YjIRpKCy9y' \
                                                          'dNpqCS3sP3PO36RxlfLke2c8o849jeF2up1PAwltfBGy4wk4Q/2jNs7tBrj9UXmaVxnR4S4jQMVxEx6NtqGLS0vvYhjp' \
                                                          'Ou6E9KLBoJ1djBaTI4u6XZB/VUyc0gpqeleWiM4Dn75MZKEVnAC8AIDNQi84AXkRAZlAb3xxFiml3yCmcAs/G3kdhjRl' \
                                                          'QZ149xS91sOh023u3bM8PlrutVXOitAGs7pTcjeFKCSXLM+luvkLu5pmxW7GXh+4H4W0l0hiLucSnYgcax6vwzAhuwJ' \
                                                          'NTSOGZC4xUofEiq7J3OEnqnAUlXj+lCVTspMcxEYBnb7EIqLQZZrVRMmcIzx7jGWbc5JjYuBKU8kI30qkT9l5OplTZc' \
                                                          'xRfAriUdc2UqL6vfURr6ZaC5EBq4fRhK7ISKm8XM89uABjOzGJcTNRAVSqKYHKYLb72yCAbUD2NwqZPRYfmbEQZ5Q10' \
                                                          '/k2kRN68uXyDB+ZYeURv53ZflJ5ZCqyO2zYDy1/qhMR6Jf4Vn7YlSUfMT75nfbe/z/mdieeXPS0mo+BVkDCj6kzU8MpIGL' \
                                                          'XGRA0vz41R67m6RLxlZ5ANXsYdk63BRA0vv41RG5QDlgbMlhV4uOcIsBz3swSDdywavxlk9liNXZae0YU2fDMILCJr1L0' \
                                                          '4MWp4C5Ggpu7FiVFDFWgtFOjZnh/KMv8TqaMXVixSwjFm2WOLX6gvUhXFWPbxVtvkepilO1TnjDvjZICXms0RYCwWHab' \
                                                          'BH2qWhUKyWYyLbTpVeLjnCDCKXEJV5jrTrVKA5uMVOUc24OEmsiHnOf+NsrbADQknVJutG0zhBJriUpQc4YSHmwgnMzen' \
                                                          'AM3NKWoOueHhJuRWmeQGmtNTajnkhoebkLtGOxcHx7M1eOYZn4vDts5As4kK7drnYRGBh5uISD3XOjOL09jCPhR3t1Dha' \
                                                          '6I60oMit1DgJqb4Igq1ph3gmrHMtQXPu8Bri+1cAM15K1rO2oKHm6wtLSeh2DjMcqkCL2+A2a3nsBsebsJuVmpThxq663k' \
                                                          '5B3h+AiE3KyerQ42G9bwwHp7pIOQ2WOSGGt/pCgs11DBJV1mooUYbeo2FGqoDrNfzjPRhHAEUUw2qa6NryVEcA8M2VQzsT' \
                                                          'DTQDAVs+My2vemZ3l7yDwuDzZkDCnbNjpX8dsE1t+yuGTjeUvKpct/H8wwdoOEbrDzLd3pe06qsNz3bDUYJkCbiEAEWfjT' \
                                                          '0+QeYGOjjv7sJIWg3au2TENEgQ59/SAESSOdaZmBueXZrKf6QzBt98ccHn97xacQC1P4o+KLG8fxsA6q71KBUOhpQnY0G9' \
                                                          'aCuOLAvLeseH1AoA+wFI5ud6hSuQvVpGgqFslANBWpYS1EWqt/VUCmUhRpuyjqFslB9wwYjE12Hp+vxXTpVijRAjYZl6o1' \
                                                          'ghMDw7BMmMNM8Hcatb4Re8DQ/ppeC+o7yNxWH8so7szjxPbaKwUSAH/JQ4O3VhesGXam9j7pBXS1wgfXEhYM6PMuIJS+n4' \
                                                          'AzwpqU5AoxBbHjGEhM7p9wM8IooQmyZQWx4rj8mdk7hFuAtU4TY1GumCLHhRQOY2Fqu1WB27nKyGtnFZlVssVmr5hebKRC' \
                                                          'wzWBKKTy7QaRULe6ycN68WujS9WEawjMHhIa1eJN6fHC5BlSZarnNJAaz7Vu8V1h4ge/PK9T0Al5h5gofYzJQJa5pxZc05' \
                                                          '2t5aQcFM2s3hvgc5xjT4GWLMNP0FFJ4mQyMtJFCCq8kjpHm7RdkKzuxW6BUzgkAmuST4+DJXQHcHWVedwVQWwBiMpVw3+I' \
                                                          'ombh7arzIpKagcneIeEENHaLzVDeDVYss/cynbKETrxfOJuTZuL5tNR9cc/r8j8t06QPxv+jbTdlZgO10sxhXYefI4H2ba' \
                                                          'foc5JMj92VOwhcORxLitcP1wsyLGXf8BrUSltQcUY68dcyBLkKKFGIwtHFmHoFC51Gipo1l33eadnROix8KqB+YQc+naqb' \
                                                          '4NFJ4rhYpb1G7D8lSqon38rMl73AHP4zeNCIrADdRk3M8qizUUJPnCrUYGqOGmoVWqM51jBpqVlKh9tfGqKHmARVqf22MG' \
                                                          'l5KkKCus1DDy3ER1NSLrmPU8JI8BDV1B0qMGl7Ch6BuUK4yrhrcc4fpDoYn6B4FwNsP8Mla1WzI8Mwahiyz3Jehzq/yfae' \
                                                          '6+NTPs+nTyK/tXRu+YY57qBy9sOctPlRi33xQI4sMqndQzb27IZ4BVE8BJciKzQCq14Auzi02A6geBLpO93nmDGScyYIXc' \
                                                          'uNMVhhxH0NJBMFXPU18/nWS9ajpIFFx8VsOeEJ4tvYv4Zh4xuDi0xVFlhzAzUWzGFfovo/gX27aO9aaHdLTs7ISj2XKVSH' \
                                                          'qAnVF0WaoQvjh5VowfiVUyMl+jwxhGD0eNnsllnFQf/bg4j1vvG/D0Bt4SGNIKIVFk6kxS2hoSxOZdB/Uq7zLSwWIXEK7D' \
                                                          '2PCWWuCd69PPGEDqKIz5BRSoCrNUFJI4QWFGKmaQgov+MNIa+mFWUKpOXtdypxVL/Uw5vxIMQij4hKMAIMO4i/nKUqHQzV' \
                                                          'MMmcrcQA6lGCviMemNbJ8HuSxzf1iIC2Si8KT7w/+WB0q7nA/eGH83sr/v10iKAaPVGCg5iLfb9A0/8/7SAycSNLAd81N3' \
                                                          'lHcRzyyA/HaVMQ7jZhDBiwOFVQYdfF29NSO5ftWGzHllm21W6xFPil1ordzu1XpBfrWhsHQIzdHfdTvP/Ik2fG2KoPDeCp' \
                                                          'Np+M6XasbVFyza7Ura+j18prnuJYX7H3B2vMl8nNGkqI5zoUKDSu5d0wvkC4QhTc2YZ7SLD4iwJ5WwzCIp1XlnF7LjjOHx' \
                                                          'uScVaOZ86cyqsroGBnx/h1rdPFe1TPspFGhTAxrBuL9IfYMil01xH5GsZuP2c9geUhFn5ElDXl5sVhlqOKFmTG4eFme23z' \
                                                          'wdgkHeQ2UE+9rgGg+dmpM3vnFtJlmrGdVvA91pUAaOzAUzmSg2SIWHcRb34J04NzwQLOP50eQvG21bM9qBtxXGfJVByc6h' \
                                                          '8N1fdfxgqjD+7bTEnct84LdtYPrqHPFYmhYFMeeJm7d4A/CPz9H2yaX8aBjk3CFz2Yd9FpJvs06n7LwtV/DLnc9dKRdN3n' \
                                                          'GVeozqsWe0s+gZjHjeREV9J17q9Fq3bg72K0oAzyfY44AY8KG2v5Rjw9IVYYyPyWdC3q+E4ZU5ha6Dph8qDT95EDUT9MPR' \
                                                          'A322pa/bVkcDkVdPIUsA01ICdOg9s/W9YRp9bKZ9vj9hz3L21vq2Uv40ys9e8A2RNUnOXDmag5noPYI1xsJZ7SyObNIOIP' \
                                                          'feB+xu3gjhyXw+sMIS4yEJbRGLKEsuUBbLLwZ8zNs/5Z3NYkWrWHyNsom74mm41lL6IU7UXuDadFywGIX8mYvCJzuEn7jP' \
                                                          'rWfLxyRqNyzhOmgmCW54vMMBenAux8wHaiTEprMp/p6wMILiyfis4Dp0XUyulblnKWZcHTx/WAnN4d3XQxaKXkG5qwZit9' \
                                                          'zwXAhNHj9ruSC8iobN7wGK4JbZuOG125FcCux8R06nbck4/vkXuis9QK7bQd2GJkmn7ib4R/lLAZ4HWaEOWrCHEE3iQTS8' \
                                                          'aHYn8ql2fv+Pd4cOX0+hyPwOukIR2oJR5Syl8sZF227sbwl8s6dKdVwkLO2jzJrd0hm7WY/dM/EmEYG96EmHtFhloT7tH4' \
                                                          'isZFKyzbbztYSfuPO+zs5LIGaVNWSy0Q0rfoq+cC53EarchExKD2R+1jH6vaW0Av3TODph4N5lZ7rPBW1DC3hxiHuM3t/M' \
                                                          'LPSc4UnBhzjvWh/ZTCt0vNtJ4cZxntiv+1SVjXn4jGtZkuIWXp27XHahXXcV8EfD2ZYeqLtfPpiOu7z+0t2PoV7q+ZEXWl' \
                                                          '18b0PjGyDLH6PL2t08Zt8U8e4J5daB0oJ+96Yw5fVczrQlTr3bS3pbDJ74yze2NmAV9bFG2d1Cs14p8DTmedCJINXb8Uka' \
                                                          'xTED684ifEbTBWliE93k7pDVS62UzsuU6g0b4RTweL8PjZGkD2PKm6tBHhxI2a3OsjwX982u1uZzWXlES9FO3hZLky72jj' \
                                                          'tuFRj+NIOXo4I066eQgovdYKRauNc5uKlHZDLFz2rbZm+tYG0s9eJ2lg3CEoA8IpYwKFCCiiGG9VAeomOHxF7PToKmvisv' \
                                                          'M3h9IQbcuMLM6pl7J4qCkX4pqr+/wE5S1lpbTcBAA==',
                                 'cargoTrckingFindButton': 'cargoTrckingFindButton',
                                 'javax.faces.partial.render': 'bookingNumbers billToBookingGrop billofLading_Table3 release_Information_bill release_Information_booking cargoTrackingOrderBillInformation cargoTrackingBookingOfLadingInformation cargoTrackingContainerHistory cargoTrackingContainerInfoStatus cargoTrackingContainerBillOfLadingNumber1 cargoTrackingContainerInfoByContainerNumber release_Information_booking_version release_Information_bill_version actualLoadingInfo containerInfoByBlNum containerInfoByBkgNumTable actualLoadingInfo5 documentStatus cargoTrackingAcivePictures containerNumberAll containerInfo_table3 containerInfo_table4 cargoTrackingPrintByContainer containerNumberAllByBookingNumber registerUserValidate validateCargoTracking isbillOfLadingExist isbookingNumberExist cargoTrackingContainerPictureByContainer cargoTrackingContainerHistory1 cargoTrackingOrderBillMyFocus cargoTrackingBookingMyFocus userId contaienrNoExist billChange4 bookingChange4 bookingChange3 cargoTrackingContainerHistory6 numberType containerSize containerMessage containerTab isLogin cargoTrackingBillContainer cargoTrackingBillContainer1 BillMessage BookingMessage searchSuccess searchError containerTransportationMode',
                                 'javax.faces.partial.execute': '@all', 'isbillOfLadingExist': 'false',
                                 'javax.faces.partial.ajax': 'true', 'isbookingNumberExist': 'false',
                                 'javax.faces.source': 'cargoTrckingFindButton'
                                 }
                    yield Request(url=start_url,
                                  headers={
                                      'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                            'Chrome/64.0.3282.186 Safari/537.36',
                                      'Content-Type': 'application/x-www-form-urlencoded',
                                      'Referer': 'http://elines.coscoshipping.com/NewEBWeb/public/cargoTracking/cargoTracking.xhtml?'
                                                       'CARGO_TRACKING_NUMBER_TYPE=CONTAINER&CARGO_'
                                                       'TRACKING_NUMBER=SESU2187520&REDIRECT=1&uid=',
                                      'Accept': 'application/xml, text/xml, */*; q=0.01',
                                      'Accept-Encoding': 'gzip, deflate',
                                      'Accept-Language': 'en-US,en;q=0.9',
                                      'Connection': 'keep-alive',
                                      'Content-Length': '11282',
                                      'Cookie': 'numberType=CONTAINER; number=SESU2198951; language=en_US; JSESSIONID=00009Eg86qyE-ttFjPu7u_wySmU:1ann3vdlp; Hm_lvt_aba1a55910444a23dbcad68d17658d63=1519929289,1519929428,1519929617,1519948494; Hm_lpvt_aba1a55910444a23dbcad68d17658d63=1519948494; RT=sl=1&ss=1519948488587&tt=5577&obo=0&dm=elines.coscoshipping.com&si=b333e5f3-e7fa-4f92-8138-580a8b9a3c73&bcn=%2F%2F36f11e2c.akstat.io%2F',
                                      'Faces-Request': 'partial/ajax',
                                      'Host': 'elines.coscoshipping.com',
                                      'Origin': 'http://elines.coscoshipping.com',
                                      'X-Requested-With': 'XMLHttpRequest'
                                           },
                                  callback=self.parse_product,
                                  method='POST',
                                  body=urlencode(form_data),
                                  dont_filter=True)
            if 'my.maerskline.com' in start_url:
                for key in keys_MAERSK:
                    yield Request(url=start_url.format(key),
                                  callback=self.parse_product,
                                  dont_filter=True)
            if 'zim.com' in start_url:
                for key in keys_ZIM:
                    yield Request(url=start_url.format(key),
                                  headers={
                                      'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                                    'Chrome/64.0.3282.186 Safari/537.36'
                                  },
                                  callback=self.parse_product,
                                  dont_filter=True)
            if 'yangming.com' in start_url:
                for key in keys_YANG:
                    yield Request(url=start_url.format(key),
                                  callback=self.parse_product,
                                  dont_filter=True)

    def parse_product(self, response):

        prod_item = SiteProductItem()

        prod_item['container_num'] = self._parse_ContainerNumber(response)
        prod_item['container_sizetype'] = self._parse_ContainerSizeType(response)
        prod_item['date'] = self._parse_Date(response)
        prod_item['container_moves'] = self._parse_ContainerMoves(response)
        prod_item['location'] = self._parse_Location(response)
        prod_item['vessel_voyage'] = self._parse_VesselVoyage(response)
        prod_item['vgm'] = self._parse_VGM(response)
        prod_item['weight'] = self._parse_weight(response)
        prod_item['origin'] = self._parse_origin(response)
        prod_item['landing_port'] = self._parse_landing_port(response)
        prod_item['TS_port'] = self._parse_TS_port(response)
        prod_item['discharging_port'] = self._parse_discharging_port(response)
        prod_item['destination'] = self._parse_destination(response)
        prod_item['ServiceTerm'] = self._parse_ServiceTerm(response)

        if any(value for value in prod_item.values()):
            return prod_item

    @staticmethod
    def _parse_ContainerNumber(response):
        try:
            ContainerNumber = response.xpath('//table[@width="95%"][3]/tr[3]/td[1]//text()').extract()
            if ContainerNumber:
                ContainerNumber = str(ContainerNumber[0])
            if not ContainerNumber and response.xpath('//td[@class="bor_L_none"]/a/font/u//text()'):
                ContainerNumber = str(response.xpath('//td[@class="bor_L_none"]/a/font/u//text()')[0].extract())
            if not ContainerNumber and response.xpath('//span[@class="tracking_container_id"]//text()'):
                ContainerNumber = str(response.xpath('//span[@class="tracking_container_id"]//text()')[0].extract())
            if not ContainerNumber and response.xpath('//tr[@class="field_odd"]//text()').extract():
                ContainerNumber = str(response.xpath('//tr[@class="field_odd"]//text()').extract()[3])
            return ContainerNumber if ContainerNumber else None
        except Exception as e:
            print('No Data')

    @staticmethod
    def _parse_ContainerSizeType(response):
        try:
            ContainerSizeType = response.xpath('//table[@width="95%"][3]/tr[3]/td[2]//text()').extract()
            if ContainerSizeType:
                ContainerSizeType = str(ContainerSizeType[0]).strip()
            if not ContainerSizeType and response.xpath('//div[@class="base_table01"]/table/tbody/tr/td/text()').extract():
                ContainerSizeType = str(response.xpath('//div[@class="base_table01"]/table/tbody/tr/td/text()').extract()[18])
            if not ContainerSizeType and response.xpath('//tr[@class="field_odd"]//text()').extract():
                ContainerSizeType = str(response.xpath('//tr[@class="field_odd"]//text()').extract()[6]) \
                                    + '/' + str(response.xpath('//tr[@class="field_odd"]//text()').extract()[9])
            return ContainerSizeType if ContainerSizeType else None
        except Exception as e:
            print('No Data')

    @staticmethod
    def _parse_Date(response):
        try:
            Date = response.xpath('//table[@width="95%"][3]/tr[3]/td[3]//text()').extract()
            if Date:
                Date = str(Date[0]).strip()
            if not Date and response.xpath('//div[@class="base_table01"]/table/tbody/tr/td/text()').extract():
                Date = str(response.xpath('//div[@class="base_table01"]/table/tbody/tr/td/text()').extract()[21])
            if not Date and response.xpath('//span[@class="ETA-block"]//text()').extract():
                Date = str(response.xpath('//span[@class="ETA-block"]//text()').extract()[1].strip())
            if not Date and response.xpath('//tr[@class="field_odd"]//text()').extract():
                Date = str(response.xpath('//tr[@class="field_odd"]//text()').extract()[12])
            return Date if Date else None
        except Exception as e:
            print('No Data')

    @staticmethod
    def _parse_ContainerMoves(response):
        try:
            ContainerMoves = response.xpath('//table[@width="95%"][3]/tr[3]/td[4]//text()').extract()
            if ContainerMoves:
                ContainerMoves = str(ContainerMoves[0]).strip()
            if not ContainerMoves and response.xpath('//div[@class="base_table01"]/table/tbody/tr/td/text()').extract():
                ContainerMoves = str(response.xpath('//div[@class="base_table01"]/table/tbody/tr/td/text()').extract()[22])
            if not ContainerMoves and response.xpath('//tr[@class="field_odd"]//text()').extract():
                ContainerMoves = str(response.xpath('//tr[@class="field_odd"]//text()').extract()[15])
            return ContainerMoves if ContainerMoves else None
        except Exception as e:
            print('No Data')

    @staticmethod
    def _parse_Location(response):
        try:
            Location = response.xpath('//table[@width="95%"][3]/tr[3]/td[5]//text()').extract()
            if Location:
                Location = str(Location[0]).strip()
            if not Location and response.xpath('//div[@class="base_table01"]/table/tbody/tr/td/text()').extract():
                Location = str(response.xpath('//div[@class="base_table01"]/table/tbody/tr/td/text()').extract()[2])
            if not Location and response.xpath('//tr[@class="field_odd"]//text()').extract():
                Location = str(response.xpath('//tr[@class="field_odd"]//text()').extract()[20])
            return Location if Location else None
        except Exception as e:
            print('No Data')

    @staticmethod
    def _parse_VesselVoyage(response):
        try:
            VesselVoyage = response.xpath('//table[@width="95%"][3]/tr[3]/td[6]//text()').extract()
            if VesselVoyage:
                VesselVoyage = str(VesselVoyage[0]).strip()
            if not VesselVoyage and response.xpath('//div[@class="base_table01"]/table/tbody/tr/td/text()').extract():
                VesselVoyage = str(response.xpath('//div[@class="base_table01"]/table/tbody/tr/td/text()').extract()[57])
            if not VesselVoyage and response.xpath('//span[@class="ETA-block"]//text()').extract():
                VesselVoyage = str(response.xpath('//span[@class="ETA-block"]//text()').extract()[0].strip())
            return VesselVoyage if VesselVoyage else None
        except Exception as e:
            print('No Data')

    @staticmethod
    def _parse_VGM(response):
        try:
            VGM = response.xpath('//table[@width="95%"][3]/tr[3]/td[8]//text()').extract()
            return str(VGM[0]).strip() if VGM else None
        except Exception as e:
            print('No Data')

    @staticmethod
    def _parse_weight(response):
        try:
            weight = str(response.xpath('//div[@class="base_table01"]/table/tbody/tr/td/text()').extract()[19])
            return weight if weight else None
        except Exception as e:
            print('No Data')

    @staticmethod
    def _parse_origin(response):
        try:
            origin = str(response.xpath('//div[@class="base_table01"]/table/tbody/tr/td/text()').extract()[1])
            return origin if origin else None
        except Exception as e:
            print('No Data')

    @staticmethod
    def _parse_landing_port(response):
        try:
            if response.xpath('//div[@class="base_table01"]/table/tbody/tr/td/text()').extract():
                landing_port = str(response.xpath('//div[@class="base_table01"]/table/tbody/tr/td/text()').extract()[2])
            if not landing_port and response.xpath('//tr[@class="container-row"]/td//text()').extract():
                landing_port = str(response.xpath('//tr[@class="container-row"]/td//text()').extract()[16])
            return landing_port if landing_port else None
        except Exception as e:
            print('No Data')

    @staticmethod
    def _parse_TS_port(response):
        try:
            ts_port = str(response.xpath('//div[@class="base_table01"]/table/tbody/tr/td/text()').extract()[3])
            return ts_port if ts_port else None
        except Exception as e:
            print('No Data')

    @staticmethod
    def _parse_discharging_port(response):
        try:
            charging_port = str(response.xpath('//div[@class="base_table01"]/table/tbody/tr/td/text()').extract()[4])
            return charging_port if charging_port else None
        except Exception as e:
            print('No Data')

    @staticmethod
    def _parse_destination(response):
        try:
            destination = str(response.xpath('//div[@class="base_table01"]/table/tbody/tr/td/text()').extract()[5])
            return destination if destination else None
        except Exception as e:
            print('No Data')

    @staticmethod
    def _parse_ServiceTerm(response):
        try:
            ServiceTerm = str(response.xpath('//div[@class="base_table01"]/table/tbody/tr/td/text()').extract()[20])
            return ServiceTerm.strip() if ServiceTerm else None
        except Exception as e:
            print('No Data')