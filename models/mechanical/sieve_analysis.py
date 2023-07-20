from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
import math

class SieveAnalysis(models.Model):
    _name = "mechanical.sieve.analysis"
    _inherit = "lerm.eln"
    _rec_name = "name"

    name = fields.Char("Name", default="Sieve Analysis")
    parameter_id = fields.Many2one('eln.parameters.result', string="Parameter")
    child_lines = fields.One2many('mechanical.sieve.analysis.line', 'parent_id', string="Parameter")
    total = fields.Integer(string="Total", compute="_compute_total")
    cumulative = fields.Float(string="Cumulative")

    @api.model
    def create(self, vals):
        record = super(SieveAnalysis, self).create(vals)
        record.parameter_id.write({'model_id': record.id})
        return record

    @api.depends('child_lines.wt_retained')
    def _compute_total(self):
        for record in self:
            record.total = sum(record.child_lines.mapped('wt_retained'))

    @api.onchange('total')
    def _compute_cumulative(self):
        last_cumulative = False
        if self.child_lines:
            last_record = self.child_lines[-1]
            last_cumulative = last_record.cumulative_retained
            self.cumulative = last_cumulative
        print("Last cumulative value:", last_cumulative)

    @api.onchange('total')
    def _onchange_total(self):
        for line in self.child_lines:
            line._compute_percent_retained()
            line._compute_cumulative_retained()

class SieveAnalysisLine(models.Model):
    _name = "mechanical.sieve.analysis.line"
    parent_id = fields.Many2one('mechanical.sieve.analysis', string="Parent Id")
    
    sieve_size = fields.Char(string="IS Sieve Size")
    wt_retained = fields.Float(string="Wt. Retained in gms")
    percent_retained = fields.Float(string='% Retained', compute="_compute_percent_retained")
    cumulative_retained = fields.Float(string="Cum. Retained %", compute="_compute_cumulative_retained", store=True)
    passing_percent = fields.Float(string="Passing %", compute="_compute_passing_percent")
    total = fields.Integer(string='Total', compute='_compute_parent_value', store=True)

    @api.depends('parent_id.total')
    def _compute_parent_value(self):
        for record in self:
            record.total = record.parent_id.total

    @api.depends('wt_retained', 'parent_id.cumulative')
    def _compute_cumulative_retained(self):
        for record in self:
            record.cumulative_retained = 0
            # record.get_previous_record()
            

    

    def get_previous_record(self):
        sorted_children = self.parent_id.child_lines.sorted(key=lambda r: r.id)
        # current_index = sorted_children.index(self)
        print("sorted",sorted_children)
        # print("current",current_index)


        # if current_index > 0:
        #     previous_record = sorted_children[current_index - 1]
        #     print("previous",previous_record)           
        #     return previous_record

        # return False


    @api.depends('wt_retained', 'total')
    def _compute_percent_retained(self):
        for record in self:
            try:
                record.percent_retained = record.wt_retained / record.total * 100
            except ZeroDivisionError:
                record.percent_retained = 0
