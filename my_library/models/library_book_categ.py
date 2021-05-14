
from odoo import models, fields, api 
from odoo.exceptions import ValidationError 
from odoo.exceptions import UserError
class BookCategory(models.Model):
    _name = 'library.book.category'
    _description = 'Library Book Category'
    # _parent_store = True
    # _parent_name = "parent_id"
    _order = 'name'
    
    # _rec_name = 'title'    
    CHOICE = [
      ('a','Apple'),
      ('b','Bin'),  
      ('c','Car'),  
      ('d','Delete'),  
      ('e','Enter'),  
      ('f','Format'),  
        
    ]
    
    name = fields.Char(required=True, string = 'Category')
    description = fields.Text('Description')
    parent_id = fields.Many2one('library.book.category', string='Parent Category', ondelete='restrict', index=True, ) 
    child_ids = fields.One2many('library.book.category', 'parent_id' , string = 'Child Categories')
    
    title = fields.Char()
    date = fields.Date()
    choice = fields.Selection(CHOICE, default = 'a')
  
    
    
    currency_id = fields.Many2one('res.currency', string='Choice Currency')
    price = fields.Monetary('Price', currency_field='currency_id' )
    
  
    @api.model 
    def translation(self, old_state, new_state):
        state=[
          ('a','b'),
          ('b','c'),
          ('c','d'),
          ('d','e'),
          ('e','f'),
        ]
        return (old_state, new_state) in state
    
  
    def change_state(self, new_place):
        for i in self:
            if i.translation(i.state, i.new_state):
                i.state = new_place
            else:
                msg = f'please moving from {i.state} to {new_place}'
                raise UserError(msg)
              
              
    def make_b(self):
        self.change_state('b')
    def make_c(self):
        self.change_state('c')
    def make_d(self):
        self.change_state('d')
    def make_e(self):
        self.change_state('e')
    def make_f(self):
        self.change_state('f')
        
                
                 
    k = fields.Many2one('res.currency', 'CURRENCY')
    cost = fields.Monetary(currency_field='k')
    
    @api.constrains('date')
    def check_date(self):
        today = fields.Date.today()
        for record in self:
            if record.date >  today :
                msg = f'Invalid Date {record.date}. Please Check the Date'
                raise UserError(msg)
  
    _sql_constraints = [('unique_name', 'UNIQUE(name)' , 'Please Check Name Must be Unique')]
    
    
   
    
    
    
    
    
    
    
    
    
    
    def create_categories(self):
        categ1 = {'name': 'Child category 1',
                  'description': 'Description for child 1'
                }
        categ2 = {'name': 'Child category 2',
                  'description': 'Description for child 2'
                }
        parent_category_val = {'name': 'Parent category',
                               'description': 'Description for parent category',
                               'child_ids': [(0, 0, categ1),(0, 0, categ2),]
                                }
        
        # record =  self.env['library.book.category'].create(parent_category_val) 
    
        multiple_records = self.env['library.book.category'].create([categ1, categ2]) 
    
    
    def name_get(self):
        l = []
        for record in self:
            rec_name = f'{record.title} Date {record.date} (name {record.name})'
            l.append((record.id, rec_name))
        return l 
    
  
  
    # def create_categories(self):
    #     categ1 = {
    #             'name': 'Child category 1',
    #             'description': 'Description for child 1'
    #             }
    #     categ2 = {
    #             'name': 'Child category 2',
    #             'description': 'Description for child 2'
    #             }
                                

    # parent_path = fields.Char(index=True)
    # @api.constrains('parent_id')     
    # def _check_hierarchy(self): 
    #     if not self._check_recursion(): 
    #         raise models.ValidationError('Error! You cannot create recursive categories.') 
        
       
        
        
        
        
        
        
        
        
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