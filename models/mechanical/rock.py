from odoo import api, fields, models
from odoo.exceptions import UserError,ValidationError
import math


class MechanicalRock(models.Model):
    _name = "mechanical.rock"
    _inherit = "lerm.eln"
    _rec_name = "name"

    name = fields.Char("Name",default="Specific Gravity, Water Absorption, Porosity & Dry Density")
    parameter_id = fields.Many2one('eln.parameters.result',string="Parameter")
    child_lines = fields.One2many('mechanical.rock.line','parent_id',string="Parameter")
    # wt_retained_total = fields.Float(string="Wt Retained Total",compute="_compute_wt_retained_total")
    
    @api.model
    def create(self, vals):
        # import wdb;wdb.set_trace()
        record = super(MechanicalRock, self).create(vals)
        record.parameter_id.write({'model_id':record.id})
        return record


class MechanicalRockLine(models.Model):
    _name = "mechanical.rock.line"
    parent_id = fields.Many2one('mechanical.rock',string="Parent Id")
   
    sr_no = fields.Integer(string="Sr No", readonly=True, copy=False, default=1)
    location = fields.Char(string="Location")
    sample_no = fields.Integer(string="Sample Number")
    depth = fields.Float(string="Depth in (mtr)")
    ssd_weight = fields.Float(string="SSD weight of sample in kg, Msat",digits=(16, 3))
    wt_sample_water = fields.Float(string="Weight of sample in water in kg, Msub",digits=(16, 3))
    oven_dry_wt = fields.Float(string="Oven dry weight of sample in kg, Ms",digits=(16, 3))
    porosity = fields.Float(string="Porosity",compute="_compute_porosity")
    water_absorption = fields.Float(string="Water Absorption",compute="_compute_water_absorption")
    dry_density = fields.Float(string="Dry Density",compute="_compute_dry_density",digits=(16, 3))
    saturated_spc_gravity = fields.Float(string="Saturated Specific Gravity",compute="_compute_saturated_spc_gravity")


    @api.depends('ssd_weight', 'oven_dry_wt', 'wt_sample_water')
    def _compute_porosity(self):
        for record in self:
            if record.ssd_weight and record.wt_sample_water != record.ssd_weight:
                record.porosity = (record.ssd_weight - record.oven_dry_wt) / (record.ssd_weight - record.wt_sample_water) * 100
            else:
                record.porosity = 0

    
    @api.depends('ssd_weight', 'oven_dry_wt')
    def _compute_water_absorption(self):
        for record in self:
            if record.oven_dry_wt:
                record.water_absorption = ((record.ssd_weight - record.oven_dry_wt) / record.oven_dry_wt) * 100
            else:
                record.water_absorption = 0

    @api.depends('ssd_weight', 'wt_sample_water', 'oven_dry_wt')
    def _compute_dry_density(self):
        for record in self:
            if record.ssd_weight and record.wt_sample_water and record.oven_dry_wt:
                record.dry_density = record.oven_dry_wt / record.ssd_weight - record.wt_sample_water
            else:
                record.dry_density = 0.0

    @api.depends('oven_dry_wt','dry_density')
    def _compute_saturated_spc_gravity(self):
        for record in self:
            if record.dry_density != 0:
                record.saturated_spc_gravity = record.oven_dry_wt/record.dry_density
            else:
                record.saturated_spc_gravity = 0.0

    @api.model
    def create(self, vals):
        # Set the serial_no based on the existing records for the same parent
        if vals.get('parent_id'):
            existing_records = self.search([('parent_id', '=', vals['parent_id'])])
            if existing_records:
                max_serial_no = max(existing_records.mapped('sr_no'))
                vals['sr_no'] = max_serial_no + 1

        return super(MechanicalRockLine, self).create(vals)

    def _reorder_serial_numbers(self):
        # Reorder the serial numbers based on the positions of the records in child_lines
        records = self.sorted('id')
        for index, record in enumerate(records):
            record.sr_no = index + 1