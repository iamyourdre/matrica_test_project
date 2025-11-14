from odoo import models, fields

class AttendanceRecord(models.Model):
    _name = 'attendance.record'
    _description = 'Attendance Record'
    _order = 'date desc'

    name = fields.Char(
        string="Nama", 
        required=True
    )
    date = fields.Datetime(
        string="Tanggal", 
        default=fields.Datetime.now, 
        required=True
    )
    attendance_type = fields.Selection(
        [('check_in', 'Check In'), 
         ('check_out', 'Check Out')],
        string="Tipe", 
        required=True
    )
    longitude = fields.Float(
        string="Longitude", 
        digits=(10, 7)
    )
    latitude = fields.Float(
        string="Latitude", 
        digits=(10, 7)
    )