from odoo import api, fields, models
from odoo.exceptions import UserError,ValidationError
import math

class Upv(models.Model):
    _name = "ndt.upv"
    _inherit = "lerm.eln"
    _rec_name = "name"

    name = fields.Char("Name",default="UPV")
    structure_age = fields.Char("Approximate Age of structure  Years")
    site_temp = fields.Char("Site Temp")
    concrete_grade = fields.Char("Concrete Grade")
    instrument = fields.Char("Instrument")
    structure = fields.Char("Structure")
    parameter_id = fields.Many2one('eln.parameters.result', string="Parameter")
    child_lines = fields.One2many('ndt.upv.line', 'parent_id', string="Parameter")
    average = fields.Float("Average", compute="_compute_velocity_stats")
    min = fields.Float("Min", compute="_compute_velocity_stats")
    max = fields.Float("Max", compute="_compute_velocity_stats")

    @api.depends('child_lines.velocity')
    def _compute_velocity_stats(self):
        for record in self:
            velocities = record.child_lines.mapped('velocity')
            if velocities:
                record.average = sum(velocities) / len(velocities)
                record.min = min(velocities)
                record.max = max(velocities)
            else:
                record.average = 0.0
                record.min = 0.0
                record.max = 0.0



    @api.model
    def create(self, vals):
        # import wdb;wdb.set_trace()
        record = super(Upv, self).create(vals)
        record.parameter_id.write({'model_id':record.id})
        return record


class UpvLine(models.Model):
    _name = "ndt.upv.line"
    parent_id = fields.Many2one('ndt.upv',string="Parent Id")
    element_type = fields.Char("Element Type")
    level_id = fields.Char("Level ID")
    dist = fields.Float("Dist. (mm)")
    time = fields.Float("Time. (μs)")
    velocity = fields.Float("Velocity(km/sec)",compute="_compute_velocity")
    condition_concrete = fields.Selection([
        ('dry', 'Dry'),
        ('wet', 'Wet')],"Condition Of Concrete")
    surface = fields.Selection([
        ('on_plaster', 'On Plaster'),
        ('wo_plaster', 'W/O Plaster')],"Surface")
    quality = fields.Selection([
        ('excellent','Excellent'),
        ('good','Good'),
        ('medium','Medium'),
        ('doubtful','Doubtful')
    ],"Quality",compute="_compute_quality")
    method = fields.Selection([
        ('direct', 'Direct'),
        ('indirect', 'In-Direct'),
        ('semi_direct', 'Semi-Direct')],"Method")
    

    @api.depends('velocity')
    def _compute_quality(self):
        for record in self:
            if record.velocity > 4.5:
                record.quality = 'excellent'
            elif 3.5 <= record.velocity <= 4.5:
                record.quality = 'good'
            elif 3.0 <= record.velocity < 3.5:
                record.quality = 'medium'
            else:
                record.quality = 'doubtful'
    
    
    @api.depends('dist', 'time')
    def _compute_velocity(self):
        for record in self:
            if record.dist and record.time:
                velocity = (record.dist / record.time) * 1000  # Convert time from μs to seconds
                record.velocity = velocity
            else:
                record.velocity = 0.0