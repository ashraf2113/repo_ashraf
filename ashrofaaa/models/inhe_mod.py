from odoo import api, fields, models

class InheMod(models.Model):
    _inherit = "sale.order"  # تحديد النموذج الموروث منه بشكل صحيح

    confirmed_user_id = fields.Many2one("res.users", string="Confirmed User")

    def action_confirm(self):
        print("ashrofaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
        print("ashrofaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
        print("ashrofaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
        # استدعاء super مباشرة بدون الحاجة لتحديد SaleOrder
        res = super(InheMod, self).action_confirm()
        # يمكنك إضافة أي منطق إضافي هنا
        self.confirmed_user_id=self.env.user.id
        return res
    # def update_prices(self):
    #     super(InheMod)
class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"  # تحديد النموذج الموروث منه بشكل صحيح

    student = fields.Char("Student")  # إضافة الحقل الجديد
