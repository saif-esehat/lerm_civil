from odoo import models, fields ,api

class DatasheetMaster(models.Model):
    _name = 'lerm.datasheet.master'
    _rec_name = 'name'
    
    name = fields.Char("Name" , required=True)
    datasheet = fields.One2many('lerm.datasheet.line','datasheet_id',string="Datasheet")

class DatasheetLine(models.Model):
    _name = 'lerm.datasheet.line'
    _rec_name = 'parameter'
    datasheet_id = fields.Many2one('lerm.datasheet.master',string="Datasheet Id")
    parameter = fields.Many2one('lerm.parameter.master',string="Parameter")