from odoo import api, fields, models
from odoo.exceptions import UserError,ValidationError
import math

class ActCompressiveStrength(models.Model):
    _name = "mechanical.act.compressive"
    _inherit = "lerm.eln"
    _rec_name = "name"

    name = fields.Char("Name", default="ACT Compressive")
    parameter_id = fields.Many2one('eln.parameters.result', string="Parameter")
    child_lines = fields.One2many('mechanical.act.compressive.line', 'parent_id', string="Parameter")
    average_compr_strength = fields.Float(string="Average Compressive Strength in N/mm2", compute="_compute_average_compr_strength",digits=(12,2))
    act_compressive = fields.Float(string="ACT Compressive", compute="_compute_act_compressive",digits=(12,2))
    grade = fields.Many2one('lerm.grade.line',string="Grade",compute="_compute_grade_id",store=True)
    size = fields.Many2one('lerm.size.line',string="Size",compute="_compute_size_id",store=True)
    eln_ref = fields.Many2one('lerm.eln',string="ELN")
    sample_parameters = fields.Many2many('lerm.parameter.master',string="Parameters",compute="_compute_sample_parameters",store=True)

    @api.depends('child_lines.compressive_strength')
    def _compute_average_compr_strength(self):
        for record in self:
            compressive_strengths = record.child_lines.mapped('compressive_strength')
            if compressive_strengths:
                record.average_compr_strength = sum(compressive_strengths) / len(compressive_strengths)
            else:
                record.average_compr_strength = 0.0



    # @api.depends('average_compr_strength')
    # def _compute_act_average(self):
    #     for record in self:
    #         record.act_compressive = record.average_compr_strength * 1.64 + 8.09

    @api.depends('average_compr_strength')
    def _compute_act_compressive(self):
        for record in self:
            record.act_compressive = (record.average_compr_strength) * (1.64) + (8.09)

    @api.depends('eln_ref')
    def _compute_grade_id(self):
        if self.eln_ref:
            self.grade = self.eln_ref.grade_id.id

    @api.depends('eln_ref')
    def _compute_size_id(self):
        if self.eln_ref:
            self.size = self.eln_ref.size_id.id
    
    @api.depends('eln_ref')
    def _compute_sample_parameters(self):
        for record in self:
            records = record.eln_ref.parameters_result.parameter.ids
            record.sample_parameters = records
            print("Records",records)



   
    @api.model
    def create(self, vals):
        record = super(ActCompressiveStrength, self).create(vals)
        record.parameter_id.write({'model_id': record.id})
        return record


class ActCompressiveStrengthLine(models.Model):
    _name = "mechanical.act.compressive.line"
    parent_id = fields.Many2one('mechanical.act.compressive', string="Parent Id")

    sr_no = fields.Integer(string="Sr No", readonly=True, copy=False, default=1)
    length = fields.Float(string="Length")
    width = fields.Float(string="Width")
    area = fields.Float(string="Area mm2", compute="_compute_area", store=True,digits=(12,2))  # Added store=True
    id_mark = fields.Char(string="Id Mark")
    weight_sample = fields.Float(string="Weight of Sample in kgs")
    crushing_load = fields.Float(string="Crushing Load in kN")
    compressive_strength = fields.Float(string="Compressive Strength in N/mm2", compute="_compute_compressive_strength",digits=(12,2))

    @api.depends('length', 'width')
    def _compute_area(self):
        for record in self:
            record.area = record.length * record.width

    @api.depends('crushing_load', 'area')
    def _compute_compressive_strength(self):
        for record in self:
            if record.area != 0:
                record.compressive_strength = record.crushing_load / record.area * 1000
            else:
                record.compressive_strength = 0.0

    
    @api.model
    def create(self, vals):
        # Set the serial_no based on the existing records for the same parent
        if vals.get('parent_id'):
            existing_records = self.search([('parent_id', '=', vals['parent_id'])])
            if existing_records:
                max_serial_no = max(existing_records.mapped('sr_no'))
                vals['sr_no'] = max_serial_no + 1

        return super(ActCompressiveStrengthLine, self).create(vals)

    def _reorder_serial_numbers(self):
        # Reorder the serial numbers based on the positions of the records in child_lines
        records = self.sorted('id')
        for index, record in enumerate(records):
            record.sr_no = index + 1
