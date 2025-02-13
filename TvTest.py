import sys
import logging

from samsungtvws import SamsungTVWS

TV_IP = "192.168.1.225"
tv = SamsungTVWS(host=TV_IP)
#tv.art().set_artmode(matte='modern_polar')
tv.art().set_photo_filter('vivid')