from odoo import api, fields, models
from odoo.exceptions import ValidationError
from datetime import timedelta, timezone , time



class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Library Book' 
    _rec_name = 'short_name'
    _order = 'date_release desc, name'
    # _log_access=False
    _inherit = ['base.archive'] 


# The automatic creation of these log fields can be disabled by setting the _log_access=False model attribute.
    
    STATE = [
        ('draft' , 'Not Available'),
        ('available' , 'Available'),
        ('lost' , 'Lost'),
    ]
    name = fields.Char('Title' , required=True, )
    short_name = fields.Char('Short Title', translate=True, index=True, )
    notes = fields.Char('Internal Notes')
    state = fields.Selection(STATE , string='State', default='draft')
    description = fields.Html('Description', sanitize=True, strip_style=False)
    cover = fields.Binary('Book Cover')
    out_of_print = fields.Boolean('Out of Print?')
    date_updated = fields.Datetime('Last Updated')
    pages = fields.Integer('Number of Pages', groups='base.group_user', states={'lost': [('readonly', True)]}, help="Total book page count", company_dependent=False)
    reader_rating = fields.Float('Reader Average Rating', digits=(14, 4), )
    date_release = fields.Date('Release Date' , required=True, )
    author_ids = fields.Many2many('res.partner', string = 'Authors' , ) 
    active = fields.Boolean('Active', default=True) 
    publisher_id = fields.Many2one('res.partner', string='Publisher', ondelete='set null', domain=[], context={}, )
    publisher_city = fields.Char('Publisher City', related='publisher_id.city', readonly=True)
    # 
    # 
    currency_id = fields.Many2one('res.currency', string='Currency')
    retail_price = fields.Monetary('Retail Price', currency_field='currency_id', )
    cost_price = fields.Monetary('Book Cost', )
    
    category_id = fields.Many2one('library.book.category', string='Category')
    
    age_days = fields.Float(string='Days Since Release', compute='_compute_age', store=False, compute_sudo=True, search='_search_age', inverse='_inverse_age', )
    
    
    @api.depends('date_release')
    def _compute_age(self):
        today = fields.Date.today()
        for book in self:
            if book.date_release:
                # book.age_days = (today - book.date_release).days
                delta = today - book.date_release
                book.age_days = delta.days
            else:
                book.age_days = 0 
                
    
    def _inverse_age(self):
        today = fields.Date.today()            
        for book in self.filtered('date_release'):
            d = today - timedelta(days=book.age_days)
            book.date_release = d
            
    def _search_age(self, operator, value):
        today = fields.Date.today()
        value_days = timedelta(days=value)
        value_date = today - value_days
        operator_map = {
            '>': '<', '>=': '<=', '<': '>', '<=': '>=',
        }    
        new_op = operator_map.ge(operator, operator)
        return [('date_release' , new_op , value_date)]
    
         
    
    def name_get(self):
        result = []
        for record in self:
            rec_name = "%s (%s)" % (record.name, record.date_release)
            result.append((record.id, rec_name))
        return result
    
    
    _sql_constraints = [
                        ('name_uniq', 'UNIQUE (name)', 'Book title must be unique.'), 
                        ('positive_page', 'CHECK(pages>0)', 'No of pages must be positive'),
                        ]
    
    @api.constrains('date_release')
    def _check_release_date(self):
        for record in self:
            if record.date_release  > fields.Date.today():
                raise models.ValidationError('Release Date must be in the past.')  
    
    
    @api.model
    def _referencable_models(self):
        models = self.env['ir.model'].search([
        ('field_id.name', '=', 'message_ids')])
        return [(x.model, x.name) for x in models]
    
    ref_doc_id = fields.Reference(selection = '_referencable_models', string='Reference Document', )
    
    
    
    
    
    
    
    
    
    
    
class ResPartner(models.Model):
    _inherit='res.partner'
    _order = 'name'
    _name = 'res.partner'
    
    
    published_book_ids = fields.One2many('library.book', 'publisher_id', string = 'Published Books')
    authored_book_ids = fields.Many2many('library.book' , string = 'Authored Books')
    count_books = fields.Integer('Number of Authored Books', compute='_compute_count_books')
    
    @api.depends('authored_book_ids')
    def _compute_count_books(self):
        for record in self:
            number = len(record.authored_book_ids)
            record.count_books  = number
        
        
    # relation='library_book_res_partner_rel' # 
    
    
    
    
    
    
