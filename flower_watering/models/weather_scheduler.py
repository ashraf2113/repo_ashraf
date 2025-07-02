import logging
import requests
from odoo import models, fields, api, _
from datetime import datetime
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)  # نحط اللوج هنا مش جوه الكلاس

class WeatherScheduler(models.Model):
    _inherit = 'stock.warehouse'

    city = fields.Char(related='partner_id.city', string='City', store=True)

    @api.model
    def fetch_and_process_weather(self):
        api_key = self.env['ir.config_parameter'].sudo().get_param('flower_watering.weather_api_key')
        if not api_key:
            _logger.warning("API key not configured.")
            return

        for warehouse in self.search([]):
            if not warehouse.partner_id or not warehouse.partner_id.city:
                _logger.warning(f"Warehouse {warehouse.name} missing city info. Skipping.")
                continue

            city = warehouse.partner_id.city
            url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}"

            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                data = response.json()
                _logger.info(f"Fetched weather for {city}: {data}")
            except Exception as e:
                _logger.error(f"Error fetching weather for {city}: {e}")
                continue

            weather_time = datetime.utcnow()


            temperature = data['current']['temp_c']
            humidity = data['current']['humidity']
            pressure = data['current']['pressure_mb']
            rain_mm = data['current'].get('precip_mm', 0.0)

            lots = self.env['stock.lot'].search([('warehouse_id', '=', warehouse.id)])
            for lot in lots:
                self.env['stock.warehouse.weather'].create({
                    'lot_id': lot.id,
                    'warehouse_id': warehouse.id,
                    'watering_date': weather_time,  # ← لازم يكون موجود
                    'weather_datetime': weather_time,
                    'temperature': temperature,
                    'humidity': humidity,
                    'pressure': pressure,
                    'rain_mm': rain_mm,
                })

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


