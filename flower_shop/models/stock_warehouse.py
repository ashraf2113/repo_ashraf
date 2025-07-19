import logging
import requests
from odoo import models, fields, api, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

class StockWarehouse(models.Model):
    _inherit = 'stock.warehouse'

    def _get_api_key_and_location(self, show_error=True):
        api_key = self.env["ir.config_parameter"].sudo().get_param("flower_shop.weather")
        if not api_key or api_key == "unset":
            if show_error:
                raise UserError(_("Weather API key is not set in system parameters."))
            else:
                _logger.warning("Weather API key is not set.")
            return False, False, False
        if not self.partner_id or not self.partner_id.partner_latitude or not self.partner_id.partner_longitude:
            if show_error:
                raise UserError(_("Warehouse '%s' location (partner coordinates) not set.") % self.name)
            else:
                _logger.warning("Warehouse '%s' location (partner coordinates) not set.", self.name)
            return False, False, False
        return api_key, self.partner_id.partner_latitude, self.partner_id.partner_longitude

    def get_weather(self, show_error=True):
        self.ensure_one()
        api_key, lat, lng = self._get_api_key_and_location(show_error)
        if not api_key:
            return
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lng}&appid={api_key}&units=metric"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            entries = response.json()
            self.env["stock.warehouse.weather"].create({
                "warehouse_id": self.id,
                "description": entries["weather"][0]["description"],
                "pressure": entries["main"]["pressure"],
                "temperature": entries["main"]["temp"],
                "humidity": entries["main"]["humidity"] / 100,
                "wind_speed": entries["wind"]["speed"],
                "rain_volume": entries.get("rain", {}).get("1h", 0),
                "capture_time": fields.Datetime.now(),
            })
        except Exception as e:
            _logger.error("Failed to fetch weather for warehouse %s: %s", self.name, e)
            if show_error:
                raise UserError(_("Failed to fetch weather: %s") % e)

    def get_weather_all_warehouses(self):
        for warehouse in self.search([]):
            try:
                warehouse.get_weather(show_error=False)
            except Exception as e:
                _logger.warning("Error updating weather for warehouse %s: %s", warehouse.name, e)

    def get_forecast_all_warehouses(self, show_error=True):
        flower_serials_to_water = self.env["stock.lot"]
        for warehouse in self:
            api_key, lat, lng = warehouse._get_api_key_and_location(show_error)
            if not api_key:
                continue
            url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lng}&appid={api_key}&units=metric"
            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                entries = response.json()
                is_rainy_today = False
                # check first 4 entries from 9 AM to 6 PM (~3-hour intervals)
                for i in range(0, 4):
                    forecast = entries["list"][i]
                    if "rain" in forecast:
                        rain = forecast["rain"].get("3h", 0)
                        if rain > 0.2:
                            is_rainy_today = True
                            break
                if is_rainy_today:
                    flower_products = self.env["product.product"].search([("is_flower", "=", True)])
                    quants = self.env["stock.quant"].search([
                        ("product_id", "in", flower_products.ids),
                        ("location_id", "=", warehouse.lot_stock_id.id)
                    ])
                    flower_serials_to_water |= quants.mapped('lot_id')
            except Exception as e:
                _logger.error("Failed to fetch forecast for warehouse %s: %s", warehouse.name, e)
                if show_error:
                    raise UserError(_("Failed to fetch forecast: %s") % e)
        for flower_serial in flower_serials_to_water:
            self.env["flower.water"].create({
                "serial_id": flower_serial.id,
            })