class BaseArchive(models.AbstractModel):
    _name = 'base.archive'
    
    active = fields.Boolean(default=True)
    
    def do_archive(self):
        for record in self:
            record.active = not record.active 
    
    
    
    
    
#   _sql_constraints = [
#  ( 'check_credit_debit',
#  'CHECK(credit + debit>=0 AND credit * debit=0)',
#  'Wrong credit or debit value in accounting entry!'
#  )
#  ]
    
    # authors
    
    
    # def name_get(self):
    #     result = []
    #     for record in self:
    #         rec_name = f"{record.name} ({record.date_release})"
    #         result.append(record.id , record.rec_name)
    #     return result
    
    
    # Date Time Field -->  fields.Date.now() 
    # Date Field -->       fields.Date.today() 
    
    # Monetary: can store an amount in a certain currency. This will also be explained in
        # the Adding a monetary field recipe in this chapter
        
        # groups: makes the field available only to some security groups. It is a string
        # containing a comma-separated list of XML IDs for security groups. This is
        # addressed in more detail in Chapter 10, Security Access.
                    
        
    # default: is the default value. It can also be a function that is used to calculate the
    # default value; for example, default=_compute_default, where _compute_
    # default is a method that was defined on the model before the field definition.
    
    # states: allows the user interface to dynamically set the value for the readonly,
    # required, and invisible attributes, depending on the value of the state field.
    # Therefore, it requires a state field to exist and be used in the form view (even if it
    # is invisible). The name of the state attribute is hardcoded in Odoo and cannot be
    # changed.
    
    # copy: flags whether the field value is copied when the record is duplicated. By
    # default, it is True for non-relational and Many2one fields, and False for
    # One2many and computed fields.
        
    # index: when set to True, creates a database index for the field, which sometimes
    # allows for faster searches. It replaces the deprecated select=1 attribute.
    
        
    # The company_dependent flag makes the field store different values for each
    # company. It replaces the deprecated Property field type.
    
    # • The sanitize flag is used by HTML fields and strips its content from potentially
    # insecure tags. Using this performs a global cleanup of the input. 
    
    
    #  group_operator is an aggregate function used to display results in the group
    # by mode. Possible values for this attribute include count, count_distinct,
    # array_agg, bool_and, bool_or, max, min, avg, and sum. Integer, float, and
    # monetary field types have the default value sum for this attribute.
    
    
    
    
    
    
    #  If you need finer control in HTML sanitization, there are a few more attributes that you
    # can use, which only work if sanitize is enabled:
    # • sanitize_tags=True, to remove tags that are not part of a whitelist (this is the
    # default)
    # • sanitize_attributes=True, to remove attributes of the tags that are not part
    # of a whitelist
    # • sanitize_style=True, to remove style properties that are not part of
    # a whitelist
    # strip_style=True, to remove all style elements
    # • strip_class=True, to remove the class attributes
    
    
    
    
    # relational m2o m2m o2m
    
    # • context: adds variables to the client context when clicking through the field to
    # the related record's view. We can, for example, use it to set default values for new
    # records that are created through that view.
    # • domain: is a search filter that's used to limit the list of related records that are
    # available.
    
    # However, we can override this using the relation attribute. in Many2many Relation
    
    
    
    # Many2many
    # One is the case where we need more than one Many2many relations between
    # the same two models. For this to be possible, we must provide ourselves with the
    # relation table name for the second relation, which must be different from the
    # first relation.
    # • The other case is when the database names of the related tables are long enough for
    # the automatically generated relation name to exceed the 63-character PostgreSQL
    # limit for database object names.
    # The relation table's automatic name is <model1>_<model2>_rel. However, this
    # relation table also creates an index for its primary key with the following identifier:
    # <model1>_<model2>_rel_<model1>_id_<model2>_id_key
    # This primary key also needs to meet the 63-character limit. So, if the two table names
    # combined exceed a total of 63 characters, you will probably have trouble meeting the
    # limits and will need to manually set the relation attribute.
        
        