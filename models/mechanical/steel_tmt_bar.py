from odoo import api, fields, models
from odoo.exceptions import UserError,ValidationError
import math


class SteelTmtBarLine(models.Model):
    _name = "steel.tmt.bar"
   
   
    
    Id_no = fields.Char("ID No")
    grade = fields.Many2one('lerm.grade.line',string="Grade",compute="_compute_grade_id")
    diameter = fields.Integer(string="Dia. in mm")
    lentgh = fields.Float(string="Length in mm",digits=(10, 3))
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
    eln_ref = fields.Many2one('lerm.eln',string="ELN")
    requirment = fields.Char(string="Requirment")
    
    bend_test = fields.Selection([
        ('satisfactory', 'Satisfactory'),
        ('non-satisfactory', 'Non-Satisfactory')],"Bend Test")
    
    re_bend_test = fields.Selection([
        ('satisfactory', 'Satisfactory'),
        ('non-satisfactory', 'Non-Satisfactory')],"Re-Bend Test")

    @api.depends('weight', 'lentgh')
    def _compute_weight_per_meter(self):
        for record in self:
            if record.lentgh != 0:
                record.weight_per_meter = record.weight / record.lentgh
            else:
                record.weight_per_meter = 0.0

    @api.depends('weight', 'lentgh')
    def _compute_crossectional_area(self):
        for record in self:
            if record.lentgh != 0:
                record.crossectional_area = record.weight / (0.00785 * record.lentgh)
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

    @api.model
    def create(self, vals):
        # import wdb;wdb.set_trace()
        record = super(SteelTmtBarLine, self).create(vals)
        # record.get_all_fields()
        record.eln_ref.write({'model_id':record.id})
        return record


    @api.depends('eln_ref')
    def _compute_grade_id(self):
        if self.eln_ref:
            self.grade = self.eln_ref.grade_id.id

    


  
          