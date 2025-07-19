from datetime import date
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
from datetime import timedelta


class Property(models.Model):
    _name = "property"
    # _log_access=False
    _inherit=['mail.thread','mail.activity.mixin']
    # rec_name="postcode"
    ref=fields.Char(default="new",readonly=True)
    active=fields.Boolean(default=True)
    name=fields.Char(default="new",size=11,translate=True)
    description = fields.Text(tracking=1,translate=True)
    postcode = fields.Char(required=1,translate=True)
    expected_price = fields.Float(digits=(0,7))
    selling_price = fields.Float()
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    # faceades = fields.Integer(groups="app_one.property_manager_group" )
    faceades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    diff=fields.Float(compute="_compute_diff",store=1)
    create_time=fields.Datetime(readonly="1",default=fields.Datetime.now())
    next_time=fields.Datetime(compute="_compute_next_time")
    garden_orientation = fields.Selection([
        ('north','North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West'),
    ],default="north")


    line_ids=fields.One2many("property.line","property_id")
    owner_id=fields.Many2one("owner")
    owner_address=fields.Char(related="owner_id.address",readonly=False)
    owner_phone = fields.Char(related="owner_id.phone",readonly=False)
    tag_ids=fields.Many2many("tag")

    state = fields.Selection(
        selection=[
            ('draft', 'Draft'),
            ('pending', 'Pending'),
            ('sold', 'Sold'),
            ('closed', 'Closed'),
        ],
        string="State",
        default="draft"
    )
    dateavailability = fields.Date(tracking=1)
    expected_selling_date=fields.Date()
    is_late=fields.Boolean()

    _sql_constraints = [
        ('unique_name','unique("name")','This name is exist')
    ]
    @api.depends("create_time")
    def _compute_next_time(self):
        for rec in self:
            if rec.create_time:
                rec.next_time=rec.create_time + timedelta(hours=6)
            else:
                rec.next_time=False

    @api.depends('expected_price','selling_price','owner_id.phone')
    def _compute_diff(self):
        for rec in self:
            print(rec)
            print("inside methode compute")
            rec.diff=rec.expected_price-rec.selling_price
    @api.onchange("expected_price")
    def _onchange_expected_price(self):
        for rec in self:
            print(rec)
            print("inside _onchange_expected_price########")
            rec.expected_price = rec.expected_price * 0.9
            return {
                'warning':{
                    'title':'warning','message':'negative value ashrofaaaaaa','type':'notification'
                }
            }
    @api.constrains("bedrooms")
    def _check_bedrooms_greater_zero(self):
        for rec in self:
            if rec.bedrooms is None or rec.bedrooms <= 0:
                raise ValidationError(_("The number of bedrooms must be greater than zero,Ashrofaaaaaaa"))



    def check_expected_selling_date(self):
        today = fields.Date.today()

        # البحث فقط عن العقارات غير المغلقة أو المباعة
        properties_to_check = self.search([
            ('state', 'not in', ['closed', 'sold']),  # استبعاد العقارات التي لا تحتاج إلى فحص
            ('expected_selling_date', '!=', False)  # التأكد من أن التاريخ ليس فارغًا
        ])

        for rec in properties_to_check:
            if rec.expected_selling_date < today:
                rec.sudo().write({'is_late': True})
                print(f"✅ العقار '{rec.name}' متأخر وتم تحديث is_late إلى True.")
            else:
                rec.sudo().write({'is_late': False})
                print(f"❌ العقار '{rec.name}' ليس متأخرًا، وتم تحديث is_late إلى False.")

    # env.ref('app_one.ashraf_check_expected_selling_date_action_cron').method_direct_trigger()

    def write(self,vals):
        res=super(Property,self).write(vals)
        print("inside write method")
        return res

    def unlink(self):
        res=super(Property,self).unlink()
        print("inside unlink method")
        return res

    def create_history_record(self, old_state, new_state,reason=""):
        for rec in self:
            rec.env['property.history'].create({
                'user_id': rec.env.uid,  # إزالة علامات الاقتباس
                'property_id': rec.id,
                'old_state': old_state,
                'new_state': new_state,  # إزالة علامات الاقتباس
                'reason':reason or "",
                'line_ids':[(0,0,{'description':line.description,'area':line.area})for line in rec.line_ids],
            })

    def action_draft(self):
        for rec in self:
            rec.create_history_record(rec.state,'draft')
            rec.state='draft'

    def action_pending(self):
        for rec in self:
                rec.create_history_record(rec.state, 'pending')
                rec.state='pending'


    def action_sold(self):
        for rec in self:
                rec.create_history_record(rec.state, 'sold')
                rec.state = 'sold'
    def action_closed(self):
        for rec in self:
            rec.create_history_record(rec.state, 'closed')
            rec.state = 'closed'
    # def action_cancel(self):
    #     self.state = 'cancel'

    def action_env(self):
        print(self.env.user)
        print(self.env.user.login)
        print(self.env.user.name)
        print(self.env.user.id)
        print(self.env.uid)
        print(self.env.company)
        print(self.env.company.id)
        print(self.env.company.name)
        print(self.env.company.street)
        print(self.env.context)
        print(self.env.cr)
        print(self.env['owner'].create({
            'name':'awwad',
            'phone':'0107777777777777'

        }))
        print(self.env['owner'].search([]))

    @api.model
    def create(self, vals):
        vals['ref'] = self.env['ir.sequence'].next_by_code('property.seq')
        return super(Property, self).create(vals)
    # @api.model_create_multi
    # def create(self,vals):
    #     res=super(Property,self).create(vals)
    #     print("inside create methode")
    #     return res

    @api.model
    def _search(self, domain, offset=0, limit=None, order=None, access_rights_uid=None):
        print("inside search method")
        res = super()._search(domain, offset=offset, limit=limit, order=order, access_rights_uid=access_rights_uid)
        return res

    def write(self, vals):
        res = super(Property, self).write(vals)
        if 'state' in vals and vals['state'] in ['closed', 'sold']:
            self.update({'expected_selling_date': False})
        return res
    def action_open_change_wizard_pythone(self):
        action=self.env['ir.actions.actions']._for_xml_id('app_one.chang_state_wizard_action')
        action['context']={'default_property_id':self.id}
        return action
    def action_open_state_wizard_xml(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Change State Wizard',
            'res_model': 'chang.state',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_property_id': self.id
            }
        }
class PropertyLine(models.Model):
    _name="property.line"
    property_id=fields.Many2one("property")
    description = fields.Text()
    area = fields.Float()




