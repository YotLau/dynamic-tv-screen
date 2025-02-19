import sys
import logging

from samsungtvws import SamsungTVWS

TV_IP = "192.168.1.225"
tv = SamsungTVWS(host=TV_IP)
print(tv.art().get_api_version())#tv.art().set_artmode(matte='modern_polar')
