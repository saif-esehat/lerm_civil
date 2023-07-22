from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
import math

class SieveAnalysis(models.Model):
    _name = "mechanical.sieve.analysis"
    _inherit = "lerm.eln"
    _rec_name = "name"

    name = fields.Char("Name",default="Sieve Analysis")
    parameter_id = fields.Many2one('eln.parameters.result',string="Parameter")
    child_lines = fields.One2many('mechanical.sieve.analysis.line','parent_id',string="Parameter")
    total = fields.Integer(string="Total",compute="_compute_total")
    cumulative = fields.Float(string="Cumulative",compute="_compute_cumulative")
    

    @api.model
    def create(self, vals):
        record = super(SieveAnalysis, self).create(vals)
        record.parameter_id.write({'model_id': record.id})
        return record

    @api.depends('child_lines.wt_retained')
    def _compute_total(self):
        for record in self:
            print("recordd",record)
            record.total = sum(record.child_lines.mapped('wt_retained'))

    # @api.onchange('child_lines.wt_retained')
    # def _compute_cumulative(self):
    #     for record in self:
    #         record.total = sum(record.child_lines.mapped('wt_retained'))


    @api.onchange('total')
    def _onchange_total(self):
        for line in self.child_lines:
            line._compute_percent_retained()
            # line._compute_cumulative_retained()

class SieveAnalysisLine(models.Model):
    _name = "mechanical.sieve.analysis.line"
    parent_id = fields.Many2one('mechanical.sieve.analysis', string="Parent Id")
    
    serial_no = fields.Integer(string="Sr. No", readonly=True, copy=False, default=1)
    sieve_size = fields.Char(string="IS Sieve Size")
    wt_retained = fields.Float(string="Wt. Retained in gms")
    percent_retained = fields.Float(string='% Retained', compute="_compute_percent_retained")
    cumulative_retained = fields.Float(string="Cum. Retained %", compute="_compute_cumulative_retained", store=True)
    passing_percent = fields.Float(string="Passing %")

    @api.model
    def create(self, vals):
        # Set the serial_no based on the existing records for the same parent
        if vals.get('parent_id'):
            existing_records = self.search([('parent_id', '=', vals['parent_id'])])
            if existing_records:
                max_serial_no = max(existing_records.mapped('serial_no'))
                vals['serial_no'] = max_serial_no + 1

        return super(SieveAnalysisLine, self).create(vals)

    def _reorder_serial_numbers(self):
        # Reorder the serial numbers based on the positions of the records in child_lines
        records = self.sorted('id')
        for index, record in enumerate(records):
            record.serial_no = index + 1

    def write(self, vals):
        # Handle row deletions and adjust serial numbers
        if 'parent_id' in vals or 'wt_retained' in vals:
            for record in self:
                if record.parent_id and record.parent_id == vals.get('parent_id') and 'wt_retained' in vals:
                    record.percent_retained = vals['wt_retained'] / record.parent_id.total * 100 if record.parent_id.total else 0

            new_self = super(SieveAnalysisLine, self).write(vals)

            if 'wt_retained' in vals:
                for record in self:
                    record.parent_id._compute_total()

            return new_self

        return super(SieveAnalysisLine, self).write(vals)

    def unlink(self):
        # Get the parent_id before the deletion
        parent_id = self[0].parent_id

        res = super(SieveAnalysisLine, self).unlink()

        if parent_id:
            parent_id.child_lines._reorder_serial_numbers()

        return res


    @api.depends('wt_retained', 'parent_id.total')
    def _compute_percent_retained(self):
        for record in self:
            try:
                record.percent_retained = record.wt_retained / self.parent_id.total * 100
            except ZeroDivisionError:
                record.percent_retained = 0

    # @api.depends('passing_percent','parent_id.total')
    # def _compute_cumulative(self):
    #     for record in self:
    #         try:
    #             record.cumulative_retained = record.wt_retained / self.parent_id.total * 100
    #         except:
    #             record.cumulative_retained = 0



   

            
                


