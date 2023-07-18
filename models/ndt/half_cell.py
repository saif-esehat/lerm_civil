from odoo import api, fields, models
from odoo.exceptions import UserError,ValidationError
import math


class HalfCell(models.Model):
    _name = "ndt.half.cell"
    _inherit = "lerm.eln"
    _rec_name = "name"

    
    name = fields.Char("Name",default="Half Cell")
    parameter_id = fields.Many2one('eln.parameters.result', string="Parameter")
    structure_age = fields.Char("Year of Construction")
    temp = fields.Char("Temp")
    instrument = fields.Char("Instrument")
    child_lines_1 = fields.One2many('ndt.half.cell.one', 'parent_id', string="Parameter")
    child_lines_2 = fields.One2many('ndt.half.cell.two', 'parent_id', string="Parameter")

class HalfCellLineOne(models.Model):
    _name = "ndt.half.cell.one"
    parent_id = fields.Many2one('ndt.half.cell',string="Parent Id")
    member = fields.Char("Member")
    location = fields.Char("Location")
    level = fields.Char("Level")
    r1 = fields.Float("R1")
    r2 = fields.Float("R2")
    r3 = fields.Float("R3")
    r4 = fields.Float("R4")
    r5 = fields.Float("R5")
    avg = fields.Float("AVG")

    @api.depends('r1', 'r2', 'r3', 'r4', 'r5')
    def _compute_avg(self):
        for record in self:
            record.avg = (record.r1 + record.r2 + record.r3 + record.r4 + record.r5) / 5.0


class HalfCellLineTwo(models.Model):
    _name = "ndt.half.cell.two"
    parent_id = fields.Many2one('ndt.half.cell',string="Parent Id")
    member = fields.Char("Member")
    location = fields.Char("Location")
    level = fields.Char("Level")
    r1 = fields.Float("R1")
    r2 = fields.Float("R2")
    r3 = fields.Float("R3")
    r4 = fields.Float("R4")
    r5 = fields.Float("R5")
    avg = fields.Float("AVG")

    @api.depends('r1', 'r2', 'r3', 'r4', 'r5')
    def _compute_avg(self):
        for record in self:
            record.avg = (record.r1 + record.r2 + record.r3 + record.r4 + record.r5) / 5.0