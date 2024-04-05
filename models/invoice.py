from odoo import models, fields ,api


class AccountMoveInheritedLerm(models.Model):
    _inherit = 'account.move'

    # @api.model
    # def create(self,vals):
    #     import wdb; wdb.set_trace()
    #     print("Insideeeeeeeee move")
    #     # res = super(AccountMoveInheritedLerm,self).create(vals)
    #     # return res

    def action_post(self):
        # import wdb; wdb.set_trace()
        for rec in self.invoice_line_ids.report_no1:
            rec.invoice_status = '2-invoiced'
        super(AccountMoveInheritedLerm,self).action_post()