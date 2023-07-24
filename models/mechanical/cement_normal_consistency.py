from odoo import api, fields, models
from odoo.exceptions import UserError,ValidationError
from datetime import datetime



class CementNormalConsistency(models.Model):
    _name = "mechanical.cement.normalconsistency"
    _inherit = "lerm.eln"
    _rec_name = "name"


    name = fields.Char("Name",default="Normal Consistency")
    parameter_id = fields.Many2one('eln.parameters.result', string="Parameter")

    temp_percent = fields.Float("Temperature %")
    humidity_percent = fields.Float("Humidity %")

    ## Normal Consistency

    tests = fields.Many2many("mechanical.cement.test",string="Tests")

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

    

    ### setting Time,Final Setting Time	

    setting_time_visible = fields.Boolean("Setting Time Visible",compute="_compute_visible")
    setting_time_name = fields.Char("Name",default="Setting Time")

    temp_percent = fields.Float("Temperature %")
    humidity_percent = fields.Float("Humidity %")

    wt_of_cement_setting_time = fields.Float("Wt. of Cement(g)",default=400)
    wt_of_water_required_setting_time = fields.Float("Wt.of water required (g) (0.85*P%)" , compute="_compute_wt_of_water_required",store=True )

    @api.depends('normal_consistency_trial3','wt_of_cement_setting_time')
    def _compute_wt_of_water_required(self):
        for record in self:
            record.wt_of_water_required_setting_time =  (((0.85 * record.normal_consistency_trial3) / 100) * record.wt_of_cement_setting_time)

    #Initial setting Time

    initial_setting_time = fields.Char("Name",default="Initial Setting Time")
    time_water_added = fields.Datetime("The Time When water is added to cement (t1)")
    time_needle_fails = fields.Datetime("The time at which needle fails to penetrate the test block to a point 5 ± 0.5 mm (t2)")
    initial_setting_time_hours = fields.Char("Initial Setting Time (t2-t1) (Hours)",compute="_compute_initial_setting_time")
    initial_setting_time_minutes = fields.Char("Initial Setting (Minutes)",compute="_compute_initial_setting_time")

    @api.depends('time_water_added', 'time_needle_fails')
    def _compute_initial_setting_time(self):
        for record in self:
            if record.time_water_added and record.time_needle_fails:
                t1 = record.time_water_added
                t2 = record.time_needle_fails
                time_difference = t2 - t1

                # hours = time_difference.total_seconds() / 3600

                record.initial_setting_time_hours = time_difference
                record.initial_setting_time_minutes = time_difference.total_seconds() / 60

            else:
                record.initial_setting_time_hours = False
                record.initial_setting_time_minutes = False


    #Final setting Time

    final_setting_time = fields.Char("Name",default="Final Setting Time")
    time_needle_make_impression = fields.Datetime("The Time at which the needle make an impression on the surface of test block while attachment fails to do (t3)")
    final_setting_time_hours = fields.Char("Initial Setting Time (t2-t1) (Hours)",compute="_compute_final_setting_time")
    final_setting_time_minutes = fields.Char("Initial Setting (Minutes)",compute="_compute_final_setting_time")




    @api.depends('time_needle_make_impression')
    def _compute_final_setting_time(self):
        for record in self:
            if record.time_needle_make_impression and record.time_water_added:
                t1 = record.time_water_added
                t2 = record.time_needle_make_impression
                time_difference = t2 - t1

                record.final_setting_time_hours = time_difference
                record.final_setting_time_minutes = time_difference.total_seconds() / 60
            else:
                record.final_setting_time_hours = False
                record.final_setting_time_minutes = False





    ### Compute Visible
    @api.depends('tests')
    def _compute_visible(self):
        setting_time_test = self.env['mechanical.cement.test'].search([('name', '=', 'Setting Time')])
        for record in self:
            record.setting_time_visible = setting_time_test in record.tests


    @api.model
    def create(self, vals):
        # import wdb;wdb.set_trace()
        record = super(CementNormalConsistency, self).create(vals)
        record.get_all_fields()
        record.parameter_id.write({'model_id':record.id})
        return record

    # @api.model 
    # def write(self, values):
    #     # Perform additional actions or validations before update
    #     result = super(CementNormalConsistency, self).write(values)
    #     # Perform additional actions or validations after update
    #     return result



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
    


class CementTest(models.Model):
    _name = "mechanical.cement.test"
    _rec_name = "name"
    name = fields.Char("Name")
