from odoo import api, fields, models
from odoo.exceptions import UserError,ValidationError


class CementNormalConsistency(models.Model):
    _name = "mechanical.cement.normalconsistency"
    _inherit = "lerm.eln"
    _rec_name = "name"


    name = fields.Char("Name",default="Normal Consistency")
    parameter_id = fields.Many2one('eln.parameters.result', string="Parameter")

    temp_percent = fields.Float("Temperature %")
    humidity_percent = fields.Float("Humidity %")



    wt_of_cement_trial1 = fields.Float("Wt. of Cement(g)",default=400)
    wt_of_cement_trial2 = fields.Float("Wt. of Cement(g)",default=400)
    wt_of_cement_trial3 = fields.Float("Wt. of Cement(g)",default=400)

    wt_of_water_req_trial1 = fields.Float("Wt.of water required (g)")
    wt_of_water_req_trial2 = fields.Float("Wt.of water required (g)")
    wt_of_water_req_trial3 = fields.Float("Wt.of water required (g)")

    penetration_of_vicat_plunger_trial1 = fields.Float("Penetraion of vicat's Plunger (mm)")
    penetration_of_vicat_plunger_trial2 = fields.Float("Penetraion of vicat's Plunger (mm)")
    penetration_of_vicat_plunger_trial3 = fields.Float("Penetraion of vicat's Plunger (mm)")

    normal_consistency_trial1 = fields.Float("Normal Consistency (%)",compute="_compute_normal_consistency",store=True)
    normal_consistency_trial2 = fields.Float("Normal Consistency (%)",compute="_compute_normal_consistency",store=True)
    normal_consistency_trial3 = fields.Float("Normal Consistency (%)",compute="_compute_normal_consistency",store=True)

    @api.model
    def create(self, vals):
        # import wdb;wdb.set_trace()
        record = super(CementNormalConsistency, self).create(vals)
        record.get_all_fields()
        record.parameter_id.write({'model_id':record.id})
        return record

    @api.model 
    def write(self, values):
        # Perform additional actions or validations before update
        result = super(CementNormalConsistency, self).write(values)
        # Perform additional actions or validations after update
        return result



    def get_all_fields(self):
        record = self.env['mechanical.cement.normalconsistency'].browse(self.ids[0])
        field_values = {}
        for field_name, field in record._fields.items():
            field_value = record[field_name]
            field_values[field_name] = field_value

        return field_values

    @api.depends("wt_of_cement_trial1","wt_of_cement_trial2","wt_of_cement_trial3","wt_of_water_req_trial1","wt_of_water_req_trial2","wt_of_water_req_trial3")
    def _compute_normal_consistency(self):
        for record in self:
            if record.wt_of_water_req_trial1 and record.wt_of_cement_trial1:
                record.normal_consistency_trial1 = (record.wt_of_water_req_trial1/record.wt_of_cement_trial1) * 100
            else:
                record.normal_consistency_trial1 = 0
            
            if record.wt_of_water_req_trial2 and record.wt_of_cement_trial2:
                record.normal_consistency_trial2 = (record.wt_of_water_req_trial2/record.wt_of_cement_trial2) * 100
            else:
                record.normal_consistency_trial2 = 0

            if record.wt_of_water_req_trial3 and record.wt_of_cement_trial3:
                record.normal_consistency_trial3 = (record.wt_of_water_req_trial3/record.wt_of_cement_trial3) * 100
            else:
                record.normal_consistency_trial3 = 0