from odoo import api, fields, models
from odoo.exceptions import UserError,ValidationError
import math

class ReboundHammer(models.Model):
    _name = "ndt.rebound.hammer"
    _inherit = "lerm.eln"
    _rec_name = "name"

    name = fields.Char("Name",default="Rebound Hammer")
    parameter_id = fields.Many2one('eln.parameters.result',string="Parameter")
    child_lines = fields.One2many('ndt.rebound.hammer.line','parent_id',string="Parameter")
    average = fields.Integer(string="Average",compute="_compute_average")
    minimum = fields.Integer(string="Minimum",compute="_compute_min_max")
    maximum = fields.Integer(string="Maximum",compute="_compute_min_max")

    @api.depends('child_lines.avg')
    def _compute_average(self):
        for record in self:
            total_value = sum(record.child_lines.mapped('avg'))
            self.average = int(round(total_value / len(record.child_lines))) if record.child_lines else 0.0

    @api.depends('child_lines.avg')
    def _compute_min_max(self):
        for record in self:
            values = record.child_lines.mapped('avg')
            self.minimum = int(min(values)) if values else 0.0
            self.maximum = int(max(values)) if values else 0.0


    @api.model
    def create(self, vals):
        # import wdb;wdb.set_trace()
        record = super(ReboundHammer, self).create(vals)
        record.parameter_id.write({'model_id':record.id})
        return record

class CarbonationnLine(models.Model):
    _name = "ndt.rebound.hammer.line"
    parent_id = fields.Many2one('ndt.rebound.hammer',string="Parent Id")
    element = fields.Char(string="Element Type")
    location = fields.Char(string="Location")
    f1 = fields.Integer(string="1")
    f2 = fields.Integer(string="2")
    f3 = fields.Integer(string="3")
    f4 = fields.Integer(string="4")
    f5 = fields.Integer(string="5")
    f6 = fields.Integer(string="6")
    avg = fields.Integer(string="Average" ,compute="_compute_average")
    mpa = fields.Integer(string="Mpa")
    direction = fields.Selection([
        ('horizontal', 'Horizontal'),
        ('vertical_up', 'Vertical Up'), 
        ('vertical_down', 'Vertical Down')], string='Direction')
    

    @api.depends('f1','f2','f3','f4','f5','f6')
    def _compute_average(self):
        for record in self:
            self.avg = round((self.f1 + self.f2 +self.f3 + self.f4 + self.f5 + self.f6)/6)
                


