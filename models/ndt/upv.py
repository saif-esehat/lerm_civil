from odoo import api, fields, models
from odoo.exceptions import UserError,ValidationError
import math
import re


class Upv(models.Model):
    _name = "ndt.upv"
    _inherit = "lerm.eln"
    _rec_name = "name"


    eln_ref = fields.Many2one("lerm.eln")
    name = fields.Char("Name",default="UPV")
    
    structure_age = fields.Char("Approximate Age of structure  Years")
    site_temp = fields.Float("Concrete Temp °C",required=True)
    concrete_grade = fields.Char("Concrete Grade")
    instrument = fields.Char("Instrument")
    structure = fields.Char("Structure")
    grade_id = fields.Many2one('lerm.grade.line',compute="_compute_grade", string="Grade")
    parameter_id = fields.Many2one('eln.parameters.result', string="Parameter")
    child_lines = fields.One2many('ndt.upv.line', 'parent_id', string="Parameter")
    average = fields.Float("Average km/s", compute="_compute_velocity_stats",digits=(16,2))
    min = fields.Float("Min km/s", compute="_compute_velocity_stats",digits=(16,2))
    max = fields.Float("Max km/s", compute="_compute_velocity_stats",digits=(16,2))

    notes = fields.One2many('ndt.upv.notes','parent_id',string="Notes")

    @api.depends('eln_ref')
    def _compute_grade(self):
        for record in self:
            record.grade_id = record.eln_ref.grade_id.id

    @api.depends('child_lines.velocity')
    def _compute_velocity_stats(self):
        for record in self:
            velocities = record.child_lines.mapped('velocity')
            if velocities:
                record.average = sum(velocities) / len(velocities)
                minimum = round(min(velocities),2)
                record.min = minimum
                maximum = round(max(velocities),2)
                record.max = maximum
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
    level_id = fields.Char("Location")
    dist = fields.Float("Dist. (m)",digits=(16,2))
    time = fields.Float("Time. (μs)",digits=(16,2))
    velocity = fields.Float("Velocity(km/sec)",compute="_compute_velocity",digits=(16,2))
    condition_concrete = fields.Selection([
        ('dry', 'Dry'),
        ('wet', 'Wet')],"Condition Of Concrete")
    
    surface = fields.Selection([
        ('w/o_plaster', 'W/O Plaster')],"Surface",default='w/o_plaster')
    
    quality = fields.Selection([
        ('excellent','Excellent'),
        ('good','Good'),
        ('medium','Medium'),
        ('doubtful','Doubtful')
    ],"Quality",compute="_compute_quality")

    method = fields.Selection([
        ('direct', 'Direct'),
        ('indirect', 'In-Direct'),
        ('Semi_direct', 'Semi-Direct')],"Method")
    
    @api.depends('velocity')
    def _compute_quality(self):
        for record in self:
            # import wdb; wdb.set_trace() 
            string1 = "M25"
            string2 = self.parent_id.grade_id.grade

            numeric_part1 = self.extract_number_from_string(string1)
            numeric_part2 = self.extract_number_from_string(string2)

            # self.extract_numeric_part(string1)
            if record.velocity > 4.5:
                record.quality = 'excellent'
            elif numeric_part1 > numeric_part2 and 3.5 <= record.velocity <= 4.5:
                record.quality = 'good'
            elif numeric_part1 < numeric_part2 and 3.75 <= record.velocity <= 4.5:
                record.quality = 'good'
            else:
                record.quality = 'doubtful'
    
    def extract_number_from_string(self,string):
        pattern = r'\d+'  # Regular expression pattern to match one or more digits
        match = re.search(pattern, string)
        if match:
            return int(match.group())  # Convert the matched substring to an integer
        else:
            return None  # 
    
    # def extract_numeric_part(s):
    #     numeric_part = ''.join(filter(str.isdigit, s))
    #     return int(numeric_part) if numeric_part else 0
    
    
    @api.depends('dist', 'time','method','parent_id')
    def _compute_velocity(self):
        for record in self:
            # import wdb; wdb.set_trace() 
            temp = float(record.parent_id.site_temp)
            if record.dist and record.time and record.method != 'indirect':
                velocity = (record.dist / record.time) * 1000  # Convert time from μs to seconds
                if temp > 30:
                    velocity = velocity + (velocity*0.05)
                record.velocity = velocity
            elif record.dist and record.time and record.method == 'indirect':
                velocity = ((record.dist / record.time) * 1000)  # Convert time from μs to seconds
                if velocity > 3:
                    velocity = velocity + 0.5
                if temp > 30:
                    velocity = velocity + (velocity*0.05)
                record.velocity = velocity

            else:
                record.velocity = 0.0

class UpvNotes(models.Model):
    _name = "ndt.upv.notes"

    parent_id = fields.Many2one('ndt.upv',string="Parent Id")
    notes = fields.Char("Notes")
