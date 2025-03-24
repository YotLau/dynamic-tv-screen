from flask import Blueprint, request
from .check_tv import check_tv_connection

api = Blueprint('api', __name__)

# ...existing routes...

@api.route('/check-tv-ip', methods=['POST'])
def check_tv_ip():
    data = request.get_json()
    tv_ip = data.get('tvIp')
    if not tv_ip:
        return jsonify({'success': False, 'error': 'TV IP is required'}), 400
    return check_tv_connection(tv_ip)
