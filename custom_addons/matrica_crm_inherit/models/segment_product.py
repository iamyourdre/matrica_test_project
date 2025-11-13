from odoo import models, fields

class SegmentProduct(models.Model):
    _name = 'segment.product'
    _description = 'Master Segment Product'

    name = fields.Char(string='Nama Segment', required=True)
    active = fields.Boolean(default=True)