from odoo import api, fields, models
from odoo.exceptions import UserError,ValidationError
import math


class CrackWidth(models.Model):
    _name = "ndt.crack.width"
    _inherit = "lerm.eln"
    _rec_name = "name"
    name = fields.Char("Name",default="Crack Width")
    parameter_id = fields.Many2one('eln.parameters.result',string="Parameter")
    child_lines = fields.One2many('ndt.crack.width.line','parent_id',string="Parameter")
    average = fields.Float(string='Average', digits=(16, 2), compute='_compute_average')
    min = fields.Float(string='Min', digits=(16, 2), compute='_compute_min_max')
    max = fields.Float(string='Max', digits=(16, 2), compute='_compute_min_max')

    @api.depends('child_lines.crack_width_mm')
    def _compute_average(self):
        for record in self:
            total_crack_width = sum(record.child_lines.mapped('crack_width_mm'))
            num_records = len(record.child_lines)

            if num_records > 0:
                record.average = total_crack_width / num_records
            else:
                record.average = 0.0

    @api.depends('child_lines.crack_width_mm')
    def _compute_min_max(self):
        for record in self:
            crack_width_values = record.child_lines.mapped('crack_width_mm')
            if crack_width_values:
                record.min = min(crack_width_values)
                record.max = max(crack_width_values)
            else:
                record.min = 0.0
                record.max = 0.0


class CrackWidthLine(models.Model):
    _name = "ndt.crack.width.line"
    parent_id = fields.Many2one('ndt.crack.width',string="Parent Id")
    member = fields.Char("Element Type")
    location = fields.Char("Location")
    crack_width_mm = fields.Float("Crack Width in mm")

    

