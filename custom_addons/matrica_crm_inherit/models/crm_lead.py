from odoo import models, fields

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    x_pelanggan_baru = fields.Boolean(string='Pelanggan Baru')

    x_segment_pelanggan = fields.Selection([
        ('konstruksi', 'Konstruksi'),
        ('perbankan', 'Perbankan'),
        ('pemerintah', 'Pemerintah'),
        ('bumn', 'BUMD/BUMN'),
        ('kementrian', 'Kementrian'),
        ('swasta', 'Swasta Lainnya')
    ], string='Segment Pelanggan')

    x_segment_pelanggan_lainnya = fields.Char(string='Segment Pelanggan Lainnya')

    x_segment_product_id = fields.Many2one(
        'segment.product', 
        string='Segment Product'
    )

    x_task_progress_ids = fields.One2many(
        'task.progress', 
        'lead_id', 
        string='Task Progress'
    )