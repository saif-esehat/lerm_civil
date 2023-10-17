from odoo import api, fields, models
from odoo.exceptions import UserError,ValidationError
from datetime import datetime , timedelta
import math



class AacBlockMechanical(models.Model):
    _name = "mechanical.aac.block"
    _inherit = "lerm.eln"
    _rec_name = "name"


    name = fields.Char("Name",default="AAC Block")
    parameter_id = fields.Many2one('eln.parameters.result', string="Parameter")

    sample_parameters = fields.Many2many('lerm.parameter.master',string="Parameters",compute="_compute_sample_parameters",store=True)
    eln_ref = fields.Many2one('lerm.eln',string="Eln")
    tests = fields.Many2many("mechanical.gypsum.test",string="Tests")

    @api.depends('eln_ref','sample_parameters')
    def _compute_visible(self):
        for record in self:
            record.dimension_visible = False
            record.moisture_visible  = False  
            record.density_visible = False
            record.drying_shrinkage_visible = False
            record.compressive_strength_visible = False

            for sample in record.sample_parameters:
                print("Samples internal id",sample.internal_id)
                if sample.internal_id == '04efc0bd-63e2-4e23-9436-51cde4fe2c57':
                    record.dimension_visible = True
                if sample.internal_id == '8e7282a0-3e80-4cee-b520-128b5a5f2015':
                    record.moisture_visible = True
                if sample.internal_id == '2d915d3b-0324-40f1-a2b9-e385a7cdc90d':
                    record.density_visible = True
                if sample.internal_id == 'ec5fa471-0e2a-411a-b1de-72cc41aed2d5':
                    record.drying_shrinkage_visible = True
                if sample.internal_id == '65321ea8-98e6-4d73-8941-5ac65d2504a9':
                    record.compressive_strength_visible = True

    @api.model
    def create(self, vals):
        # import wdb;wdb.set_trace()
        record = super(AacBlockMechanical, self).create(vals)
        record.get_all_fields()
        record.eln_ref.write({'model_id':record.id})
        return record

    @api.depends('eln_ref')
    def _compute_sample_parameters(self):
        for record in self:
            records = record.eln_ref.parameters_result.parameter.ids
            record.sample_parameters = records
            print("Records",records)

    def get_all_fields(self):
        record = self.env['mechanical.aac.block'].browse(self.ids[0])
        field_values = {}
        for field_name, field in record._fields.items():
            field_value = record[field_name]
            field_values[field_name] = field_value

        return field_values

    @api.depends('eln_ref')
    def _compute_sample_parameters(self):
        
        for record in self:
            records = record.eln_ref.parameters_result.parameter.ids
            record.sample_parameters = records
            print("Records",records)

    # Dimension
    dimension_name = fields.Char(default="Dimension")
    dimension_visible = fields.Boolean(compute="_compute_visible")

    dimension_table = fields.One2many('mech.aac.dimension.line','parent_id',string="Dimension")
    average_length = fields.Float('Average Length',compute="_compute_average_length")
    average_width = fields.Float('Average Width',compute="_compute_average_width")
    average_height = fields.Float('Average Height',compute="_compute_average_height")

    @api.depends('dimension_table.length')
    def _compute_average_length(self):
        for record in self:
            try:
                record.average_length = sum(record.dimension_table.mapped('length')) / len(
                    record.dimension_table)
            except:
                record.average_length = 0

    
    @api.depends('dimension_table.width')
    def _compute_average_width(self):
        for record in self:
            try:
                record.average_width = sum(record.dimension_table.mapped('width')) / len(
                    record.dimension_table)
            except:
                record.average_width = 0


    @api.depends('dimension_table.height')
    def _compute_average_height(self):
        for record in self:
            try:
                record.average_height = sum(record.dimension_table.mapped('height')) / len(
                    record.dimension_table)
            except:
                record.average_height = 0

    # Moisture Content
    moisture_name = fields.Char(default="Moisture Content")
    moisture_visible = fields.Boolean(compute="_compute_visible")

    moisture_content_table = fields.One2many('mech.aac.moisture.line','parent_id',string="Moisture Content")
    average_moisture_content = fields.Float("Average Moisture Content %",compute="_compute_average_moisture_content")


    @api.depends('moisture_content_table.moisture_content')
    def _compute_average_moisture_content(self):
        for record in self:
            try:
                record.average_moisture_content = sum(record.moisture_content_table.mapped('moisture_content')) / len(
                    record.moisture_content_table)
            except:
                record.average_moisture_content = 0

    # Density 
    density_name = fields.Char(default="Density Content")
    density_visible = fields.Boolean(compute="_compute_visible")

    density_table = fields.One2many('mech.aac.density.line','parent_id',string="Density")
    average_density = fields.Float("Average Density",compute="_compute_average_density")

    @api.depends('density_table.density')
    def _compute_average_density(self):
        for record in self:
            try:
                record.average_density = sum(record.density_table.mapped('density')) / len(
                    record.density_table)
            except:
                record.average_density = 0

    # Drying Shrinkage
    drying_shrinkage_name = fields.Char(default="Drying Shrinkage")
    drying_shrinkage_visible = fields.Boolean(compute="_compute_visible")

    drying_shrinkage_table = fields.One2many('mech.aac.drying.shrinkage.line','parent_id',string="Density")
    average_drying_shrinkage = fields.Float("Average Drying Shrinkage",compute="_compute_average_drying_shrinkage")

    @api.depends('drying_shrinkage_table.drying_shrinkage')
    def _compute_average_drying_shrinkage(self):
        for record in self:
            try:
                record.average_drying_shrinkage = sum(record.drying_shrinkage_table.mapped('drying_shrinkage')) / len(
                    record.drying_shrinkage_table)
            except:
                record.average_drying_shrinkage = 0


    # Compressive Strength
    compressive_strength_name = fields.Char(default="Compressive Strength")
    compressive_strength_visible = fields.Boolean(compute="_compute_visible")

    compressive_strength_table = fields.One2many('mech.aac.compressive.strength.line','parent_id',string="Compressive Strength")
    average_compressive_strength = fields.Float("Average Compressive Strength",compute="_compute_average_compressive_strength")
    
    @api.depends('compressive_strength_table.compressive_strength')
    def _compute_average_compressive_strength(self):
        for record in self:
            try:
                record.average_compressive_strength = sum(record.compressive_strength_table.mapped('compressive_strength')) / len(
                    record.compressive_strength_table)
            except:
                record.average_compressive_strength = 0

