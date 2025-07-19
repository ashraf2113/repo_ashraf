from datetime import date
from odoo import api, fields, models

class HospitalPatients(models.Model):
    _name = "hospital.patients"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Hospital Patients"
    _rec_name="name"

    doctor_id=fields.Many2one("res.users" ,string="Doctor" ,tracking=True)
    color=fields.Integer("Color")
    color_2=fields.Char("Color_2")
    active = fields.Boolean(string="Active", default="True")
    name = fields.Char(string="Name",tracking=True)
    
    image=fields.Image(string="Image")
    age=fields.Integer(string="Age",compute="_compute_age",tracking=True)
    gender=fields.Selection([('male','Male'),('female','Female')],string="Gender",tracking=True)
    
    refs = fields.Char(string="Reference",tracking=True)
    date_of_birth=fields.Date(string="Date Of Birth",help="زر التاريخ يا اشرف")
    periority=fields.Selection([('0','low'),('1','high'),('2','very high')],string="periority")
    state=fields.Selection([('draft','Draft '),('in_consultaion','In Consultaion'),('done','Done'),('cancel','Cancel')],string="State",default="draft" ,required=True)
    # لاحظ الفرق بين onchange , _compute_ في هذا المودل والمودل الاخر 
    api.depends("date_of_birth")
    def _compute_age(self):
        for rec in self:
            today=date.today()
            if rec.date_of_birth:
                rec.age=today.year-rec.date_of_birth.year
            else:
                rec.age=1

    def action_in_consultaion(self):
        if self.state == 'draft':
            self.state='in_consultaion'


    def action_done(self):
        if self.state == 'in_consultaion':
            self.state='done'
    
    def action_cancel(self):
        # if self.state == 'done':
        self.state='cancel'

    def test_rainbow(self):
        print("rainbowwwwwwwwwwwwwwwwwwwwwwww")
        return{
        'effect':{
           
                'fadeout':'slow',
                'message':'خللي بالك يا حاج دي علامة مش كويسة ',
                'type':'rainbow_man',
            
        }
        }
    @api.model
    def create(self,vals):
        print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",self.env['ir.sequence'])
        print("bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",vals)
        print("cccccccccccccccccccccccccccccccccccccccccccc",vals)
        vals["refs"]=self.env['ir.sequence'].next_by_code('hospital.patients')
        return super(HospitalPatients,self).create(vals)
    
    def write(self,vals):
        print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
        print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",vals)
        return super(HospitalPatients,self).write(vals)
    
    def name_get(self):
        pations_list=[]
        for rec in self:
            name = str(rec.refs or '') + str(rec.name or '')
            pations_list.append((rec.id,name))   
        return pations_list