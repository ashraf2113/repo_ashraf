# -*- coding: utf-8 -*-
from odoo.exceptions import UserError
from odoo import models, fields
from datetime import timedelta

class StockLot(models.Model):
    _inherit = 'stock.lot'

    water_record_ids = fields.One2many(
        comodel_name='flower.water',
        inverse_name='lot_id',
        string='Watering Records'
    )
    name_plant = fields.Char(string="اسم النبتة")  # تأكد من كتابة Char وليس Chr
    next_watering_date = fields.Datetime(
        string='Next Watering Date',
        store=True
    )

    def action_create_water_record(self):
        if len(self) != 1:
            raise UserError("يرجى تحديد سجل واحد فقط.")

        return {
            'name': 'Water Now',
            'type': 'ir.actions.act_window',
            'res_model': 'flower.water',
            'view_mode': 'form,list',
            'context': {
                'default_lot_id': self.id,
                'default_name_plant': self.name_plant,
            },
            'target': 'current',
        }

    def action_bulk_water(self):
        FlowerWater = self.env['flower.water']
        for lot in self:
            # البحث عن آخر سجل سقي موجود لهذه النبتة
            last_record = FlowerWater.search([
                ('lot_id', '=', lot.id)
            ], order='watering_date desc', limit=1)

            # تحديد تاريخ الري بناءً على السجل السابق
            if last_record:
                watering_date = last_record.watering_date + timedelta(days=last_record.watering_frequency)
            else:
                watering_date = fields.Datetime.now()  # إذا لم يكن هناك سجل سابق، استخدم الوقت الحالي

            FlowerWater.create({
                'lot_id': lot.id,
                'watering_date': watering_date,
                'user_id': self.env.uid,
                'note': 'Auto watering from list view',
                'name_plant': lot.name_plant,
            })

        return {
            'type': 'ir.actions.act_window',
            'name': 'Water Records',
            'res_model': 'flower.water',
            'view_mode': 'tree,form',
            'target': 'current',
            'domain': [('lot_id', 'in', self.ids)],
        }

    def print_custom_pdf(self):
        all_records = self.env['flower.water'].search([])
        return self.env.ref('flower_watering.report_screen_flower_water_ashraf').report_action(all_records)
