from odoo import fields, models, api, _
from datetime import date, datetime
from dateutil.relativedelta import relativedelta

from odoo.exceptions import ValidationError


class School(models.Model):
    _name = 'school.info'
    _description = 'Class Information'
    _order = 'id'
    # _rec_name = 'name'
    _inherit = 'mail.thread'


    STATES = [
        ('allowed_to_book','Allowed To Book'),
        ('closed_for_fixing', 'Closed For Fixing'),
        ('booked','Booked'),
        ('prepaired_for_party','Prepaired for Party'),
    ] 
    MILITARY = [
        ('c','Completed'),
        ('n','No'),
        ('p','Process'),
    ]
# Monetary
# Monetary

    code = fields.Char(string='ID', index=True, required=True, readonly=True, default='#New')
    name = fields.Char('Subject Name', required=True)
    date_of_birth = fields.Date()
    age = fields.Char(compute='_calculate_age')
    image = fields.Binary('Cover')
    image_1500 = fields.Image("Image 1500", max_width=1500, max_height=1500)
    currency_id = fields.Many2one('res.currency', string='Currency')
    salary = fields.Monetary(currency_field= 'currency_id')
    state = fields.selection(STATES, default='allowed_to_book')

    gender = fields.Selection([('m','Male'), ('f', 'Female')])
    military = fields.selection(MILITARY, compute='')
    email = fields.Char('Email', required=True)
    test = fields.Char(
    readonly=True 
    )

    _sql_constraints = [
        ("unique_name", "UNIQUE(name)", "Error Username Must be Unique")
    ]
#   
#      

    @api.constrains('email')
    def validate_email(self):
        for rec in self:
            if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", obj.email) == None:
                raise ValidationError("Please Provide Valid Email Address: %s" % obj.email)
        return True
 

    def name_get(self):
        r = []
        for rec in self:
            rec_name = f'{name} and {salary}'
            r.append(rec_name)
            # r.append((rec.id, rec_name))
            return r




    @api.onchange('email', 'gender')
    def change_data(self):
        if email == 'k@gmail.com' and gender == 'm':
            test = 'DONE'
        else:
            msg = f'Email Not = {email}'
            raise ValidationError(msg)




    @api.depends('date_of_birth')
    def _calculate_age(self):
        for rec in self:
            if rec.date_of_birth:
                d1 = rec.date_of_birth
                d2 = datetime.today().date()
                r = relativedelta(d2, d1)
                rec.age = str(r.years) + "y" + " " + \
                    str(rd.months) + "m" + " " + str(rd.days) + "d"
            else:
                rec.age = 'No Date Of Birth!'


    @api.model
    def create(self, v):
        if v.get('code', '#New') == '#New':
            v['code'] = self.env['ir.sequence'].next_by_code('school.info') or '#New'
        r = super(School, self).create(v)
        return r

# Buttons

    @api.model
    def allowed_transition_states(self, old_state, new_state):
        allowed = [
            ('allowed_to_book','booked'),
            ('booked','prepaired_for_party'),
            ('prepaired_for_party','closed_for_fixing'),
            ('closed_for_fixing','allowed_to_book'),
        ]
        return (old_state, new_state) in allowed

    def change_states(self, new_state):
        for rec in self:
            if allowed_transition_states(rec.state, rec.new_state):
                rec.state = new_state
            else:
                msg = f'Sorry Con\'t Allowed To Trasition {rec.state} To {new_state}'
                raise ValidationError(msg)
    
    def make_booked(self):
        self.change_states('booked')

    def make_prepaired_for_party(self):
        self.change_states('prepaired_for_party')
    
    def make_closed_for_fixing(self):
        self.change_states('closed_for_fixing')
    
    def make_allowed_to_book(self):
        self.change_states('allowed_to_book')
    


