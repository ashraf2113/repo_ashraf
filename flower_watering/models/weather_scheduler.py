import logging
import requests
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)  # نحط اللوج هنا مش جوه الكلاس

class WeatherScheduler(models.Model):
    _inherit = 'stock.warehouse'

    city = fields.Char(related='partner_id.city', string='City', store=True)

    @api.model
    def fetch_and_process_weather(self):
        # 1. جلب مفتاح API
        api_key = self.env['ir.config_parameter'].sudo().get_param('flower_watering.weather_api_key')
        if not api_key:
            _logger.warning("API key not configured.")
            return

        # 2. التكرار على كل المخازن
        for warehouse in self.search([]):
            if not warehouse.partner_id or not warehouse.partner_id.city:
                _logger.warning(f"Warehouse {warehouse.name} is missing city info. Skipping.")
                continue

            city = warehouse.partner_id.city
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()  # تأكد إن الاستجابة ناجحة
                data = response.json()
                _logger.info(f"Fetched weather for {city}: {data}")
            except Exception as e:
                _logger.error(f"Error fetching weather for {city}: {e}")
                continue

            # 3. استخراج القيم
            rain = data.get('rain', {}).get('1h', 0.0)
            temperature = data.get('main', {}).get('temp')
            humidity = data.get('main', {}).get('humidity')
            pressure = data.get('main', {}).get('pressure')

            if temperature is None or humidity is None or pressure is None:
                _logger.warning(f"Incomplete weather data for {city}. Skipping record creation.")
                continue

            weather_time = fields.Datetime.now()

            # 4. إنشاء سجل الطقس لكل نبتة (lot)
            lots = self.env['stock.lot'].search([('warehouse_id', '=', warehouse.id)])
            for lot in lots:
                self.env['stock.warehouse.weather'].create({
                    'lot_id': lot.id,  # ← الحقل المطلوب
                    'warehouse_id': warehouse.id,
                    'weather_datetime': weather_time,
                    'temperature': temperature,
                    'humidity': humidity,
                    'pressure': pressure,
                    'rain_mm': rain
                })

                # 5. تنفيذ الري التلقائي إذا كانت الشروط مناسبة
                if 9 <= weather_time.hour <= 18 and rain > 0.2:
                    self.env['flower.water'].create({
                        'lot_id': lot.id,
                        'watering_date': weather_time,
                        'note': f"Auto watering from weather at {city}",
                        'name_plant': lot.name_plant,
                        'user_id': self.env.uid
                    })

            _logger.info(f"Weather recorded and watering triggered for warehouse {warehouse.name} at {weather_time}")

    def action_fix_partner_city(self):
        for warehouse in self:
            partner = warehouse.partner_id
            if partner and not partner.city:
                child_with_city = partner.child_ids.filtered(lambda p: p.city)
                if child_with_city:
                    warehouse.partner_id = child_with_city[0]
                    _logger.info(f"تم ربط العنوان الفرعي مع مدينة للمخزن: {warehouse.name}")
                else:
                    _logger.warning(f"لا يوجد عنوان فرعي يحتوي على مدينة للمخزن: {warehouse.name}")
        _logger.info("✅ تمت محاولة إصلاح جميع المخازن.")


