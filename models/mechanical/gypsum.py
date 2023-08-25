from odoo import api, fields, models
from odoo.exceptions import UserError,ValidationError
from datetime import datetime , timedelta
import math



class GypsumMechanical(models.Model):
    _name = "mechanical.gypsum"
    _inherit = "lerm.eln"
    _rec_name = "name"


    name = fields.Char("Name",default="GGBS")
    parameter_id = fields.Many2one('eln.parameters.result', string="Parameter")

    sample_parameters = fields.Many2many('lerm.parameter.master',string="Parameters",store=True)
    eln_ref = fields.Many2one('lerm.eln',string="Eln")
    tests = fields.Many2many("mechanical.gypsum.test",string="Tests")

    # Normal Consistency

    normal_consistency_name = fields.Char("Name",default="Normal Consistency")
    normal_consistency_visible = fields.Boolean("Normal Consistency Visible")

    temp_normal = fields.Float("Temperature")
    humidity_normal = fields.Float("Humidity")
    start_date_normal = fields.Date("Start Date")
    end_date_normal = fields.Date("End Date")



    wt_gypsum_plaster = fields.Float("Wt. of  Gypsum Plaster (g)",default=400)
    wt_water_req = fields.Float("Wt.of water required (g)")
    penetration_vicat = fields.Float("Penetraion of vicat's Plunger (mm)")
    normal_consistency = fields.Float("Normal Consistency %",compute="compute_normal_consistency",store=True)

    @api.depends('wt_gypsum_plaster','wt_water_req')
    def compute_normal_consistency(self):
        for record in self:
            if record.wt_gypsum_plaster != 0:
                record.normal_consistency = (record.wt_water_req / record.wt_gypsum_plaster)*100
            else:
                record.normal_consistency = 0

    # Setting Time 

    setting_time_visible = fields.Boolean("Setting Time Visible")
    setting_time_name = fields.Char("Name",default="Setting Time")

    temp_setting = fields.Float("Temperature %")
    humidity_setting = fields.Float("Humidity %")
    start_date_setting = fields.Date("Start Date")
    end_date_setting = fields.Date("End Date")

    time_water_added = fields.Datetime("The Time When water is added to cement (t1)")
    time_needle_penetrate = fields.Datetime("The time at which needle fails to penetrate the test block (t2)")
    setting_time_minutes = fields.Float("Setting Time (Minutes)", compute="_compute_initial_setting_time")


    @api.depends('time_water_added', 'time_needle_penetrate')
    def _compute_initial_setting_time(self):
        for record in self:
            if record.time_water_added and record.time_needle_penetrate:
                t1 = record.time_water_added
                t2 = record.time_needle_penetrate
                time_difference = t2 - t1

                # Convert time difference to seconds and then to minutes
                time_difference_minutes = time_difference.total_seconds() / 60
                record.setting_time_minutes = time_difference_minutes

                # record.initial_setting_time_hours = time_difference.total_seconds() / 3600
                # if time_difference_minutes % 5 == 0:
                #     record.initial_setting_time_minutes = time_difference_minutes
                # else:
                #     record.initial_setting_time_minutes = round(time_difference_minutes / 5) * 5

            else:
                # record.initial_setting_time_hours = False
                record.setting_time_minutes = False


    # Dry Bulk Density 

    dry_bulk_visible = fields.Boolean("Setting Time Visible")
    dry_bulk_name = fields.Char("Name",default="Setting Time")

    temp_dry_flex = fields.Float("Temperature %")
    humidity_dry_flex = fields.Float("Humidity %")
    start_date_dry_flex = fields.Date("Start Date")
    end_date_dry_flex = fields.Date("End Date")

    wt_empty_cylinder_trial1 = fields.Float("Wt of Empty Cylinder w1")
    wt_empty_cylinder_trial2 = fields.Float("Wt of Empty Cylinder w1")
    wt_empty_cylinder_trial3 = fields.Float("Wt of Empty Cylinder w1")

    wt_empty_gypsum_trial1 = fields.Float("Wt of Empty Gypsum w1")
    wt_empty_gypsum_trial2 = fields.Float("Wt of Empty Gypsum w1")
    wt_empty_gypsum_trial3 = fields.Float("Wt of Empty Gypsum w1")

    wt_empty_cylinder_gypsum_trial1 = fields.Float("Weight of empty Cylinder  + Gypsum (w2")
    wt_empty_cylinder_gypsum_trial2 = fields.Float("Weight of empty Cylinder  + Gypsum (w2")
    wt_empty_cylinder_gypsum_trial3 = fields.Float("Weight of empty Cylinder  + Gypsum (w2")

    volume_of_cylinder_trial1 = fields.Float("Volume of Cylinder")
    volume_of_cylinder_trial2 = fields.Float("Volume of Cylinder")
    volume_of_cylinder_trial3 = fields.Float("Volume of Cylinder")

    dry_loose_bulf_density_trial1 = fields.Float("Dry Loose Bulk Density (kg/m³)")
    dry_loose_bulf_density_trial2 = fields.Float("Dry Loose Bulk Density (kg/m³)")
    dry_loose_bulf_density_trial3 = fields.Float("Dry Loose Bulk Density (kg/m³)")

    average_dry_loose_bulk_density = fields.Float("Average Dry Loose Bulk Density (kg/m³)")



    