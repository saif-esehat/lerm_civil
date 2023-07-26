from odoo import api, fields, models
from odoo.exceptions import UserError,ValidationError
import math


class HalfCell(models.Model):
    _name = "ndt.half.cell"
    _inherit = "lerm.eln"
    _rec_name = "name"

    name = fields.Char("Name",default="Half Cell")
    parameter_id = fields.Many2one('eln.parameters.result', string="Parameter")
    structure_age = fields.Char("Year of Construction")
    temp = fields.Float("Temp")
    instrument = fields.Char("Instrument")
    child_lines_1 = fields.One2many('ndt.half.cell.one', 'parent_id', string="Parameter")
    child_lines_2 = fields.One2many('ndt.half.cell.two', 'parent_id', string="Parameter")

    @api.model
    def create(self, vals):
        # import wdb;wdb.set_trace()
        record = super(HalfCell, self).create(vals)
        record.parameter_id.write({'model_id':record.id})
        return record
   

    # @api.model
    # def _is_temp_within_range(self, temp):
    #     return 22.2 <= temp <= 27.7

    # def _check_temperature(self):
    #     for record in self:
    #         if not self._is_temp_within_range(record.temp):
    #             raise UserError("Temperature should be between 22.2°C and 27.7°C.")

    def button_press_action(self):

        if self.temp < 22.2:
            correction = 22.2 - self.temp
            mv = correction * (-0.91)
        elif self.temp > 27.7:
            correction = self.temp - 27.7
            mv = correction * (-0.91)
        else:
            print("No Factor Needed")
        
        # import wdb; wdb.set_trace()


        for line1 in self.child_lines_1:
            # import wdb; wdb.set_trace()
            # Find or create the corresponding record in child_lines_2 using the 'member' and 'location' fields
            corresponding_line2 = self.child_lines_2.filtered(lambda line2: line2.member == line1.member and line2.location == line1.location)

            if corresponding_line2:
                # Update the existing record in child_lines_2
                corresponding_line2.write({
                    'r1': line1.r1 + mv,
                    'r2': line1.r2 + mv,
                    'r3': line1.r3 + mv,
                    'r4': line1.r4 + mv,
                    'r5': line1.r5 + mv,
                    'r6': line1.r6 + mv,
                })
            else:
                # Create a new record in child_lines_2
                self.env['ndt.half.cell.two'].create({
                    'parent_id': self.id,
                    'member': line1.member,
                    'location': line1.location,
                    'level': line1.level,
                    'r1': line1.r1 + mv,
                    'r2': line1.r2 + mv,
                    'r3': line1.r3 + mv,
                    'r4': line1.r4 + mv,
                    'r5': line1.r5 + mv,
                    'r6': line1.r6 + mv,
                })            

class HalfCellLineOne(models.Model):
    _name = "ndt.half.cell.one"
    parent_id = fields.Many2one('ndt.half.cell',string="Parent Id")
    member = fields.Char("Member")
    location = fields.Char("Location")
    level = fields.Char("Level")
    r1 = fields.Float("R1")
    r2 = fields.Float("R2")
    r3 = fields.Float("R3")
    r4 = fields.Float("R4")
    r5 = fields.Float("R5")
    r6 = fields.Float("R6")
    avg = fields.Float("AVG",compute='_compute_avg')

    @api.depends('r1', 'r2', 'r3', 'r4', 'r5','r6')
    def _compute_avg(self):
        for record in self:
            record.avg = (record.r1 + record.r2 + record.r3 + record.r4 + record.r5 + record.r6) / 6.0


class HalfCellLineTwo(models.Model):
    _name = "ndt.half.cell.two"
    parent_id = fields.Many2one('ndt.half.cell',string="Parent Id")
    member = fields.Char("Member")
    location = fields.Char("Location")
    level = fields.Char("Level")
    r1 = fields.Float("R1")
    r2 = fields.Float("R2")
    r3 = fields.Float("R3")
    r4 = fields.Float("R4")
    r5 = fields.Float("R5")
    r6 = fields.Float("R6")
    avg = fields.Float("AVG",compute='_compute_avg')

    @api.depends('r1', 'r2', 'r3', 'r4', 'r5','r6')
    def _compute_avg(self):
        for record in self:
            record.avg = (record.r1 + record.r2 + record.r3 + record.r4 + record.r5 + record.r6) / 6.0
