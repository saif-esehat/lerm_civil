from odoo import api, fields, models
from odoo.exceptions import UserError,ValidationError
import math

class CrushingValue(models.Model):
    _name = "mechanical.crushing.value.coarse.aggregate"
    _inherit = "lerm.eln"
    _rec_name = "name"

    name = fields.Char("Name",default="Compressive Strength of Concrete Cube")
    parameter_id = fields.Many2one('eln.parameters.result',string="Parameter")
    child_lines = fields.One2many('mechanical.crushing.value.coarse.aggregate.line','parent_id',string="Parameter")

    average_crushing_value = fields.Float(string="Average Aggregate Crushing Value", compute="_compute_average_crushing_value")


    @api.depends('child_lines.crushing_value')
    def _compute_average_crushing_value(self):
        for record in self:
            if record.child_lines:
                sum_crushing_values = sum(record.child_lines.mapped('crushing_value'))
                record.average_crushing_value = sum_crushing_values / len(record.child_lines)
            else:
                record.average_crushing_value = 0.0
   

    @api.model
    def create(self, vals):
        # import wdb;wdb.set_trace()
        record = super(CrushingValue, self).create(vals)
        record.parameter_id.write({'model_id':record.id})
        return record

class CrushingValueLine(models.Model):
    _name = "mechanical.crushing.value.coarse.aggregate.line"
    parent_id = fields.Many2one('mechanical.crushing.value.coarse.aggregate',string="Parent Id")

    sample_no = fields.Integer(string="Sample", readonly=True, copy=False, default=1)
    wt_of_cylinder = fields.Integer(string="Weight of the empty cylinder in gms")
    total_wt_of_dried = fields.Integer(string="Total weight of oven dried ( 4.0 hrs ) aggregate sample filling the cylindrical measure in gms")
    total_wt_aggregate = fields.Float(string="Total weight of aggeregate in the cylinder in gms", compute="_compute_total_wt_aggregate")
    wt_of_aggregate_passing = fields.Float(string="Weight of aggregate fines passing 2.36 mm sieve after  the application of Load gms")
    wt_of_aggregate_retained = fields.Float(string="Weight of aggregate retained on 2.36 mm sieve after the test in gms", compute="_compute_wt_of_aggregate_retained")
    crushing_value = fields.Float(string="Aggregate Crushing value", compute="_compute_crushing_value")


    @api.depends('total_wt_of_dried', 'wt_of_cylinder')
    def _compute_total_wt_aggregate(self):
        for rec in self:
            rec.total_wt_aggregate = rec.total_wt_of_dried - rec.wt_of_cylinder


    @api.depends('total_wt_aggregate', 'wt_of_aggregate_passing')
    def _compute_wt_of_aggregate_retained(self):
        for rec in self:
            rec.wt_of_aggregate_retained = rec.total_wt_aggregate - rec.wt_of_aggregate_passing


    @api.depends('wt_of_aggregate_passing', 'total_wt_aggregate')
    def _compute_crushing_value(self):
        for rec in self:
            if rec.total_wt_aggregate != 0:
                rec.crushing_value = (rec.wt_of_aggregate_passing / rec.total_wt_aggregate) * 100
            else:
                rec.crushing_value = 0.0


    @api.model
    def create(self, vals):
        # Set the serial_no based on the existing records for the same parent
        if vals.get('parent_id'):
            existing_records = self.search([('parent_id', '=', vals['parent_id'])])
            if existing_records:
                max_serial_no = max(existing_records.mapped('sample_no'))
                vals['sample_no'] = max_serial_no + 1

        return super(CrushingValueLine, self).create(vals)

    def _reorder_serial_numbers(self):
        # Reorder the serial numbers based on the positions of the records in child_lines
        records = self.sorted('id')
        for index, record in enumerate(records):
            record.sample_no = index + 1


class AbrasionValueCoarseAggregate(models.Model):
    _name = "mechanical.abrasion.value.coarse.aggregate"
    _inherit = "lerm.eln"
    _rec_name = "name"

    name = fields.Char("Name",default="Abrasion Value")
    parameter_id = fields.Many2one('eln.parameters.result',string="Parameter")
    child_lines = fields.One2many('mechanical.abrasion.value.coarse.aggregate.line','parent_id',string="Parameter")
   


  

    @api.model
    def create(self, vals):
        # import wdb;wdb.set_trace()
        record = super(AbrasionValueCoarseAggregate, self).create(vals)
        record.parameter_id.write({'model_id':record.id})
        return record

