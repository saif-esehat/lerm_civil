from odoo import api, fields, models

class Material(models.Model):
    _inherit = "product.template"

    is_sample = fields.Boolean(string="Is Sample?")
    casting_required = fields.Boolean(string="Casting Required")

    test_parameter = fields.Char("Test Column Title")
    results = fields.Char("Result Column Title")
    specifications = fields.Char("Specifications Column Title")
    unit = fields.Char("Unit Column Title")
    method_reference = fields.Char("Method Reference Column Title")
    result_remark = fields.Char("Results Remark Column Title")
    discipline = fields.Many2one('lerm_civil.discipline',string="Discipline")
    group = fields.Many2one('lerm_civil.group',string="Group")
    test_format_no = fields.Char(string="Test Format No")
    data_sheet_format_no = fields.Many2one('lerm.datasheet.master',string="Data Sheet Format No")
    group_ids = fields.Many2many('lerm_civil.group',string="Group Ids",compute="compute_group_ids")
    parameter_table = fields.One2many('lerm.parameter.line','parameter_id',string="Parameter")
    size_table = fields.One2many('lerm.size.line','product_id',string="Size")
    qty_table = fields.One2many('lerm.qty.line','product_id',string="Qty")
    grade_table = fields.One2many('lerm.grade.line','product_id',string="Grade")
    alias_table = fields.One2many('lerm.alias.line','product_id',string="Alias")

    @api.depends('discipline')
    def compute_group_ids(self):
        for record in self:
            # record.group = None
            group_ids = self.env['lerm_civil.group'].search([('discipline', '=', record.discipline.id)])
            record.group_ids = group_ids

class ParameterMasterAliasLine(models.Model):
    _name = 'lerm.alias.line'

    product_id = fields.Many2one('product.template',string="Parameter Id")
    alias = fields.Char(string="Alias")
    customer = fields.Many2one('res.partner',string="Customer")

class ParameterLine(models.Model):
    _name = 'lerm.parameter.line'

    parameter_id = fields.Many2one('product.template')
    parameter = fields.Char("Parameter")
    minimum = fields.Float("min")
    maximum = fields.Float("max")
    mu_value = fields.Float("MU Value")
    specification1 = fields.Char("Specification 1")
    specification2 = fields.Char("Specifications 2")
    unit = fields.Char("Unit")
    test_method = fields.Many2one('lerm_civil.test_method',string="Test Parameter")

class SizeLine(models.Model):
    _name = 'lerm.size.line'
    _rec_name = 'size'

    product_id = fields.Many2one('product.template')
    size = fields.Char("Size")


class QtyLine(models.Model):
    _name = 'lerm.qty.line'
    _rec_name = 'qty'

    product_id = fields.Many2one('product.template')
    qty = fields.Char("Qty")

class GradeLine(models.Model):
    _name = 'lerm.grade.line'
    _rec_name = 'grade'
    
    product_id = fields.Many2one('product.template')
    grade = fields.Char("Grade")