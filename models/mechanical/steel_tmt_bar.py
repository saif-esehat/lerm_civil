from odoo import api, fields, models
from odoo.exceptions import UserError,ValidationError
import math


class SteelTmtBarLine(models.Model):
    _name = "steel.tmt.bar"
    _inherit = "lerm.eln"
   
    
    Id_no = fields.Char("ID No")
    grade_id = fields.Char(string="Grade",compute="_compute_grade")
    diameter = fields.Integer(string="Dia. in mm")
    length = fields.Float(string="Length in mm",digits=(10, 3))
    weight = fields.Float(string="Weight, in kg",digits=(10, 3))
    weight_per_meter = fields.Float(string="Weight per meter, kg/m",compute="_compute_weight_per_meter",store=True)
    crossectional_area = fields.Float(string="Cross sectional Area, mm²",compute="_compute_crossectional_area",store=True)
    gauge_length = fields.Integer(string="Gauge Length, 5.65 √A, mm",compute="_compute_gauge_length",store=True)
    elongated_gauge_length = fields.Float(string="Elongated Gauge Length, mm")
    percent_elongation = fields.Float(string="% Elongation")
    yeild_load = fields.Float(string="Yield Load  KN")
    ultimate_load = fields.Float(string="Ultimate Load, Kn")
    proof_yeid_stress = fields.Float(string="0.2% Proof Stress / Yield Stress N/mm2",compute="_compute_proof_yeid_stress",store=True)
    ult_tens_strgth = fields.Float(string="Ultimate Tensile Strength, N/mm2",compute="_compute_ult_tens_strgth")
    fracture = fields.Char("Fracture (Within Gauge Length)",default="W.G.L")
    
    bend_test = fields.Selection([
        ('satisfactory', 'Satisfactory'),
        ('non-satisfactory', 'Non-Satisfactory')],"Bend Test")
    
    re_bend_test = fields.Selection([
        ('satisfactory', 'Satisfactory'),
        ('non-satisfactory', 'Non-Satisfactory')],"Re-Bend Test")

    eln_ref = fields.Many2one('lerm.eln',string="Eln ref")

    @api.depends('weight', 'length')
    def _compute_weight_per_meter(self):
        for record in self:
            if record.length != 0:
                record.weight_per_meter = record.weight / record.length
            else:
                record.weight_per_meter = 0.0

    @api.depends('weight', 'length')
    def _compute_crossectional_area(self):
        for record in self:
            if record.length != 0:
                record.crossectional_area = record.weight / (0.00785 * record.length)
            else:
                record.crossectional_area = 0.0

    @api.depends('crossectional_area')
    def _compute_gauge_length(self):
        for record in self:
            record.gauge_length = round(5.65 * math.sqrt(record.crossectional_area))


    @api.depends('yeild_load','crossectional_area')
    def _compute_proof_yeid_stress(self):
        for record in self:
            if record.crossectional_area != 0:
                record.proof_yeid_stress = record.yeild_load / record.crossectional_area * 1000
            else:
                record.proof_yeid_stress = 0.0

    @api.depends('ultimate_load')
    def _compute_ult_tens_strgth(self):
        for record in self:
            if record.crossectional_area != 0:
                record.ult_tens_strgth = record.ultimate_load / record.crossectional_area * 1000
            else:
                record.ult_tens_strgth = 0.0

    @api.depends('eln_ref')
    def _compute_grade(self):
        for record in self:
            grade = record.eln_ref.grade_id.id
            print("Grade",grade)
            record.grade_id = grade
  
          
   