# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Address(models.Model):

    _name = 'address'
    _description = 'Student Address'

    street = fields.Char()
    street2 = fields.Char()
    area = fields.Char()
    city = fields.Char()
    country = fields.Char()
