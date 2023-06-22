from odoo import models , fields,api
import json

class ElnReport(models.AbstractModel):
    _name = 'report.lerm_civil.eln_report_template'
    _description = 'ELN Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        eln = self.env['lerm.eln'].sudo().browse(docids)

        print(eln,"ELN DATA")

        return {
            'eln': eln
        }


class DataSheetReport(models.AbstractModel):
    _name = 'report.lerm_civil.datasheet_report_template'
    _description = 'DataSheet Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        eln = self.env['lerm.eln'].sudo().browse(docids)
        return {
            'eln': eln
        }