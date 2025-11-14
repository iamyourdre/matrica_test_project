{
    'name': 'Matrica Attendance API',
    'version': '1.0',
    'summary': 'Module test absensi via API.',
    'author': 'Adrian Sutansaty',
    'depends': [
        'base',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/attendance_record_views.xml',
        'views/res_users_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}