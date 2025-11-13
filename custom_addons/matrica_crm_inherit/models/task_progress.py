from odoo import models, fields

class TaskProgress(models.Model):
    _name = 'task.progress'
    _description = 'Task Progress'
    _order = 'sequence'

    lead_id = fields.Many2one('crm.lead', string='Opportunity', ondelete='cascade')

    name = fields.Char(string='Task', required=True)
    deadline = fields.Date(string='Deadline')
    status = fields.Selection([
        ('todo', 'To do'),
        ('progress', 'Progress'),
        ('done', 'Done')
    ], string='Status', default='todo', required=True)
    
    sequence = fields.Integer(default=10)