class AacDimensionLine(models.Model):
    _name = "mech.aac.dimension.line"
    parent_id = fields.Many2one('mechanical.aac.block', string="Parent Id")

    length = fields.Float('Length')
    width = fields.Float('Width')
    height = fields.Float('Height')


class AacMoistureLine(models.Model):
    _name = "mech.aac.moisture.line"
    parent_id = fields.Many2one('mechanical.aac.block', string="Parent Id")

    wt_sample = fields.Float('Weight of sample W1 in gm')
    oven_wt = fields.Float('Oven dry Weight of sample W in gm')
    moisture_content = fields.Float('Moisture Content %',compute="_compute_moisture_content")

    @api.depends('wt_sample','oven_wt')
    def _compute_moisture_content(self):
        for record in self:
            if record.oven_wt != 0:
                record.moisture_content = round(((record.wt_sample - record.oven_wt)/record.oven_wt *100),2)
            else:
                record.moisture_content = 0

class AacDensityLine(models.Model):
    _name = "mech.aac.density.line"
    parent_id = fields.Many2one('mechanical.aac.block', string="Parent Id")

    length = fields.Float('Length of Sample before Drying',digits=(16,3))
    width = fields.Float('Width of Sample before Drying',digits=(16,3))
    height = fields.Float('Height of Sample before Drying',digits=(16,3))
    volume = fields.Float('Volume of Sample',compute="_compute_volume",digits=(16,7))
    wt_sample = fields.Float("Weight of Sample after Drying",digits=(16,3))
    density = fields.Float("Density of Sample",compute="Compute_density",digits=(16,3))

    @api.depends('length','width','height')
    def _compute_volume(self):
        for record in self:
            record.volume = round((record.length * record.width * record.height),7)

    @api.depends('volume','wt_sample')
    def Compute_density(self):
        for record in self:
            if record.volume != 0:
                record.density = rounnd((record.wt_sample / record.volume),3)
            else:
                record.density = 0


class AacDryingShrinkageLine(models.Model):
    _name = "mech.aac.drying.shrinkage.line"
    parent_id = fields.Many2one('mechanical.aac.block', string="Parent Id")

    length = fields.Float('Length of Specimen')
    initial_length = fields.Float('Initial Length L1 in mm')
    final_length = fields.Float('Final Length L2 in mm')
    change_length = fields.Float('Change in Length in mm',compute="_compute_change_length")
    drying_shrinkage = fields.Float('Drying Shrinkage in %',compute="_compute_drying_shrinkage")

    @api.depends('initial_length','final_length')
    def _compute_change_length(self):
        for record in self:
            record.change_length = record.initial_length - record.final_length

    @api.depends('change_length','length')
    def _compute_drying_shrinkage(self):
        for record in self:
            if record.length != 0:
                record.drying_shrinkage = record.change_length / record.length * 100
            else:
                record.drying_shrinkage = 0


class AacCompressiveStrengthLine(models.Model):
    _name = "mech.aac.compressive.strength.line"
    parent_id = fields.Many2one('mechanical.aac.block', string="Parent Id")

    crosssectional_area = fields.Float('Crosssectional Area')
    load = fields.Float('Load (p) kN')
    compressive_strength = fields.Float('Compressive Strength',compute="_compute_compressive_strength")


    def _compute_compressive_strength(self):
        for record in self:
            if record.crosssectional_area != 0:
                record.compressive_strength = round((record.load/record.crosssectional_area)*1000,2)
            else:
                record.compressive_strength = 0