from odoo import api, fields, models
from odoo.tools.safe_eval import safe_eval


class PlaysGround(models.Model):
    _name = "env.find"
    _description = "Env  Find"

    # الحقول الأساسية
    model_id = fields.Many2one("ir.model", string="Model")
    code = fields.Text(string="Code")
    result = fields.Text(string="Result")

    # دالة لمسح الحقول
    def action_clear(self):
        """Clear the code and result fields."""
        self.code = ""
        self.result = ""

    # دالة لتنفيذ الكود
    def action_execute(self):
        """Execute the code provided in the 'code' field safely."""
        try:
            # إعداد بيئة التنفيذ
            localdict = {'env': self.env, 'self': self}

            # إذا كان النموذج محددًا، أضفه إلى البيئة
            if self.model_id:
                model = self.env[self.model_id.model]
                localdict['model'] = model

            # تنفيذ الكود باستخدام safe_eval
            self.result = str(safe_eval(self.code or "", localdict))
        except Exception as e:
            # تسجيل أي خطأ يحدث أثناء التنفيذ
            self.result = f"Error: {str(e)}"
