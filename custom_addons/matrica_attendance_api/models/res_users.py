import secrets
from odoo import models, fields, api

class ResUsers(models.Model):
    _inherit = 'res.users'

    api_key = fields.Char(
        string="API Key", 
        size=64, 
        copy=False, 
        groups="base.group_system",
    )

    def action_generate_api_key(self):
        for user in self:
            new_key = secrets.token_hex(32)
            user.api_key = new_key