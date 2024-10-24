from odoo import api, fields, models
from odoo.exceptions import UserError,ValidationError
import math


class WireMesh(models.Model):
    _name = "chemical.wire.mesh"
    _inherit = "lerm.eln"
    _rec_name = "name"

    name = fields.Char("Name",default="WIRE MESH")
    parameter_id = fields.Many2one('eln.parameters.result',string="Parameter")
    sample_parameters = fields.Many2many('lerm.parameter.master',string="Parameters",compute="_compute_sample_parameters",store=True)
    eln_ref = fields.Many2one('lerm.eln',string="Eln")
    grade = fields.Many2one('lerm.grade.line',string="Grade",compute="_compute_grade_id",store=True)



    # Sulphur ( IS 228 part 9 )		
    sulphur_name = fields.Char("Name",default="Sulphur ( IS 228 part 9 )")
    sulphur_visible = fields.Boolean("Sulphur",compute="_compute_visible")

    sulphur_vl_po = fields.Float("A) volume, in ml, of potassium iodate  added	")
    sulphur_vl_un = fields.Float("B) volume, in ml, of potassium iodate  unused")
    sulphur_no = fields.Float("C)normality of Sodium thiosulphate")
    sulphur_mass = fields.Float("D)mass, in g, of sample taken")
    sulphur = fields.Float("% Sulphur =B-A x C*1.6 /D",compute="_compute_sulphur",digits=(12,3))


    @api.depends('sulphur_vl_po', 'sulphur_vl_un', 'sulphur_no', 'sulphur_mass')
    def _compute_sulphur(self):
        for record in self:
            if record.sulphur_mass != 0:
                record.sulphur = ((record.sulphur_vl_po - record.sulphur_vl_un) * record.sulphur_no * 1.6) / record.sulphur_mass
            else:
                record.sulphur = 0


    sulphur_conformity = fields.Selection([
            ('pass', 'Pass'),
            ('fail', 'Fail')], string="Conformity",compute="_compute_sulphur_conformity", store=True)


    @api.depends('sulphur','eln_ref','grade')
    def _compute_sulphur_conformity(self):
        
        for record in self:
            record.sulphur_conformity = 'fail'
            line = self.env['lerm.parameter.master'].sudo().search([('internal_id','=','7e9f55f6-24f1-4a9d-887a-3e6eabd84a15')])
            materials = self.env['lerm.parameter.master'].sudo().search([('internal_id','=','7e9f55f6-24f1-4a9d-887a-3e6eabd84a15')]).parameter_table
            for material in materials:
                if material.grade.id == record.grade.id:
                    req_min = material.req_min
                    req_max = material.req_max
                    mu_value = line.mu_value
                    
                    lower = record.sulphur - record.sulphur*mu_value
                    upper = record.sulphur + record.sulphur*mu_value
                    if lower >= req_min and upper <= req_max:
                        record.sulphur_conformity = 'pass'
                        break
                    else:
                        record.sulphur_conformity = 'fail'


    sulphur_nabl = fields.Selection([
        ('pass', 'NABL'),
        ('fail', 'Non-NABL')], string="NABL",compute="_compute_sulphur_nabl", store=True)


    @api.depends('sulphur','eln_ref','grade')
    def _compute_sulphur_nabl(self):
        
        for record in self:
            record.sulphur_nabl = 'fail'
            line = self.env['lerm.parameter.master'].sudo().search([('internal_id','=','7e9f55f6-24f1-4a9d-887a-3e6eabd84a15')])
            materials = self.env['lerm.parameter.master'].sudo().search([('internal_id','=','7e9f55f6-24f1-4a9d-887a-3e6eabd84a15')]).parameter_table
            for material in materials:
                if material.grade.id == record.grade.id:
                    lab_min = line.lab_min_value
                    lab_max = line.lab_max_value
                    mu_value = line.mu_value
                    
                    lower = record.sulphur - record.sulphur*mu_value
                    upper = record.sulphur + record.sulphur*mu_value
                    if lower >= lab_min and upper <= lab_max:
                        record.sulphur_nabl = 'pass'
                        break
                    else:
                        record.sulphur_nabl = 'fail'



    # Phosphorous(IS : 228 part 3)		
    phosphorous_name = fields.Char("Name",default="Phosphorous(IS : 228 part 3)")
    phosphorous_visible = fields.Boolean("Phosphorous",compute="_compute_visible")

    phosphorous_sample = fields.Float("A)Wt of Sample taken (gm)")
    phosphorous_bu = fields.Float("B)Burette reading of 0.1N. NaOH Added (ml)")
    phosphorous_re = fields.Float("C)Burette reading of 0.1N. HNO3 Required (ml) for sample.")
    phosphorous_blank = fields.Float("D)Blank Reading in ml")
    phosphorous_diff = fields.Float("E)Difference = (D - C ) ml",compute="_compute_phosphorous_diff",digits=(12,4))
    phosphorous_no = fields.Float("F)Normality of  0.1N. HNO3")
    phosphorous = fields.Float("% P=E x F x  0.001354 x100 / wt of sample",compute="_compute_phosphorous",digits=(12,3))


    @api.depends('phosphorous_blank', 'phosphorous_re')
    def _compute_phosphorous_diff(self):
        for record in self:
            record.phosphorous_diff = record.phosphorous_blank - record.phosphorous_re


    @api.depends('phosphorous_diff', 'phosphorous_no', 'phosphorous_sample')
    def _compute_phosphorous(self):
        for record in self:
            if record.phosphorous_sample != 0:
                record.phosphorous = (record.phosphorous_diff * record.phosphorous_no * 0.001354 * 100) / record.phosphorous_sample
            else:
                record.phosphorous = 0


    phosphorous_conformity = fields.Selection([
            ('pass', 'Pass'),
            ('fail', 'Fail')], string="Conformity",compute="_compute_phosphorous_conformity", store=True)

    
    @api.depends('phosphorous','eln_ref','grade')
    def _compute_phosphorous_conformity(self):
        
        for record in self:
            record.phosphorous_conformity = 'fail'
            line = self.env['lerm.parameter.master'].sudo().search([('internal_id','=','3f9984cd-7716-4342-abf7-ae3b821baf0f')])
            materials = self.env['lerm.parameter.master'].sudo().search([('internal_id','=','3f9984cd-7716-4342-abf7-ae3b821baf0f')]).parameter_table
            for material in materials:
                if material.grade.id == record.grade.id:
                    req_min = material.req_min
                    req_max = material.req_max
                    mu_value = line.mu_value
                    
                    lower = record.phosphorous - record.phosphorous*mu_value
                    upper = record.phosphorous + record.phosphorous*mu_value
                    if lower >= req_min and upper <= req_max:
                        record.phosphorous_conformity = 'pass'
                        break
                    else:
                        record.phosphorous_conformity = 'fail'



    phosphorous_nabl = fields.Selection([
        ('pass', 'NABL'),
        ('fail', 'Non-NABL')], string="NABL",compute="_compute_phosphorous_nabl", store=True)


    @api.depends('phosphorous','eln_ref','grade')
    def _compute_phosphorous_nabl(self):
        
        for record in self:
            record.phosphorous_nabl = 'fail'
            line = self.env['lerm.parameter.master'].sudo().search([('internal_id','=','3f9984cd-7716-4342-abf7-ae3b821baf0f')])
            materials = self.env['lerm.parameter.master'].sudo().search([('internal_id','=','3f9984cd-7716-4342-abf7-ae3b821baf0f')]).parameter_table
            for material in materials:
                if material.grade.id == record.grade.id:
                    lab_min = line.lab_min_value
                    lab_max = line.lab_max_value
                    mu_value = line.mu_value
                    
                    lower = record.phosphorous - record.phosphorous*mu_value
                    upper = record.phosphorous + record.phosphorous*mu_value
                    if lower >= lab_min and upper <= lab_max:
                        record.phosphorous_nabl = 'pass'
                        break
                    else:
                        record.phosphorous_nabl = 'fail'


    
    @api.depends('sample_parameters')
    def _compute_visible(self):
        for record in self:
            record.sulphur_visible = False
            record.phosphorous_visible = False


            for sample in record.sample_parameters:
                print("Samples internal id",sample.internal_id)
                if sample.internal_id == '7e9f55f6-24f1-4a9d-887a-3e6eabd84a15':
                    record.sulphur_visible = True
                if sample.internal_id == '3f9984cd-7716-4342-abf7-ae3b821baf0f':
                    record.phosphorous_visible = True



    @api.model
    def create(self, vals):
        # import wdb;wdb.set_trace()
        record = super(WireMesh, self).create(vals)
        # record.get_all_fields()
        record.eln_ref.write({'model_id':record.id})
        return record


    def get_all_fields(self):
        record = self.env['chemical.wire.mesh'].browse(self.ids[0])
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


    @api.depends('eln_ref')
    def _compute_grade_id(self):
        if self.eln_ref:
            self.grade = self.eln_ref.grade_id.id


