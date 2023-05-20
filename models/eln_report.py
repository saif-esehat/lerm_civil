from odoo import models , fields,api
import json

class ElnReport(models.AbstractModel):
    _name = 'report.lerm_civil.eln_report_template'
    _description = 'ELN Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs1 = self.env['account.move'].sudo().browse(docids)
        tax_totals_json = docs1.tax_totals_json

        # Parse the tax_totals_json string into a Python object
        tax_totals = json.loads(tax_totals_json)
        # Pass the tax_totals to the report context
        report_data = {'tax_totals': tax_totals}

        return {
              'doc_ids': docids,
              'doc_model': 'account.move',
              'data': docs1,
              'report_data': report_data,
        }
