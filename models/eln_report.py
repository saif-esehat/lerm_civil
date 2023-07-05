from odoo import models , fields,api
import json
import base64
import qrcode
from io import BytesIO

class ElnReport(models.AbstractModel):
    _name = 'report.lerm_civil.eln_report_template'
    _description = 'ELN Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        eln = self.env['lerm.eln'].sudo().browse(docids)
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        qr.add_data(eln.sample_id.client_sample_id)
        qr.make(fit=True)
        qr_image = qr.make_image()

        # Convert the QR code image to base64 string
        buffered = BytesIO()
        qr_image.save(buffered, format="PNG")
        qr_image_base64 = base64.b64encode(buffered.getvalue()).decode()

        # Assign the base64 string to a field in the 'srf' object
        qr_code = qr_image_base64
        return {
            'eln': eln,
            'qrcode': qr_code
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