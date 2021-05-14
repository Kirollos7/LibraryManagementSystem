from odoo import api, models, fields

class StudentInformationData(models.Model):
    _name = 'stu.data'
    _inherit = 'address'

    name = fields.Char()
    age = fields.Char()
    email = fields.Char()
    phone = fields.Char()
