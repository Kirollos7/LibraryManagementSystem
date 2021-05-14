from odoo import api, fields, models

class SalesInherit(models.Model):
    _name = 'sales.inherit'
    _description = 'Sales Inherit'
    _inherit = ['', 'mail.thread']
