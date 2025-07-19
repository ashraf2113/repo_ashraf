import datetime
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class CancelInWizard(models.TransientModel):
    _name = "cancel.in.wizard"
    _description = "Cancel In Wizard"
    _rec_name = "name"

    time_cancel = fields.Datetime("Time Cancel")  # حقل من نوع Datetime
    name = fields.Char(string='Name')
    patients_id = fields.Many2many("hospital.patients", string='Patient many choices',domain=[('|'),('state','=','draft'),('periority','in',('0','1',False))])
    reason = fields.Text("Reason", default="ايه سبب الالغاء يا حاج اشرف يا ترى")

    @api.model
    def default_get(self, fields_list):
        res = super(CancelInWizard, self).default_get(fields_list)
        res["time_cancel"] = fields.Datetime.now()  # ضبط الحقل للحصول على الوقت الحالي
        res["reason"] = "يا عم الحاج قوللي ايه السبب للالغاء"
        return res

    def action_cancel(self):
        # التحقق من تطابق التاريخ فقط بين `time_cancel` و `fields.Date.today()`
        if self.time_cancel and self.time_cancel.date() == fields.Date.today():
            raise ValidationError(_("!!!! انت اهبل يا بني اضبط الزمن بلاش تاريخ اليوم ..ضحكتني يا واد"))
        return True
