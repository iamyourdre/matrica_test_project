{
    'name': 'Matrica CRM Inherit',
    'version': '1.0',
    'summary': 'Module test untuk inherit CRM',
    'author': 'Matrica Test',
    'depends': [
        'base',
        'crm',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/segment_product_views.xml',
        'views/crm_lead_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}