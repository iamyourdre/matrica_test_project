import json
import logging
from odoo import http
from odoo.http import request, Response

_logger = logging.getLogger(__name__)

class AttendanceApiController(http.Controller):

  def _json_response(self, status_code, message, data=None):
    response_data = {
      "status": status_code,
      "message": message
    }
    if data is not None:
      response_data["data"] = data
    
    return Response(
      json.dumps(response_data),
      status=status_code,
      mimetype='application/json'
    )

  def _check_api_key(self):
    api_key = request.httprequest.headers.get('X-API-Key')
    
    valid_api_key = request.env['ir.config_parameter'].sudo().get_param('matrica_attendance_api.api_key')
    
    if not api_key or not valid_api_key or api_key != valid_api_key:
      return False
    return True

  def _get_user_from_api_key(self):
    api_key = request.httprequest.headers.get('X-API-Key')
    if not api_key:
      return None
    
    user = request.env['res.users'].sudo().search(
      [('api_key', '=', api_key)], 
      limit=1
    )
    
    return user if user else None

  @http.route('/api/attendance', type='http', auth='public', methods=['GET'], csrf=False)
  def get_attendance_records(self, start_date=None, end_date=None, **kwargs):
    """
    HEADER: 'X-API-Key'.
    QUERY PARAMS:
    - start_date (string: 'YYYY-MM-DD HH:MM:SS')
    - end_date (string: 'YYYY-MM-DD HH:MM:SS')
    """
    
    api_user = self._get_user_from_api_key()
    if not api_user:
      return self._json_response(401, "Unauthorized: Invalid or missing API Key")

    try:
      domain = []
      if start_date:
        domain.append(('date', '>=', start_date))
      if end_date:
        domain.append(('date', '<=', end_date))
      
      records = request.env['attendance.record'].sudo().search(domain)
      
      data_list = []
      for rec in records:
        data_list.append({
          "nama": rec.name,
          "tanggal": rec.date.strftime('%Y-%m-%d %H:%M:%S'),
          "tipe": rec.attendance_type,
          "longitude": rec.longitude,
          "latitude": rec.latitude
        })
      
      return self._json_response(200, "Success", data_list)

    except Exception as e:
      _logger.error(f"Error GET /api/attendance: {e}")
      return self._json_response(500, f"Internal Server Error: {e}")

  @http.route('/api/attendance', type='http', auth='public', methods=['POST'], csrf=False)
  def create_attendance_record(self, **kwargs):
    """
    HEADER: 'X-API-Key'.
    BODY (json):
    {
      "nama": "Nama",
      "tanggal": "YYYY-MM-DD HH:MM:SS",
      "tipe": "check_in" atau "check_out",
      "longitude": 106.8272,
      "latitude": -6.1754
    }
    """
    
    api_user = self._get_user_from_api_key()
    if not api_user:
      return self._json_response(401, "Unauthorized: Invalid or missing API Key")

    try:
      data = json.loads(request.httprequest.data)       
      required_fields = ['nama', 'tanggal', 'tipe']
      if not all(field in data for field in required_fields):
        return self._json_response(400, "Bad Request: Missing required fields")
        
      if data.get('tipe') not in ['check_in', 'check_out']:
        return self._json_response(400, "Bad Request: 'tipe' must be 'check_in' or 'check_out'")

      record = request.env['attendance.record'].with_user(api_user).create({
        'name': data.get('nama'),
        'date': data.get('tanggal'),
        'attendance_type': data.get('tipe'),
        'longitude': data.get('longitude'),
        'latitude': data.get('latitude'),
      })
      
      if record:
        return self._json_response(200, "Success")
      else:
        return self._json_response(500, "Failed to create record")

    except json.JSONDecodeError:
      return self._json_response(400, "Bad Request: Invalid JSON format")
    except Exception as e:
      _logger.error(f"Error POST /api/attendance: {e}")
      return self._json_response(500, f"Internal Server Error: {e}")