from odoo import api, fields, models
from odoo.exceptions import UserError,ValidationError
from datetime import datetime , timedelta
import math



class WptMechanical(models.Model):
    _name = "mechanical.wpt"
    _inherit = "lerm.eln"
    _rec_name = "name"


    name = fields.Char("Name",default="Water Permeability Test")
    parameter_id = fields.Many2one('eln.parameters.result',string="Parameter")
    child_lines = fields.One2many('mechanical.wpt.line','parent_id',string="Parameter")
    temp_percent_wpt = fields.Float("Temperature °C")
    humidity_percent_wpt = fields.Float("Humidity %")
    start_date_wpt = fields.Date("Start Date")
    end_date_wpt = fields.Date("End Date")

    casting_date = fields.Date("Date of Casting",compute="_compute_casting_date")
    grade = fields.Many2one('lerm.grade.line',string="Grade",compute="_compute_grade_id",store=True)
    quantity = fields.Char("Quantity",compute="_compute_quantity")
    size = fields.Many2one('lerm.size.line',string="Specimen Size (mm)",compute="_compute_size",store=True)

    eln_ref = fields.Many2one('lerm.eln',string="Eln")

    @api.model
    def create(self, vals):
        # import wdb;wdb.set_trace()
        record = super(WptMechanical, self).create(vals)
        record.parameter_id.write({'model_id':record.id})
        record.eln_ref.write({'model_id':record.id})
        return record

    @api.depends('eln_ref')
    def _compute_size(self):
        if self.eln_ref:
            self.size = self.eln_ref.size_id.id

    @api.depends('eln_ref')
    def _compute_grade_id(self):
        if self.eln_ref:
            self.grade = self.eln_ref.grade_id.id

    @api.depends('eln_ref')
    def _compute_quantity(self):
        if self.eln_ref:
            self.quantity = self.eln_ref.sample_id.volume

    @api.depends('eln_ref')
    def _compute_casting_date(self):
        if self.eln_ref:
            self.casting_date = self.eln_ref.sample_id.date_casting


class WptMechanicalLine(models.Model):
    _name = "mechanical.wpt.line"
    parent_id = fields.Many2one('mechanical.wpt',string="Parent Id")

    sample = fields.Char("Sample")
    depth1 = fields.Float("Depth of Penetration 1")
    depth2 = fields.Float("Depth of Penetration 2")
    depth3 = fields.Float("Depth of Penetration 3")
    average = fields.Float("Average",compute="_compute_average")

    @api.depends('depth1','depth2','depth3')
    def _compute_average(self):
        for record in self:
            record.average = round(((record.depth1 + record.depth2 + record.depth3)/3),3)

