from odoo import fields, models, api

class LibraryMember(models.Model):
    _name = 'library.member'
    _inherits = {'res.partner' : 'partner_id'}
    _description = 'Library Members'
    
    partner_id = fields.Many2one('res.partner', required=True, ondelete='cascade')
    # 
    date_start = fields.Date('Member Since')
    date_end = fields.Date('Termination Date')
    member_number = fields.Char()
    date_of_birth = fields.Date('Date of birth')
    

    
    def log_all_library_members(self):
        library_member_model = self.env['library.member']
        all_member = library_member_model.search([])
        print("All Members: ", all_member)
        return True
    
        
    