from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class Lawyers(models.Model):
    _name = "lawyers"
    _description = "LAWYERS"
    _rec_name="name"

    name = fields.Char(string='Name', required=True)  # جعل الحقل مطلوبًا
    image=fields.Image(string="Image")
    patients_id=fields.Many2many("hospital.patients",string='Patient many choices')
    customers_id = fields.Many2one(
        'hospital.patients',  # تحديد الموديل المرتبط
        string='Patient'
    )
    gender = fields.Selection(related='customers_id.gender')
    age = fields.Integer(string="Age", default=1)
    refs = fields.Char(string="Reference")

    state=fields.Selection([('draft','Draft '),('in_consultaion','In Consultaion'),('done','Done'),('cancel','Cancel')],string="State",default="draft" ,required=True)

    sql_constraints=[
    ('unique_tag_name', 'unique(name)', 'Name must be unique'),
    ('check_age', 'check(age > 0)', 'Age must be greater than zero')
]

    @api.constrains('name')
    def _check_unique_name(self):
        for record in self:
            # البحث عن أي سجل آخر بنفس الاسم
            existing = self.env['lawyers'].search([
                ('name', '=', record.name),
                ('id', '!=', record.id)  # تجاهل السجل الحالي
            ])
            if existing:
                raise ValidationError(_("The name '%s' already exists. Please choose a different name.") % record.name)
    @api.constrains('age')
    def _check_age(self):
        for record in self:
            if record.age <= 0:
                raise ValidationError(_("Age must be greater than zero"))

# لاحظ الفرق بين onchange , _compute_ في هذا المودل والمودل الاخر 
    @api.onchange('customers_id')
    def onchange_customers_id(self):
        if self.customers_id:
            self.refs = self.customers_id.refs
            self.name="fffffffffffffffffffffffffff"
        else:
            self.refs = False

   

    def action_in_consultaion(self):
        for rec in self:
            rec.state="in_consultaion"
    def action_done(self):
        for rec in self:
            rec.state="done"
    def action_cancel(self):
        action=self.env.ref("ashrofaaa.action_cancel_in_wizard").read()[0]
                                                                        
        return action
                   
    def action_draft(self):
        for rec in self:
            rec.state="draft"           

    def unlink(self):
        if self.state=='done':
            raise ValidationError(_("بلاش يا اشرف تحذف حاجة معمولة دن"))
        super(Lawyers,self).unlink()