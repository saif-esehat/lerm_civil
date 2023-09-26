# from odoo import api, fields, models
# from odoo.exceptions import UserError,ValidationError
# from datetime import timedelta
# import math



# class AggregateFine(models.Model):
#     _name = "mechanical.aggregate.fine"
#     _inherit = "lerm.eln"
#     _rec_name = "name_aggregate"


#     name_aggregate = fields.Char("Name",default="Fine Aggregate")
#     parameter_id = fields.Many2one('eln.parameters.result', string="Parameter")

#     sample_parameters = fields.Many2many('lerm.parameter.master',string="Parameters",compute="_compute_sample_parameters",store=True)
#     eln_ref = fields.Many2one('lerm.eln',string="Eln")

#     tests = fields.Many2many("mechanical.aggregate.fine.test",string="Tests")

#     # Loose Bulk Density (LBD)

#     loose_bulk_name = fields.Char("Name",default="Loose Bulk Density (LBD)")
#     loose_bulk_visible = fields.Boolean("Loose Bulk Density (LBD) Visible",compute="_compute_visible")





#     ### Compute Visible
#     @api.depends('tests')
#     def _compute_visible(self):
#         loose_bulk_test = self.env['mechanical.aggregate.fine.test'].search([('name', '=', 'Loose Bulk Density (LBD)')])
        
#         for record in self:
#             record.loose_bulk_visible = False
           
            
#             if loose_bulk_test in record.tests:
#                 record.loose_bulk_visible = True

            



               


#     @api.model
#     def create(self, vals):
#         # import wdb;wdb.set_trace()
#         record = super(AggregateFine, self).create(vals)
#         record.get_all_fields()
#         record.eln_ref.write({'model_id':record.id})
#         return record







#     @api.depends('eln_ref')
#     def _compute_sample_parameters(self):
#         # records = self.env['lerm.eln'].search([('id','=', record.eln_id.id)]).parameters_result
#         # print("records",records)
#         # self.sample_parameters = records
#         for record in self:
#             records = record.eln_ref.parameters_result.parameter.ids
#             record.sample_parameters = records
#             print("Records",records)



#     def get_all_fields(self):
#         record = self.env['mechanical.soil'].browse(self.ids[0])
#         field_values = {}
#         for field_name, field in record._fields.items():
#             field_value = record[field_name]
#             field_values[field_name] = field_value

#         return field_values




# class AggregateFineTest(models.Model):
#     _name = "mechanical.aggregate.fine.test"
#     _rec_name = "name"
#     name = fields.Char("Name")
