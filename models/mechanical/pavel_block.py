from odoo import api, fields, models
from odoo.exceptions import UserError,ValidationError
import math

class PavelBlock(models.Model):
    _name = "mechanical.pavel.block"
    _inherit = "lerm.eln"
    _rec_name = "name"

    name = fields.Char("Name",default="Tensile Splitting Strength")
    parameter_id = fields.Many2one('eln.parameters.result',string="Parameter")
    child_lines = fields.One2many('mechanical.pavel.block.line','parent_id',string="Parameter" )
    average_tensile = fields.Float(string="Average Tensile Splitting Strength", compute="_compute_average_tensile")  

    @api.model
    def create(self, vals):
        # import wdb;wdb.set_trace()
        record = super(PavelBlock, self).create(vals)
        record.parameter_id.write({'model_id':record.id})
        return record


    @api.depends('child_lines.splitting_tensile')
    def _compute_average_tensile(self):
        for record in self:
            splitting_tensiles = record.child_lines.mapped('splitting_tensile')
            if splitting_tensiles:
                record.average_tensile = sum(splitting_tensiles) / len(splitting_tensiles)
            else:
                record.average_tensile = 0.0

    
   



class PavelBlockthLine(models.Model):
    _name = "mechanical.pavel.block.line"
    parent_id = fields.Many2one('mechanical.pavel.block',string="Parent Id")

    length = fields.Float(string="Mean of failure Length in mm (l)")
    thickness = fields.Float(string="Mean of failure Thickness in mm (t)")
    area = fields.Float(string="Area of Failure = l x t in mm2", compute="_compute_area")
    failure_load = fields.Float(string="Failure Load in N")
    splitting_tensile = fields.Float(string="Tensile Splitting Strength in N/mm2", compute="_compute_splitting_tensile")
    # average_tensile = fields.Float(string="AverageTensile Splitting Strength in N/mm2", compute="_compute_average_tensile")    



    @api.depends('length', 'thickness')
    def _compute_area(self):
        for record in self:
            record.area = record.length * record.thickness


    @api.depends('failure_load', 'area')
    def _compute_splitting_tensile(self):
        for record in self:
            if record.area != 0:
                record.splitting_tensile = record.failure_load / record.area
            else:
                record.splitting_tensile = 0.0

    # @api.depends('splitting_tensile')
    # def _compute_average_tensile(self):
    #     for record in self:
    #         record.average_tensile = record.splitting_tensile
    


   
    
