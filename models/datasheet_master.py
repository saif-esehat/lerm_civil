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
    test_method = fields.Many2one('lerm_civil.test_method',string="Test Method")
<<<<<<< HEAD
    calculated = fields.Boolean("Calculated")
=======
>>>>>>> 2c897141ecbd10d66120adc678d1debd8012fed2


    @api.onchange("parameter")
    def onchange_parameter(self):
        for record in self:
            record.test_method = record.parameter.test_method.id
<<<<<<< HEAD
            record.calculated = record.parameter.calculated
=======
>>>>>>> 2c897141ecbd10d66120adc678d1debd8012fed2
