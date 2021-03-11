from odoo import api, fields, models    
    
    
    
class ResPartner(models.Model):
    _inherit='res.partner'
    _order = 'name'
    _name = 'res.partner'
    _description = 'Authors'
    
    
    published_book_ids = fields.One2many('library.book', 'publisher_id', string = 'Published Books')
    authored_book_ids = fields.Many2many('library.book' , string = 'Authored Books')
    count_books = fields.Integer('Authored Books', compute='_compute_count_books')
    
    @api.depends('authored_book_ids')
    def _compute_count_books(self):
        for record in self:
            number = len(record.authored_book_ids)
            record.count_books  = number
        
        
    # relation='library_book_res_partner_rel' # 
    
    