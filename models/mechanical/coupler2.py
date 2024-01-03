from odoo import api, fields, models
from odoo.exceptions import UserError,ValidationError
import math
import re



class CouplerLine(models.Model):
    _name = "mechanical.coupler"
    _inherit = "lerm.eln"
   
    
    Id_no = fields.Char("ID No")
    grade = fields.Many2one('lerm.grade.line',string="Grade",compute="_compute_grade_id",store=True)
    size = fields.Many2one('lerm.size.line',string="Size",compute="_compute_size_id",store=True)
    diameter = fields.Integer(string="Outer Diameter")
    crossectional_area = fields.Float(string="Nominal Cross Sectional Area mm²",compute="_compute_crossectional_area")
    gauge_length = fields.Float(string="Gauge Length L, mm",store=True)
    elongated_gauge_length = fields.Float(string="Gauge Length  at Maximum Force, mm")
    ultimate_load = fields.Float(string="Ultimate Tensile Load, KN")
    # lentgh = fields.Float(string="Length in meter",digits=(10, 3))
    # weight = fields.Float(string="Weight, in kg",digits=(10, 3))
    # weight_per_meter = fields.Float(string="Weight per meter, kg/m",compute="_compute_weight_per_meter",store=True)
   
   
   
    # percent_elongation = fields.Float(string="% Elongation",compute="_compute_elongation_percent",store=True)
    # yeild_load = fields.Float(string="Yield Load  KN")
   
    # proof_yeid_stress = fields.Float(string="0.2% Proof Stress / Yield Stress N/mm2",compute="_compute_proof_yeid_stress",store=True)
    # ult_tens_strgth = fields.Float(string="Ultimate Tensile Strength, N/mm2",compute="_compute_ult_tens_strgth",store=True)
    # fracture = fields.Char("Fracture (Within Gauge Length)",default="W.G.L")
    eln_ref = fields.Many2one('lerm.eln',string="ELN")
    # ts_ys_ratio = fields.Float(string="TS/YS Ratio",compute="_compute_ts_ys_ratio",store=True)
    # weight_per_meter = fields.Float(string="Weight per meter",compute="_compute_weight_per_meter",store=True)
    # variation = fields.Float(string="Variation")

    # requirement_utl = fields.Float(string="Requirement",compute="_compute_requirement_utl",store=True)
    # requirement_yield = fields.Float(string="Requirement",compute="_compute_requirement_yield",store=True)
    # requirement_ts_ys = fields.Float(string="Requirement",compute="_compute_requirement_ts_ys",store=True)
    # requirement_elongation = fields.Float(string="Requirement",compute="_compute_requirement_elongation",store=True)
    # requirement_weight_per_meter = fields.Float(string="Requirement",compute="_compute_requirement_weight_per_meter",digits=(16, 4),store=True)

    sample_parameters = fields.Many2many('lerm.parameter.master',string="Parameters",compute="_compute_sample_parameters",store=True)
    tests = fields.Many2many("mechanical.tmt.test",string="Tests")
    # fracture_visible = fields.Boolean("Fracture visible",compute="_compute_visible",store=True)
    # bend_visible = fields.Boolean("Bend visible",compute="_compute_visible",store=True)
    # rebend_visible = fields.Boolean("Rebend visible",compute="_compute_visible",store=True)
    # bend_test_text = fields.Char(string="Bend Test Text", compute="_compute_bend_test_text", store=True)


    
    bend_test = fields.Selection([
        ('satisfactory', 'Satisfactory'),
        ('non-satisfactory', 'Non-Satisfactory')],"Bend Test",store=True)
    
    re_bend_test = fields.Selection([
        ('satisfactory', 'Satisfactory'),
        ('non-satisfactory', 'Non-Satisfactory')],"Re-Bend Test",store=True)
    
      

    # @api.depends('bend_test')
    # def _compute_bend_test_text(self):
    #     for record in self:
    #         if record.bend_test == '1':
    #             record.bend_test_text = 'Satisfactory'
    #         elif record.bend_test == '2':
    #             record.bend_test_text = 'Non-Satisfactory'
    #         else:
    #             record.bend_test_text = 'Undefined'
    


    uts_conformity = fields.Selection([
        ('pass', 'Pass'),
        ('fail', 'Fail')],string="Conformity",compute="_compute_uts_conformity",store=True)

    yield_conformity = fields.Selection([
        ('pass', 'Pass'),
        ('fail', 'Fail')],string="Conformity",compute="_compute_yield_conformity",store=True)

    elongation_conformity = fields.Selection([
        ('pass', 'Pass'),
        ('fail', 'Fail')],string="Conformity",compute="_compute_elongation_conformity",store=True)

    ts_ys_conformity = fields.Selection([
        ('pass', 'Pass'),
        ('fail', 'Fail')],string="Conformity",compute="_compute_ts_ys_conformity",store=True)

    weight_per_meter_conformity = fields.Selection([
        ('pass', 'Pass'),
        ('fail', 'Fail')],string="Conformity",compute="_compute_weight_per_meter_conformity",store=True)

    fracture_visible = fields.Boolean("Fracture",compute="_compute_visible")
    bend_visible = fields.Boolean("Bend Test",compute="_compute_visible")
    rebend_visible = fields.Boolean("Rebend Test",compute="_compute_visible")

    uts_nabl = fields.Selection([
        ('pass', 'Pass'),
        ('fail', 'Fail')],string="NABL",compute="_compute_uts_nabl",store=True)

    yield_nabl = fields.Selection([
        ('pass', 'Pass'),
        ('fail', 'Fail')],string="NABL",compute="_compute_yield_nabl",store=True)

    elongation_nabl = fields.Selection([
        ('pass', 'Pass'),
        ('fail', 'Fail')],string="NABL",compute="_compute_elongation_nabl",store=True)

    ts_ys_nabl = fields.Selection([
        ('pass', 'Pass'),
        ('fail', 'Fail')],string="NABL",compute="_compute_ts_ys_nabl",store=True)
    
    

    weight_per_meter_nabl = fields.Selection([
        ('pass', 'Pass'),
        ('fail', 'Fail')],string="NABL",compute="_compute_weight_per_meter_nabl",store=True)

    

    @api.depends('eln_ref','sample_parameters')
    def _compute_visible(self):
        for record in self:
            record.fracture_visible = False
            record.bend_visible  = False  
            record.rebend_visible = False
            for sample in record.sample_parameters:
                print("Samples internal id",sample.internal_id)
                if sample.internal_id == 'c3b7e054-bafc-40bf-82ad-82063feabfb8':
                    record.fracture_visible = True
                if sample.internal_id == 'dceffc67-d195-4991-8e28-e35eb27ecc34':
                    record.bend_visible = True
                if sample.internal_id == 'd898fa49-9d66-47c7-a311-7746433408f3':
                    record.rebend_visible = True

    fracture_visible = fields.Boolean("Fracture",compute="_compute_visible")
    bend_visible = fields.Boolean("Bend Test",compute="_compute_visible")
    rebend_visible = fields.Boolean("Rebend Test",compute="_compute_visible")

    @api.depends('eln_ref','sample_parameters')
    def _compute_visible(self):
        for record in self:
            record.fracture_visible = False
            record.bend_visible  = False  
            record.rebend_visible = False
            for sample in record.sample_parameters:
                print("Samples internal id",sample.internal_id)
                if sample.internal_id == 'c3b7e054-bafc-40bf-82ad-82063feabfb8':
                    record.fracture_visible = True
                if sample.internal_id == 'dceffc67-d195-4991-8e28-e35eb27ecc34':
                    record.bend_visible = True
                if sample.internal_id == 'd898fa49-9d66-47c7-a311-7746433408f3':
                    record.rebend_visible = True

    @api.depends('diameter')
    def _compute_crossectional_area(self):
        for record in self:
            if record.diameter:
                record.crossectional_area = 3.14 * (record.diameter ** 2) / 4
            else:
                record.crossectional_area = 0.0

   
  

    @api.model
    def create(self, vals):
        # import wdb;wdb.set_trace()
        record = super(CouplerLine, self).create(vals)
        # record.get_all_fields()
        record.eln_ref.write({'model_id':record.id})
        return record


    @api.depends('eln_ref')
    def _compute_grade_id(self):
        if self.eln_ref:
            self.grade = self.eln_ref.grade_id.id
    

    @api.depends('eln_ref')
    def _compute_size_id(self):
        if self.eln_ref:
            self.size = self.eln_ref.size_id.id

    # @api.depends('eln_ref')
    # def _compute_dia(self):
    #     for record in self:
    #         pattern = r'\d+'
    #         match = re.search(pattern, str(record.eln_ref.size_id.size))
    #         if match:
    #             dia = int(match.group())
    #             record.diameter = int(match.group())
    #         else:
    #             record.diameter = 0
                 


    

    


    # @api.depends('tests')
    # def _compute_visible(self):
    #     fracture_test = self.env['mechanical.tmt.test'].search([('name', '=', 'Fracture')])
    #     bend_test = self.env['mechanical.tmt.test'].search([('name', '=', 'Bend Test')])
    #     rebend_test = self.env['mechanical.tmt.test'].search([('name', '=', 'Rebend Test')])


    #     for record in self:
    #         record.fracture_visible = False
    #         record.bend_visible  = False  
    #         record.rebend_visible = False
            
    #         if fracture_test in record.tests:
    #             record.fracture_visible = True
    #         if bend_test in record.tests:
    #             record.bend_visible = True
    #         if rebend_test in record.tests:
    #             record.rebend_visible = True

    @api.depends('eln_ref')
    def _compute_sample_parameters(self):
        for record in self:
            records = record.eln_ref.parameters_result.parameter.ids
            record.sample_parameters = records
            print("Records",records)
            



# class MechanicalTmtTest(models.Model):
#     _name = "mechanical.tmt.test"
#     _rec_name = "name"
#     name = fields.Char("Name")