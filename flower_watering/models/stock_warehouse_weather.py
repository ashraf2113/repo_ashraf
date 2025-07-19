from odoo.exceptions import UserError
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import timedelta
from odoo.exceptions import UserError

class StockWarehouseWeather(models.Model):
    _name = 'stock.warehouse.weather'
    _description = 'Warehouse Weather Info'

    _order = 'weather_datetime desc'

    lot_id = fields.Many2one(
        comodel_name='stock.lot',
        string='Flower (Serial Number)',
        required=True,
        ondelete='cascade'
    )

    watering_date = fields.Datetime(
        string='Watering Date',
        default=None,  # اجعلها فارغة للسماح للمستخدم بالإدخال
        required=True
    )

    name_plant=fields.Char("Name Plant")
    note = fields.Text(string='Note')
    # sellected=fields.Boolean("Sellected")
    user_id = fields.Many2one(
        comodel_name='res.users',
        string='Watered By',
        default=lambda self: self.env.user
    )

    next_watering_date = fields.Datetime(
        string='Next Watering Date',
        compute='_compute_next_watering_date',
        store=True
    )

    watering_frequency = fields.Integer(
        string='Watering Frequency (Days)',
        default=7,
        help='Minimum number of days between watering'
    )
    warehouse_id = fields.Many2one('stock.warehouse', string='Warehouse', required=True)
    weather_datetime = fields.Datetime(string='Weather Time', required=True)
    temperature = fields.Float(string='Temperature (°C)')
    humidity = fields.Float(string='Humidity (%)')
    pressure = fields.Float(string='Pressure (hPa)')
    rain_mm = fields.Float(string='Rain Volume (mm)')

    @api.depends('watering_date', 'watering_frequency')
    def _compute_next_watering_date(self):
        for record in self:
            if record.watering_date and record.watering_frequency:
                record.next_watering_date = record.watering_date + timedelta(days=record.watering_frequency)

    def action_fetch_weather(self):
        # 1. إصلاح المدن المرتبطة بالمخازن أولاً
        self.env['stock.warehouse'].action_fix_partner_city()

        # 2. ثم جلب بيانات الطقس وتسجيلها
        self.env['stock.warehouse'].fetch_and_process_weather()

        # 3. إظهار إشعار للمستخدم بشكل غير مزعج
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'عملية ناجحة ✅',
                'message': 'تم ربط المدن وتحديث بيانات الطقس بنجاح.',
                'type': 'success',  # يمكن أيضاً استخدام 'warning' أو 'danger'
                'sticky': False,  # لو True هيفضل ظاهر حتى المستخدم يقفله
            }
        }


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    weather_api_key = fields.Char(string="Weather API Key", config_parameter="flower_watering.weather_api_key")

