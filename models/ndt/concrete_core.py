from odoo import api, fields, models
from odoo.exceptions import UserError,ValidationError
import math

class ConcreteCore(models.Model):
    _name = "ndt.concrete.core"
    _inherit = "lerm.eln"
    _rec_name = "name"

    name = fields.Char("Name",default="Rebound Hammer")
    parameter_id = fields.Many2one('eln.parameters.result',string="Parameter")
    child_lines = fields.One2many('ndt.concrete.core.line','parent_id',string="Parameter")
    average = fields.Integer(string="Average Compressive Strength in Mpa",compute="_compute_average")


    # @api.depends('child_lines.avg')
    # def _compute_average(self):
    #     for record in self:
    #         total_value = sum(record.child_lines.mapped('avg'))
    #         self.average = int(round(total_value / len(record.child_lines))) if record.child_lines else 0.0


    @api.model
    def create(self, vals):
        # import wdb;wdb.set_trace()
        record = super(ConcreteCore, self).create(vals)
        record.parameter_id.write({'model_id':record.id})
        return record

class CarbonationLine(models.Model):
    _name = "ndt.concrete.core.line"
    parent_id = fields.Many2one('ndt.concrete.core',string="Parent Id")
    identification = fields.Char(string="Identification Ark")
    dia = fields.Float(string="dia d mm")
    length = fields.Float(string="length h mm")
    hd = fields.Float(string="H/D")
    dry = fields.Float(string="Dry wt kg")
    failure_load = fields.Float(string="Failure Load kN")
    core_strength = fields.Float(string="6")
    