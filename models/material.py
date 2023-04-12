from odoo import api, fields, models

class Material(models.Model):
    _inherit = "product.template"

    is_sample = fields.Boolean(string="Is Sample?")

    test_parameter = fields.Char("Test Parameters")
    results = fields.Char("Results")
    specifications = fields.Char("Specifications")
    unit = fields.Char("Unit")
    method_reference = fields.Char("Method Reference")
    result_remark = fields.Char("Results Remark")
    discipline = fields.Many2one('lerm_civil.discipline',string="Discipline")
    group = fields.Many2one('lerm_civil.group',string="Group")
    test_format_no = fields.Char(string="Test Format No")
    data_sheet_format_no = fields.Char(string="Data Sheet Format No")

    parameter_table = fields.One2many('lerm.parameter.line','parameter_id',string="Parameter")
    size_table = fields.One2many('lerm.size.line','size_id',string="Size")
    qty_table = fields.One2many('lerm.qty.line','qty_id',string="Qty")
    grade_table = fields.One2many('lerm.grade.line','grade_id',string="Grade")



class ParameterLine(models.Model):
    _name = 'lerm.parameter.line'

    parameter_id = fields.Many2one('product.template')
    parameter = fields.Char("Parameter")
    minimum = fields.Integer("min")
    maximum = fields.Integer("max")
    specification1 = fields.Char("Specification 1")
    specification2 = fields.Char("Specifications 2")
    unit = fields.Char("Unit")
    test_method = fields.Char("Test Method")

class SizeLine(models.Model):
    _name = 'lerm.size.line'

    size_id = fields.Many2one('product.template')
    size = fields.Char("Size")


class QtyLine(models.Model):
    _name = 'lerm.qty.line'

    qty_id = fields.Many2one('product.template')
    qty = fields.Char("Qty")

class GradeLine(models.Model):
    _name = 'lerm.grade.line'

    grade_id = fields.Many2one('product.template')
    grade = fields.Char("Grade")