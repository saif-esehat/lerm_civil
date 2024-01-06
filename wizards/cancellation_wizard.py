from odoo import api, fields, models,_
from odoo.exceptions import UserError
import logging



class SampleCancellationWizard(models.TransientModel):
    _name = "sample.cancellation.wizard"

    cancellation_reason = fields.Selection([
        ('software_error', 'Software Error'),
        ('work_cancelled', 'Work has been Cancelled'),
        ('out_of_scope', 'Out of Scope'),
        ('other', 'Other'),


    ])
    other_cancellation_reason = fields.Text("Cancellation Reason")
