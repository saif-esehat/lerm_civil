from odoo import models, fields ,api

class ParameterMaster(models.Model):
    _name = 'lerm.parameter.master'
    _rec_name = 'parameter_name'

    parameter_name = fields.Char(string="Parameter Name")
    lab_min_value = fields.Float(string="Lab min Value")
    lab_max_value = fields.Float(string="Lab max Value")
    nabl_min_value = fields.Float(string="Nabl min value")
    nabl_max_value = fields.Float(string="Nabl max value")
    client_min_value = fields.Float(string="Client min Value")
    client_max_value = fields.Float(string="Client max Value")
    mu_value = fields.Float(string="Mu Value")
    unit = fields.Many2one('uom.uom',string="Unit")
    calculated = fields.Boolean("Calulated")
    test_method = fields.Many2one('lerm_civil.test_method',string="Test Method")
    discipline = fields.Many2one('lerm_civil.discipline',string="Discipline")
    nabl_select = fields.Selection([('nabl', 'NABL'), ('non_nabl', 'Non NABL')], string='NABL')
    spreadsheet_template = fields.Many2one("spreadsheet.template",string="Spreadsheet Template")
    sheets = fields.Char("Sheet Name")
    cell = fields.Char("Result Cell")
    group = fields.Many2one('lerm_civil.group',string="Group")
    dependent_inputs = fields.One2many("lerm.dependent.inputs","parameter_id",string="Inputs")
    formula = fields.Text("Formula")




class DependentInputs(models.Model):
    _name = 'lerm.dependent.inputs'
    _rec_name = 'label'
    parameter_id =  fields.Many2one('lerm.parameter.master',string="Parameters")
    identifier = fields.Char(string="Identifier")
    label = fields.Char(string="Label")


