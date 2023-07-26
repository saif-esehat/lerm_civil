from odoo import api, fields, models
from odoo.exceptions import UserError,ValidationError
import math

class CarbonationTest(models.Model):
    _name = "ndt.carbonation.test"
    _inherit = "lerm.eln"
    _rec_name = "name"

    
    name = fields.Char("Name",default="Carbonation Test")
    parameter_id = fields.Many2one('eln.parameters.result',string="Parameter")
    child_lines = fields.One2many('ndt.carbonation.test.line','parent_id',string="Parameter")

    @api.model
    def create(self, vals):
        # import wdb;wdb.set_trace()
        record = super(CarbonationTest, self).create(vals)
        record.parameter_id.write({'model_id':record.id})
        return record

class CarbonationnLine(models.Model):
    _name = "ndt.carbonation.test.line"
    parent_id = fields.Many2one('ndt.carbonation.test',string="Parent Id")
    member = fields.Char(string="Element Type")
    level = fields.Char(string="Level")
    location = fields.Char(string="Location")
    condition_of_concrete = fields.Selection([
        ('carbonated', 'Carbonated'),
        ('uncarbonated', 'Uncarbonated')
    ], string='Condition of Concrete',default='carbonated')
    depth = fields.Float(string='Depth of Carbonation in mm')
    


                


