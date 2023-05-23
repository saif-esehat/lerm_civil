from odoo import models , fields,api
import json

class ElnReport(models.AbstractModel):
    _name = 'report.lerm_civil.eln_report_template'
    _description = 'ELN Report'

    @api.model
    def _get_report_values(self, docids, data=None):

        eln = self.env['lerm.eln'].sudo().browse(docids)
        import wdb ; wdb.set_trace()        
        for parameter in eln.parameters:
            print(parameter.result_json)
            data = parameter.result_json



        # docs1 = self.env['account.move'].sudo().browse(docids)
        # tax_totals_json = docs1.tax_totals_json

        # Parse the tax_totals_json string into a Python object
        # tax_totals = json.loads(tax_totals_json)
        # Pass the tax_totals to the report context
        # report_data = {'tax_totals': tax_totals}
#         data_mock = [
#             {
#                 "columns" : [
#                     {"name": "Particulars"},
#                     {"name": "Results"}
#                 ]
#             },
#             {
#             "rows": [
#                 {
#                 "row" : [
#                 {"value": "i) Mean weight of the aggregate in the cylinder in gm, W"},
#                 {"value": 21}
#                 ]
#                 },
#                 {
#                 "row" : [
#                 {"value": "i) M of the aggregate in the cylinder in gm, W"},
#                 {"value": 81}
#                 ]
#                 }
#         ]
#     }
           
# ]

        return {
            'data_mock': data_json
        }
