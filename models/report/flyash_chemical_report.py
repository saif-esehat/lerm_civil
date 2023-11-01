from odoo import models , fields,api
import json
import base64
import qrcode
from io import BytesIO


class FlyAshChemicalReport(models.AbstractModel):
    _name = 'report.lerm_civil.flyash_chemical_report'
    _description = 'ELN Report'

    @api.model
    def _get_report_values(self, docids, data):
        # eln = self.env['lerm.eln'].sudo().browse(docids)
        inreport_value = data.get('inreport', None)
        nabl = data.get('nabl')
        print(data , 'dataaaaaaaaaaaaaa')
        # stamp = data['inreport']
        if 'active_id' in data['context']:
            # stamp = data['inreport']
            eln = self.env['lerm.eln'].sudo().search([('sample_id','=',data['context']['active_id'])])
        else:
            eln = self.env['lerm.eln'].sudo().browse(docids)
        print()
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        qr.add_data(eln.kes_no)
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
            'qrcode': qr_code,
            'stamp' : inreport_value,
            'nabl' : nabl,
            'report_name' : 'Afzal'
        }