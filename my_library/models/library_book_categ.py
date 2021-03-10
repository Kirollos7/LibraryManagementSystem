
from odoo import models, fields, api 
from odoo.exceptions import ValidationError 

class BookCategory(models.Model):
    _name = 'library.book.category'
    _description = 'Library Book Category'
    _parent_store = True
    _parent_name = "parent_id"
    # _order = ''
    # _rec_name = ''    
    
    name = fields.Char(required=True, string = 'Category')
    parent_id = fields.Many2one('library.book.category', string='Parent Category', ondelete='restrict', index=True, )
    child_ids = fields.One2many('library.book.category', 'parent_id' , string = 'Child Categories')
    parent_path = fields.Char(index=True)
    
    @api.constrains('parent_id')     
    def _check_hierarchy(self): 
        if not self._check_recursion(): 
            raise models.ValidationError('Error! You cannot create recursive categories.') 
        
        
        
        
        
        
        
        
        
        
        # Database Hierarchy Model 
# There's more...
# The technique shown here should be used for static hierarchies, which are read and
# queried often but are updated less frequently. Book categories are a good example, since
# the library will not be continuously creating new categories; however, readers will often
# be restricting their searches to a category and its child categories. The reason for this lies
# in the implementation of the nested set model in the database, which requires an update
# of the parent_path column (and the related database indexes) for all records whenever
# a category is inserted, removed, or moved. This can be a very expensive operation,
# especially when multiple editions are being performed in parallel transactions.
# If you are dealing with a very dynamic hierarchical structure, the standard parent_id
# and child_ids relations will often result in better performance by avoiding table-level
# locks.








# Odoo supports two different types of constraints:
# • The ones checked at the database level
# • The ones checked at the server level