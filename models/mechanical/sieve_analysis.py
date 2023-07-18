from odoo import api, fields, models
from odoo.exceptions import UserError,ValidationError
import math

class SieveAnalysis(models.Model):
    _name = "mechanical.sieve.analysis"
    _inherit = "lerm.eln"
    _rec_name = "name"

    name = fields.Char("Name",default="Sieve Analysis")
    parameter_id = fields.Many2one('eln.parameters.result',string="Parameter")
    child_lines = fields.One2many('mechanical.sieve.analysis.line','parent_id',string="Parameter")
    total = fields.Integer(string="Total",compute="_compute_total")

    @api.model
    def create(self, vals):
        # import wdb;wdb.set_trace()
        record = super(SieveAnalysis, self).create(vals)
        record.parameter_id.write({'model_id':record.id})
        return record

    @api.depends('child_lines.wt_retained')
    def _compute_total(self):
        for record in self:
            self.total = sum(record.child_lines.mapped('wt_retained'))

    @api.onchange('total')
    def _onchange_total(self):
        for line in self.child_lines:
            line._compute_percent_retained()
            line._compute_cumulative_retained()

class SieveAnalyisLine(models.Model):
    _name = "mechanical.sieve.analysis.line"
    parent_id = fields.Many2one('mechanical.sieve.analysis',string="Parent Id")
    
    sieve_size = fields.Char(string="IS Sieve Size")
    wt_retained = fields.Float(string="Wt. Retained in gms")
    percent_retained = fields.Float(string='% Retained', compute="_compute_percent_retained")
    cumulative_retained = fields.Float(string="Cum. Retained %" , compute="_compute_cum_retained")
    passing_percent = fields.Float(string="Passing %" , compute="_compute_passing_percent")
    total = fields.Integer(string='Total',compute='_compute_parent_value', store=True)

    

    @api.depends('parent_id.total')
    def _compute_parent_value(self):
        for record in self:
            record.total = record.parent_id.total



    @api.depends('wt_retained', 'total')
    def _compute_percent_retained(self):
        for record in self:
            try:
                record.percent_retained = record.wt_retained / record.total * 100
            except ZeroDivisionError:
                record.percent_retained = 0


    @api.depends('parent_id.child_lines.cumulative_retained')
    def _compute_cumulative_retained(self):
        sorted_lines = self.sorted(lambda r: r.id)
        cumulative_retained = 0.0
        for line in sorted_lines:
            line.cumulative_retained = cumulative_retained + line.percent_retained
            cumulative_retained = line.cumulative_retained
            
            
                


