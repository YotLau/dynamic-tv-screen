from flask import jsonify
import sys
import os
import json
import logging
from samsungtvws import SamsungTVWS

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def check_tv_connection(tv_ip):
    try:
        logger.debug(f"Checking TV connection for IP: {tv_ip}")
        tv = SamsungTVWS(host=tv_ip)
        tv_state = tv.__getstate__()
        logger.debug(f"TV state: {tv_state}")
        host_matches = tv_state.get('host') == tv_ip
        logger.debug(f"Host matches: {host_matches}")
        return jsonify({
            'success': host_matches,
            'message': 'TV connection successful' if host_matches else 'TV connection failed'
        })
    except Exception as e:
        logger.error(f"TV connection error: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
