from odoo import api, fields, models
from odoo.exceptions import UserError,ValidationError
import math

class ChemicalGyspum(models.Model):
    _name = "chemical.gyspum"
    _inherit = "lerm.eln"
    _rec_name = "name"

    name = fields.Char("Name",default="Gyspum")
    parameter_id = fields.Many2one('eln.parameters.result',string="Parameter")
    sample_parameters = fields.Many2many('lerm.parameter.master',string="Parameters",compute="_compute_sample_parameters",store=True)
    eln_ref = fields.Many2one('lerm.eln',string="Eln")
    grade = fields.Many2one('lerm.grade.line',string="Grade",compute="_compute_grade_id",store=True)


    # %Sulphur trioxide (SO3)
    so3_name = fields.Char("Name", default="SO3")
    so3_visible = fields.Boolean("SO3", compute="_compute_visible")

    plaster1 = fields.Char(string="Plaster Of Paris",default="35 Min")
    retarded1 = fields.Char(string="Retarded Hemihydrate Gypsum Plaster",default="35 Min")
    anhydrous1 = fields.Char(string="Anhydrous Gypsum Plaster",default="40 Min")
    keenes1 = fields.Char(string="Keene's Plaster",default="47 Min")

    wt_of_sample_so3 = fields.Float("A) Wt of Sample (gm)")
    wt_cr_so3 = fields.Float("B) Wt of crucible +Residue after ignition (gm)")
    wt_empty_co3 = fields.Float("C) Wt of empty crucible (gm)")
    difference_co3 = fields.Float("D)Diff. in weight(gm)=( B - C )",compute="_compute_difference_co3",digits=(12,4))
    so3 = fields.Float("SO3  % =  D x 34.30  / A",compute="_compute_so3",digits=(12,3))

    @api.depends('wt_cr_so3', 'wt_empty_co3')
    def _compute_difference_co3(self):
        for record in self:
            record.difference_co3 = record.wt_cr_so3 - record.wt_empty_co3

    @api.depends('difference_co3', 'wt_of_sample_so3')
    def _compute_so3(self):
        for record in self:
              if self.wt_of_sample_so3 != 0:
                 self.so3 = self.difference_co3 * 34.30 / self.wt_of_sample_so3
              else:
                self.so3 = 0.0
  
          

   


    so3_conformity = fields.Selection([
            ('pass', 'Pass'),
            ('fail', 'Fail')], string="Conformity", compute="_compute_so3_conformity", store=True)

    @api.depends('so3','eln_ref','grade')
    def _compute_so3_conformity(self):
        
        for record in self:
            record.so3_conformity = 'fail'
            line = self.env['lerm.parameter.master'].search([('internal_id','=','a58cb5bc-d2d2-4756-81d2-6571ae81a813')])
            materials = self.env['lerm.parameter.master'].search([('internal_id','=','a58cb5bc-d2d2-4756-81d2-6571ae81a813')]).parameter_table
            for material in materials:
                if material.grade.id == record.grade.id:
                    req_min = material.req_min
                    req_max = material.req_max
                    mu_value = line.mu_value
                    
                    lower = record.so3 - record.so3*mu_value
                    upper = record.so3 + record.so3*mu_value
                    if lower >= req_min and upper <= req_max:
                        record.so3_conformity = 'pass'
                        break
                    else:
                        record.so3_conformity = 'fail'

    so3_nabl = fields.Selection([
        ('pass', 'NABL'),
        ('fail', 'Non-NABL')], string="NABL", compute="_compute_so3_nabl", store=True)

    @api.depends('so3','eln_ref','grade')
    def _compute_so3_nabl(self):
        
        for record in self:
            record.so3_nabl = 'fail'
            line = self.env['lerm.parameter.master'].search([('internal_id','=','a58cb5bc-d2d2-4756-81d2-6571ae81a813')])
            materials = self.env['lerm.parameter.master'].search([('internal_id','=','a58cb5bc-d2d2-4756-81d2-6571ae81a813')]).parameter_table
            for material in materials:
                if material.grade.id == record.grade.id:
                    lab_min = line.lab_min_value
                    lab_max = line.lab_max_value
                    mu_value = line.mu_value
                    
                    lower = record.so3 - record.so3*mu_value
                    upper = record.so3 + record.so3*mu_value
                    if lower >= lab_min and upper <= lab_max:
                        record.so3_nabl = 'pass'
                        break
                    else:
                        record.so3_nabl = 'fail'


    @api.depends('sample_parameters')
    def _compute_visible(self):
        for record in self:
            record.so3_visible = False
         
           
            for sample in record.sample_parameters:
                print("Samples internal id",sample.internal_id)
                if sample.internal_id == 'a58cb5bc-d2d2-4756-81d2-6571ae81a813':
                    record.so3_visible = True

   
               

    
          

    @api.model
    def create(self, vals):
        # import wdb;wdb.set_trace()
        record = super(ChemicalGyspum, self).create(vals)
        record.get_all_fields()
        record.eln_ref.write({'model_id':record.id})
        return record


        
    def get_all_fields(self):
        record = self.env['chemical.gyspum'].browse(self.ids[0])
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
    