class AbrasionValueCoarseAggregateLine(models.Model):
    _name = "mechanical.abrasion.value.coarse.aggregate.line"
    parent_id = fields.Many2one('mechanical.abrasion.value.coarse.aggregate',string="Parent Id")
   
    sr_no = fields.Integer(string="Test", readonly=True, copy=False, default=1)
    total_weight_sample = fields.Integer(string="Total weight of Sample in gms")
    weight_passing_sample = fields.Integer(string="Weight of Passing sample in 1.70 mm IS sieve in gms")
    weight_retain_sample = fields.Integer(string="Weight of Retain sample in 1.70 mm IS sieve in gms",compute="_compute_weight_retain_sample")
    abrasion_value_percentage = fields.Float(string="Abrasion Value (in %)",compute="_compute_sample_weight")


    @api.depends('total_weight_sample', 'weight_passing_sample')
    def _compute_weight_retain_sample(self):
        for line in self:
            line.weight_retain_sample = line.total_weight_sample - line.weight_passing_sample

    # @api.depends('total_weight_sample')
    # def _compute_sample_weight(self):
    #     for line in self:
    #         # Your computation logic for abrasion_value_percentage here
    #         pass


    @api.depends('total_weight_sample', 'weight_passing_sample')
    def _compute_sample_weight(self):
        for line in self:
            if line.total_weight_sample != 0:
                line.abrasion_value_percentage = (line.weight_passing_sample / line.total_weight_sample) * 100
            else:
                line.abrasion_value_percentage = 0.0


    @api.model
    def create(self, vals):
        # Set the serial_no based on the existing records for the same parent
        if vals.get('parent_id'):
            existing_records = self.search([('parent_id', '=', vals['parent_id'])])
            if existing_records:
                max_serial_no = max(existing_records.mapped('sr_no'))
                vals['sr_no'] = max_serial_no + 1

        return super(AbrasionValueCoarseAggregateLine, self).create(vals)

    def _reorder_serial_numbers(self):
        # Reorder the serial numbers based on the positions of the records in child_lines
        records = self.sorted('id')
        for index, record in enumerate(records):
            record.sr_no = index + 1



class SpecificGravityAndWaterAbsorption(models.Model):
    _name = "mechanical.specific.gravity.and.water.absorption"
    _inherit = "lerm.eln"
    _rec_name = "name"

    name = fields.Char("Name",default="Specific Gravity & Water Absorption")
    parameter_id = fields.Many2one('eln.parameters.result',string="Parameter")
    child_lines = fields.One2many('mechanical.specific.gravity.and.water.absorption.line','parent_id',string="Parameter")
   


  

    @api.model
    def create(self, vals):
        # import wdb;wdb.set_trace()
        record = super(SpecificGravityAndWaterAbsorption, self).create(vals)
        record.parameter_id.write({'model_id':record.id})
        return record

class SpecificGravityAndWaterAbsorptionLine(models.Model):
    _name = "mechanical.specific.gravity.and.water.absorption.line"
    parent_id = fields.Many2one('mechanical.specific.gravity.and.water.absorption',string="Parent Id")
   
    sr_no = fields.Integer(string="Test", readonly=True, copy=False, default=1)
    wt_surface_dry = fields.Integer(string="Weight of saturated surface dry (SSD) sample in air in gms")
    wt_sample_inwater = fields.Integer(string="Weight of saturated sample in water in gms")
    oven_dried_wt = fields.Integer(string="Oven dried weight of sample in gms")
    specific_gravity = fields.Float(string="Specific Gravity",compute="_compute_specific_gravity")
    water_absorption = fields.Float(string="Water absorption  %",compute="_compute_water_absorption")


    @api.depends('wt_surface_dry', 'wt_sample_inwater', 'oven_dried_wt')
    def _compute_specific_gravity(self):
        for line in self:
            if line.wt_surface_dry - line.wt_sample_inwater != 0:
                line.specific_gravity = line.oven_dried_wt / (line.wt_surface_dry - line.wt_sample_inwater)
            else:
                line.specific_gravity = 0.0



    @api.depends('wt_surface_dry', 'oven_dried_wt')
    def _compute_water_absorption(self):
        for line in self:
            if line.oven_dried_wt != 0:
                line.water_absorption = ((line.wt_surface_dry - line.oven_dried_wt) / line.oven_dried_wt) * 100
            else:
                line.water_absorption = 0.0


    @api.model
    def create(self, vals):
        # Set the serial_no based on the existing records for the same parent
        if vals.get('parent_id'):
            existing_records = self.search([('parent_id', '=', vals['parent_id'])])
            if existing_records:
                max_serial_no = max(existing_records.mapped('sr_no'))
                vals['sr_no'] = max_serial_no + 1

        return super(SpecificGravityAndWaterAbsorptionLine, self).create(vals)

    def _reorder_serial_numbers(self):
        # Reorder the serial numbers based on the positions of the records in child_lines
        records = self.sorted('id')
        for index, record in enumerate(records):
            record.sr_no = index + 1

    


    