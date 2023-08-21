from odoo import api, fields, models
from odoo.exceptions import UserError,ValidationError
from datetime import timedelta
import math



class FlyaschNormalConsistency(models.Model):
    _name = "mechanical.flyasch.normalconsistency"
    _inherit = "lerm.eln"
    _rec_name = "name"


    name = fields.Char("Name",default="Fly Asch")
    parameter_id = fields.Many2one('eln.parameters.result', string="Parameter")

    sample_parameters = fields.Many2many('lerm.parameter.master',string="Parameters",compute="_compute_sample_parameters",store=True)
    eln_ref = fields.Many2one('lerm.eln',string="Eln")

    temp_percent_normal = fields.Float("Temperature %")
    humidity_percent_normal = fields.Float("Humidity %")

     ## Normal Consistency

    tests = fields.Many2many("mechanical.cement.test",string="Tests")

    normal_consistency_name = fields.Char("Name",default="Normal Consistency")
    normal_consistency_visible = fields.Boolean("Normal Consistency Visible",compute="_compute_visible")
    start_date_normal = fields.Date("Start Date")
    end_date_normal = fields.Date("End Date")



    specific_gravity_fly1 = fields.Float("Specific Gravity of Flyash")
    specific_gravity_cement1 = fields.Float("Specific Gravity of Cement")
    n1 = fields.Float("N",compute="_compute_n",store=True)
    
    wt_of_flyash = fields.Float(string="Wt. of Flyash",compute="_compute_flyash")
    wt_of_cement = fields.Float(string="Wt. of  Cement",default=0.8*400)
    total_wt_of_sample = fields.Float(string="Total Weight of Sample(g)",compute="_compute_of_sample")

    wt_of_water_req_trial1 = fields.Float("Wt.of water required (g)")
    penetration_of_vicat_plunger_trial1 = fields.Float("Penetraion of vicat's Plunger (mm)")

    normal_consistency_trial1 = fields.Float("Normal Consistency (%)",compute="_compute_normal_consistency",store=True)

    @api.depends('specific_gravity_fly1','specific_gravity_cement1')
    def _compute_n(self):
        for record in self:
            if record.specific_gravity_cement1 != 0:
                record.n1 = record.specific_gravity_fly1 / record.specific_gravity_cement1
            else:
                record.n1 = 0.0


    @api.depends('n1')
    def _compute_flyash(self):
        for record in self:
            record.wt_of_flyash = 0.2 * record.n1 * 400

    @api.depends('wt_of_cement','wt_of_flyash')
    def _compute_of_sample(self):
        for record in self:
            record.total_wt_of_sample = record.wt_of_cement + record.wt_of_flyash

    @api.depends('wt_of_water_req_trial1','total_wt_of_sample')
    def _compute_normal_consistency(self):
        for record in self:
            if record.total_wt_of_sample != 0:
                record.normal_consistency_trial1 = (record.wt_of_water_req_trial1 / record.total_wt_of_sample) * 100
            else:
                record.normal_consistency_trial1 = 0.0

    specific_gravity_fly2 = fields.Float("Specific Gravity of Flyash")
    specific_gravity_cement2 = fields.Float("Specific Gravity of Cement")
    n2 = fields.Float("N",compute="_compute_n2")

    wt_of_flyash2 = fields.Float(string="Wt. of Flyash",compute="_compute_flyash2")
    wt_of_cement2 = fields.Float(string="Wt. of  Cement",default=0.8*400)
    total_wt_of_sample2 = fields.Float(string="Total Weight of Sample(g)",compute="_compute_of_sample2")

    wt_of_water_req_trial2 = fields.Float("Wt.of water required (g)")
    penetration_of_vicat_plunger_trial2 = fields.Float("Penetraion of vicat's Plunger (mm)")

    normal_consistency_trial2 = fields.Float("Normal Consistency (%)",compute="_compute_normal_consistency2",store=True)

    @api.depends('specific_gravity_fly2','specific_gravity_cement2')
    def _compute_n2(self):
        for record in self:
            if record.specific_gravity_cement2 != 0:
                record.n2 = record.specific_gravity_fly2 / record.specific_gravity_cement2
            else:
                record.n2 = 0.0

    @api.depends('n2')
    def _compute_flyash2(self):
        for record in self:
            record.wt_of_flyash2 = 0.2 * record.n2 * 400

    @api.depends('wt_of_flyash2','wt_of_cement2')
    def _compute_of_sample2(self):
        for record in self:
            record.total_wt_of_sample2 = record.wt_of_flyash2 + record.wt_of_cement2


    @api.depends('wt_of_water_req_trial2','total_wt_of_sample2')
    def _compute_normal_consistency2(self):
        for record in self:
            if record.total_wt_of_sample2 != 0:
                record.normal_consistency_trial2 = (record.wt_of_water_req_trial2 / record.total_wt_of_sample2) * 100
            else:
                record.normal_consistency_trial2 = 0.0

    


    # Setting Time
    setting_time_visible = fields.Boolean("Setting Time Visible",compute="_compute_visible")
    setting_time_name = fields.Char("Name",default="Setting Time")

    temp_percent_setting = fields.Float("Temperature %")
    humidity_percent_setting = fields.Float("Humidity %")
    start_date_setting = fields.Date("Start Date")
    end_date_setting = fields.Date("End Date")

    total_wt_of_sample_setting_time = fields.Float(string="Total Weight of Sample(g)",compute="_compute_total_wt_of_sample_setting_time",store=True)
    wt_of_water_required_setting_time = fields.Float("Wt.of water required (g)",compute="_compute_wt_of_water_required",store=True)


    @api.depends('total_wt_of_sample')
    def _compute_total_wt_of_sample_setting_time(self):
        for record in self:
            record.total_wt_of_sample_setting_time = record.total_wt_of_sample

    @api.depends('normal_consistency_trial1','total_wt_of_sample_setting_time')
    def _compute_wt_of_water_required(self):
        for record in self:
            record.wt_of_water_required_setting_time =  (0.85 * record.normal_consistency_trial1 * record.total_wt_of_sample_setting_time) / 100


    initial_setting_time = fields.Char("Name", default="Initial Setting Time")
    time_water_added = fields.Datetime("The Time When water is added to cement (t1)")
    time_needle_fails = fields.Datetime("The time at which needle fails to penetrate the test block to a point 5 ± 0.5 mm (t2)")
    initial_setting_time_hours = fields.Float("Initial Setting Time (t2-t1) (Hours)", compute="_compute_initial_setting_time")
    initial_setting_time_minutes = fields.Float("Initial Setting Time", compute="_compute_initial_setting_time")

    @api.depends('time_water_added', 'time_needle_fails')
    def _compute_initial_setting_time(self):
        for record in self:
            if record.time_water_added and record.time_needle_fails:
                t1 = record.time_water_added
                t2 = record.time_needle_fails
                time_difference = t2 - t1

                # Convert time difference to seconds and then to minutes
                time_difference_minutes = time_difference.total_seconds() / 60

                record.initial_setting_time_hours = time_difference.total_seconds() / 3600
                if time_difference_minutes % 5 == 0:
                    record.initial_setting_time_minutes = time_difference_minutes
                else:
                    record.initial_setting_time_minutes = round(time_difference_minutes / 5) * 5

            else:
                record.initial_setting_time_hours = False
                record.initial_setting_time_minutes = False


     #Final setting Time

    final_setting_time = fields.Char("Name",default="Final Setting Time")
    time_needle_make_impression = fields.Datetime("The Time at which the needle make an impression on the surface of test block while attachment fails to do (t3)")
    final_setting_time_hours = fields.Char("Final Setting Time (t3-t1) (Hours)",compute="_compute_final_setting_time")
    final_setting_time_minutes = fields.Char("Final Setting Time",compute="_compute_final_setting_time")




    @api.depends('time_needle_make_impression')
    def _compute_final_setting_time(self):
        for record in self:
            if record.time_needle_make_impression and record.time_water_added:
                t1 = record.time_water_added
                t2 = record.time_needle_make_impression
                time_difference = t2 - t1

                record.final_setting_time_hours = time_difference
                final_setting_time = time_difference.total_seconds() / 60
                if final_setting_time % 5 == 0:
                    record.final_setting_time_minutes =  final_setting_time
                else:
                    record.final_setting_time_minutes =  round(final_setting_time / 5) * 5
            else:
                record.final_setting_time_hours = False
                record.final_setting_time_minutes = False

     #  Particles retained on 45 micron IS sieve (wet sieving) 

    particles_retained = fields.Char("Name",default=" Particles retained on 45 micron IS sieve (wet sieving)")
    particles_retained_visible = fields.Boolean("Particles retained Visible",compute="_compute_visible")

    temp_percent_retained = fields.Float("Temperature %")
    humidity_percent_retained = fields.Float("Humidity %")
    start_date_retained = fields.Date("Start Date")
    end_date_retained = fields.Date("End Date")


    particles_retained_table = fields.One2many('particles.retained.line','parent_id',string="Particles Retained")
    average_weight_retained = fields.Float("Average", compute="_compute_average_weight_retained")

    prcent_retaind = fields.Float(string="% Weight Retained",compute="_compute_prcent_retaind",digits=(12,1))


    @api.depends('particles_retained_table.wt_retained')
    def _compute_average_weight_retained(self):
        for record in self:
            total_wt_retained = sum(record.particles_retained_table.mapped('wt_retained'))
            count_lines = len(record.particles_retained_table)
            record.average_weight_retained = total_wt_retained / count_lines if count_lines else 0.0

    @api.depends('average_weight_retained')
    def _compute_prcent_retaind(self):
        for record in self:
            integer_part = math.floor(record.average_weight_retained)
            fractional_part = record.average_weight_retained - integer_part
            if fractional_part > 0 and fractional_part <= 0.25:
                record.prcent_retaind = integer_part
            elif fractional_part > 0.25 and fractional_part <= 0.75:
                record.prcent_retaind = integer_part + 0.5
            elif fractional_part > 0.75 and fractional_part <= 1:
                record.prcent_retaind = integer_part + 1
            else:
                record.prcent_retaind = 0

    # Soundness Test
    soundness_name_fly = fields.Char("Name",default="Soundness by Le-Chatelier Method")
    soundness_visible = fields.Boolean("Soundness Visible",compute="_compute_visible")

    temp_percent_soundness = fields.Float("Temperature %")
    humidity_percent_soundness = fields.Float("Humidity %")
    start_date_soundness = fields.Date("Start Date")
    end_date_soundness = fields.Date("End Date")


    wt_of_flyash_soundness = fields.Float(string="Wt. of Flyash",compute="_compute_wt_of_flyash_soundness")
    wt_of_cement_soundness = fields.Float(string="Wt. of Cement (g)",default=0.8*100)
    total_wt_sample_soundness = fields.Float(string="Total Weight of Sample(g)",compute="_compute_total_wt_sample_soundness")
    wt_of_water_req_soundness = fields.Float(string="Wt.of water required (g)",compute="_compute_wt_of_water_req_soundness")

    @api.depends('n1')
    def _compute_wt_of_flyash_soundness(self):
        for record in self:
            record.wt_of_flyash_soundness = (0.2 * record.n1 * 100)

    @api.depends('wt_of_flyash_soundness','wt_of_cement_soundness')
    def _compute_total_wt_sample_soundness(self):
        for record in self:
            record.total_wt_sample_soundness = record.wt_of_flyash_soundness + record.wt_of_cement_soundness

    @api.depends('normal_consistency_trial1', 'total_wt_sample_soundness')
    def _compute_wt_of_water_req_soundness(self):
      for record in self:
        if record.total_wt_sample_soundness != 0:
            record.wt_of_water_req_soundness = (0.78 * record.normal_consistency_trial1 / 100) * record.total_wt_sample_soundness
        else:
            record.wt_of_water_req_soundness = 0.0

    soundness_table = fields.One2many('flyash.soundness.line','parent_id',string="Soundness")
    average_soundness = fields.Float("Average",compute="_compute_average_soundness")
    expansion_soundness = fields.Float("Expansion(mm)",compute="_compute_expansion_soundness")

    @api.depends('soundness_table.expansion')
    def _compute_average_soundness(self):
        for record in self:
            try:
                record.average_soundness = sum(record.soundness_table.mapped('expansion'))/len(record.soundness_table)
            except:
                record.average_soundness = 0

    @api.depends('average_soundness')
    def _compute_expansion_soundness(self):
        for record in self:
            integer_part = math.floor(record.average_soundness)
            fractional_part = record.average_soundness - integer_part
            if fractional_part > 0 and fractional_part <= 0.25:
                record.expansion_soundness = integer_part
            elif fractional_part > 0.25 and fractional_part <= 0.75:
                record.expansion_soundness = integer_part + 0.5
            elif fractional_part > 0.75 and fractional_part <= 1:
                record.expansion_soundness = integer_part + 1
            else:
                record.expansion_soundness = 0
    
    #  Specigic Gravity
    specigic_gravity = fields.Char("Name",default="Specigic Gravity")
    specigic_gravity_visible = fields.Boolean("Specigic Gravity Visible",compute="_compute_visible")

    temp_percent_specific = fields.Float("Temperature %")
    humidity_percent_specific = fields.Float("Humidity %")
    start_date_specific = fields.Date("Start Date")
    end_date_specific = fields.Date("End Date")


    wt_of_flyash_specific1 = fields.Float(string="Weight of Flyash (g)",default=45)
    wt_of_flyash_specific2 = fields.Float(string="Weight of Flyash (g)",default=45)

    intial_volume_specific1 = fields.Float(string="Initial Volume of kerosine (ml)")
    intial_volume_specific2 = fields.Float(string="Initial Volume of kerosine (ml)")

    final_volume_specific1 = fields.Float(string="Final Volume of kerosine and Flyash (After immersion in constant water bath) (ml)")
    final_volume_specific2 = fields.Float(string="Final Volume of kerosine and Flyash (After immersion in constant water bath) (ml)")
    
    displaced_volume1 = fields.Float(string="Displaced volume (cm³)",compute="_compute_volume1",digits=(12,1))
    displaced_volume2 = fields.Float(string="Displaced volume (cm³)",compute="_compute_volume2",digits=(12,1))

    specific_gravity1 = fields.Float(string="Specific Gravity",compute="_compute_specific1")
    specific_gravity2 = fields.Float(string="Specific Gravity",compute="_compute_specific2")

    average_specific_gravity = fields.Float(
        string="Average",
        compute="_compute_average_specific_gravity")

    @api.depends('final_volume_specific1','intial_volume_specific1')
    def _compute_volume1(self):
        for record in self:
            record.displaced_volume1 = record.final_volume_specific1 - record.intial_volume_specific1

    @api.depends('final_volume_specific2','intial_volume_specific2')
    def _compute_volume2(self):
        for record in self:
            record.displaced_volume2 = record.final_volume_specific2 - record.intial_volume_specific2

    @api.depends('wt_of_flyash_specific1','displaced_volume1')
    def _compute_specific1(self):
        for record in self:
            if record.displaced_volume1 != 0:
                record.specific_gravity1 = record.wt_of_flyash_specific1 / record.displaced_volume1
            else:
                record.specific_gravity1 = 0.0

    @api.depends('wt_of_flyash_specific2','displaced_volume2')
    def _compute_specific2(self):
        for record in self:
            if record.displaced_volume2 != 0:
                record.specific_gravity2 = record.wt_of_flyash_specific2 / record.displaced_volume2
            else:
                record.specific_gravity2 = 0.0

    

    @api.depends('specific_gravity1', 'specific_gravity2')
    def _compute_average_specific_gravity(self):
        for record in self:
            average = (record.specific_gravity1 + record.specific_gravity2) / 2
            record.average_specific_gravity = average



     # Compressive Strength 

    compressive_name = fields.Char("Name",default="Compressive Strength")
    compressive_visible = fields.Boolean("Compressive Visible",compute="_compute_visible")

    temp_percent_compressive = fields.Float("Temperature %")
    humidity_percent_compressive = fields.Float("Humidity %")
    start_date_compressive = fields.Date("Start Date")
    end_date_compressive = fields.Date("End Date")


    specific_garavity_flyash = fields.Float(string="Specific Gravity of Flyash (g)",compute="_compute_specific_gravity_flyash")
    specific_gravity_cement = fields.Float(string="Specific Gravity of cement (g)",compute="_compute_specific_gravity_cement")
    n2 = fields.Float(string="N",compute="_compute_n2")
    weight_of_flyash = fields.Float(string="Weight of Flyash (g)",compute="_compute_wt_flyash")
    wt_of_cement_comp = fields.Integer(string="Weight of Cement (g)",default=400)
    wt_of_standerd_comp1 = fields.Integer(string="Weight of Standard Sand (g)Grade-I",default=500)
    wt_of_standerd_comp2 = fields.Integer(string="Weight of Standard Sand (g)Grade-II",default=500)
    wt_of_standerd_comp3 = fields.Integer(string="Weight of Standard Sand (g)Grade-III",default=500)
    quantity_water = fields.Integer(string="Quantity of Water (g)")
   
    @api.depends('average_specific_gravity')
    def _compute_specific_gravity_flyash(self):
        for record in self:
            record.specific_garavity_flyash = record.average_specific_gravity

    @api.depends('specific_gravity_cement1')
    def _compute_specific_gravity_cement(self):
        for record in self:
            record.specific_gravity_cement = record.specific_gravity_cement1

    @api.depends('specific_garavity_flyash', 'specific_gravity_cement')
    def _compute_n2(self):
        for record in self:
            if record.specific_gravity_cement != 0:
                record.n2 = record.specific_garavity_flyash / record.specific_gravity_cement
            else:
                record.n2 = 0.0

    @api.depends('n2')
    def _compute_wt_flyash(self):
        for record in self:
            record.weight_of_flyash = 100 * record.n2


    measured_value1 = fields.Float(string="Measured Values")
    measured_value2 = fields.Float(string="Measured Values")
    measured_value3 = fields.Float(string="Measured Values")
    measured_value4 = fields.Float(string="Measured Values")

    average_measured = fields.Float(string="Average",compute="_compute_average")
    percent_flow = fields.Float(string="% Flow",compute="_compute_flow")

    @api.depends('measured_value1', 'measured_value2', 'measured_value3', 'measured_value4')
    def _compute_average(self):
        for record in self:
            measured_values = [
                record.measured_value1,
                record.measured_value2,
                record.measured_value3,
                record.measured_value4
            ]
            non_empty_values = [value for value in measured_values if value is not False]
            if non_empty_values:
                record.average_measured = sum(non_empty_values) / len(non_empty_values)
            else:
                record.average_measured = 0.0


    @api.depends('average_measured')
    def _compute_flow(self):
        for record in self:
            record.percent_flow = record.average_measured - 100

     #28 days Casting

    casting_28_name = fields.Char("Name",default="28 Days")
    # casting_28_visible = fields.Boolean("28 days Visible",compute="_compute_visible")

    casting_date_28days = fields.Date(string="Date of Casting")
    testing_date_28days = fields.Date(string="Date of Testing",compute="_compute_testing_date_28days")
    casting_28_days_tables = fields.One2many('flyash.casting.28days.line','parent_id',string="28 Days")
    average_casting_28days = fields.Float("Average",compute="_compute_average_28days")
    status_28days = fields.Boolean("Done")


    @api.depends('casting_28_days_tables.compressive_strength')
    def _compute_average_28days(self):
        for record in self:
            try:
                record.average_casting_28days = sum(record.casting_28_days_tables.mapped('compressive_strength')) / len(
                    record.casting_28_days_tables)
            except:
                record.average_casting_28days = 0


    @api.depends('casting_date_28days')
    def _compute_testing_date_28days(self):
        for record in self:
            if record.casting_date_28days:
                cast_date = fields.Datetime.from_string(record.casting_date_28days)
                testing_date = cast_date + timedelta(days=28)
                record.testing_date_28days = fields.Datetime.to_string(testing_date)
            else:
                record.testing_date_28days = False


    wt_of_cement_fly = fields.Integer(string="Weight of Cement (g)",default=500)
    wt_of_standared_grade1 = fields.Integer(string="Weight of Standard Sand (g)Grade-I",default=500)
    wt_of_standared_grade2 = fields.Integer(string="Weight of Standard Sand (g)Grade-II",default=500)
    wt_of_standared_grade3 = fields.Integer(string="Weight of Standard Sand (g)Grade-III",default=500)
    total_wieght = fields.Integer(string="Total Weight (g)",compute="_compute_total_wiegth")
    quantity_water_flyash = fields.Float(string="Quantity of Water (g)")


    @api.depends('wt_of_cement_fly','wt_of_standared_grade1','wt_of_standared_grade2','wt_of_standared_grade3')
    def _compute_total_wiegth(self):
        for record in self:
            record.total_wieght = record.wt_of_cement_fly + record.wt_of_standared_grade1 + record.wt_of_standared_grade2 + record.wt_of_standared_grade3


    measured_values1 = fields.Float(string="Measured Values")
    measured_values2 = fields.Float(string="Measured Values")
    measured_values3 = fields.Float(string="Measured Values")
    measured_values4 = fields.Float(string="Measured Values")

    average_measureds = fields.Float(string="Average",compute="_compute_averages")
    percent_flows = fields.Float(string="% Flow",compute="_compute_flows")

    @api.depends('measured_values1', 'measured_values2', 'measured_values3', 'measured_values4')
    def _compute_averages(self):
        for record in self:
            measured_values = [
                record.measured_values1,
                record.measured_values2,
                record.measured_values3,
                record.measured_values4
            ]
            non_empty_values = [value for value in measured_values if value is not False]
            if non_empty_values:
                record.average_measureds = sum(non_empty_values) / len(non_empty_values)
            else:
                record.average_measureds = 0.0


    @api.depends('average_measureds')
    def _compute_flows(self):
        for record in self:
            record.percent_flows = record.average_measureds - 100


     #28 days Casting

    casting_28_names = fields.Char("Name",default="28 Days")
    # casting_28_visible = fields.Boolean("28 days Visible",compute="_compute_visible")

    casting_dates_28days = fields.Date(string="Date of Casting")
    testing_dates_28days = fields.Date(string="Date of Testing",compute="_compute_testing_date_28dayss")
    casting_28_dayss_tables = fields.One2many('flyash.casting.28days.lines','parent_id',string="28 Days")
    average_casting_28dayss = fields.Float("Average",compute="_compute_average_28dayss")
    status_28dayss = fields.Boolean("Done")


    @api.depends('casting_28_dayss_tables.compressive_strengths')
    def _compute_average_28dayss(self):
        for record in self:
            try:
                record.average_casting_28dayss = sum(record.casting_28_dayss_tables.mapped('compressive_strengths')) / len(
                    record.casting_28_dayss_tables)
            except:
                record.average_casting_28dayss = 0


    @api.depends('casting_dates_28days')
    def _compute_testing_date_28dayss(self):
        for record in self:
            if record.casting_dates_28days:
                cast_date = fields.Datetime.from_string(record.casting_dates_28days)
                testing_date = cast_date + timedelta(days=28)
                record.testing_dates_28days = fields.Datetime.to_string(testing_date)
            else:
                record.testing_dates_28days = False



    compressive_strength_of_sample = fields.Float(string="Compressive Strength of  Sample (%)",compute="_compute_compressive_strength_of_sample")

    @api.depends('average_casting_28days','average_casting_28dayss')
    def _compute_compressive_strength_of_sample(self):
        for record in self:
            if record.average_casting_28dayss != 0:
                record.compressive_strength_of_sample = (record.average_casting_28days / record.average_casting_28dayss) * 100
            else:
                record.compressive_strength_of_sample = 0.0


    # Lime reactivity

    lime_reactivity = fields.Char("Name",default="Lime Reactivity")
    lime_reactivity_visible = fields.Boolean("Lime Visible",compute="_compute_visible")

    temp_percent_lime = fields.Float("Temperature %")
    humidity_percent_lime = fields.Float("Humidity %")
    start_date_lime = fields.Date("Start Date")
    end_date_lime = fields.Date("End Date")



    specific_gravity_fly_lime = fields.Float(string="Specific Gravity of Flyash (g)",compute="_compute_specific_gravity_flyash_lime")
    specific_gravity_of_lime = fields.Float(string="Specific Gravity of Lime (g)",compute="_compute_specific_gravity_lime")
    m = fields.Float(string="M",compute="_compute_m")
    wt_of_hydrent = fields.Integer(string="Weight of Hydrated Lime (g)",default=150)
    wt_of_fly_lime = fields.Float(string="Weight of Flyas (g)",compute="_compute_wt_of_fly_lime")
    wt_of_standard_grade_lime1 = fields.Integer(string="Weight of Standard Sand (g) Grade-I",default=450)
    wt_of_standard_grade_lime2 = fields.Integer(string="Weight of Standard Sand (g) Grade-II",default=450)
    wt_of_standard_grade_lime3 = fields.Integer(string="Weight of Standard Sand (g) Grade-III",default=450)
    quantity_water_lime = fields.Integer(string="Quantity of Water (g)")


    @api.depends('average_specific_gravity')
    def _compute_specific_gravity_flyash_lime(self):
        for record in self:
            record.specific_gravity_fly_lime = record.average_specific_gravity

    @api.depends('specific_gravity_cement1')
    def _compute_specific_gravity_lime(self):
        for record in self:
            record.specific_gravity_of_lime = record.specific_gravity_cement1

    @api.depends('specific_gravity_fly_lime','specific_gravity_of_lime')
    def _compute_m(self):
        for record in self:
            if record.specific_gravity_of_lime != 0:
                record.m = record.specific_gravity_fly_lime / record.specific_gravity_of_lime
            else:
                record.m = 0.0


    @api.depends('m')
    def _compute_wt_of_fly_lime(self):
        for record in self:
            record.wt_of_fly_lime = 300 * record.m


    measured_valuess1 = fields.Float(string="Measured Values")
    measured_valuess2 = fields.Float(string="Measured Values")
    measured_valuess3 = fields.Float(string="Measured Values")
    measured_valuess4 = fields.Float(string="Measured Values")

    average_measuredss = fields.Float(string="Average",compute="_compute_averagess")
    percent_flowss = fields.Float(string="% Flow",compute="_compute_flowss")

    @api.depends('measured_valuess1', 'measured_valuess2', 'measured_valuess3', 'measured_valuess4')
    def _compute_averagess(self):
        for record in self:
            measured_values = [
                record.measured_valuess1,
                record.measured_valuess2,
                record.measured_valuess3,
                record.measured_valuess4
            ]
            non_empty_values = [value for value in measured_values if value is not False]
            if non_empty_values:
                record.average_measuredss = sum(non_empty_values) / len(non_empty_values)
            else:
                record.average_measuredss = 0.0


    @api.depends('average_measuredss')
    def _compute_flowss(self):
        for record in self:
            record.percent_flowss = record.average_measuredss - 100


     #28 days Casting

    casting_28_namess = fields.Char("Name",default="28 Days")
    # casting_28_visible = fields.Boolean("28 days Visible",compute="_compute_visible")

    casting_dates_28dayss = fields.Date(string="Date of Casting")
    testing_dates_28dayss = fields.Date(string="Date of Testing",compute="_compute_testing_date_28daysss")
    casting_28_dayss_tabless = fields.One2many('flyash.casting.28days.liness','parent_id',string="28 Days")
    average_casting_28daysss = fields.Float("Average",compute="_compute_average_28daysss")
    compressive_strength_28_days = fields.Float("Compressive Strength",compute="_compute_compressive_strength_28dayss")
    status_28daysss = fields.Boolean("Done")


    @api.depends('casting_28_dayss_tabless.compressive_strengthss')
    def _compute_average_28daysss(self):
        for record in self:
            try:
                record.average_casting_28daysss = sum(record.casting_28_dayss_tabless.mapped('compressive_strengthss')) / len(
                    record.casting_28_dayss_tabless)
            except:
                record.average_casting_28daysss = 0


    @api.depends('casting_dates_28dayss')
    def _compute_testing_date_28daysss(self):
        for record in self:
            if record.casting_dates_28dayss:
                cast_date = fields.Datetime.from_string(record.casting_dates_28dayss)
                testing_date = cast_date + timedelta(days=28)
                record.testing_dates_28dayss = fields.Datetime.to_string(testing_date)
            else:
                record.testing_dates_28dayss = False

    @api.depends('average_casting_28daysss')
    def _compute_compressive_strength_28dayss(self):
        for record in self:
            integer_part = math.floor(record.average_casting_28daysss)
            fractional_part = record.average_casting_28daysss - integer_part
            if fractional_part > 0 and fractional_part <= 0.25:
                record.compressive_strength_28_days = integer_part
            elif fractional_part > 0.25 and fractional_part <= 0.75:
                record.compressive_strength_28_days = integer_part + 0.5
            elif fractional_part > 0.75 and fractional_part <= 1:
                record.compressive_strength_28_days = integer_part + 1
            else:
                record.compressive_strength_28_days = 0



     # Fineness Air Permeability Method

    fineness_blaine_name = fields.Char("Name",default="Fineness By Blaine Air Permeability Method")
    fineness_blaine_visible = fields.Boolean("Fineness Blaine Visible",compute="_compute_visible")

    temp_percent_fineness = fields.Float("Temperature %")
    humidity_percent_fineness = fields.Float("Humidity %")
    start_date_fineness = fields.Date("Start Date")
    end_date_fineness = fields.Date("End Date")

    weight_of_mercury_before_trial1 = fields.Float("Weight of mercury before placing the sample in the permeability cell  (m₁),g." ,default=84.160,digits=(16, 3))
    weight_of_mercury_before_trial2 = fields.Float("Weight of mercury before placing the sample in the permeability cell  (m₁),g.",default=84.140,digits=(16, 3))
    

    weight_of_mercury_after_trail1 = fields.Float("Weight of mercury after palcing the sample in the permeability cell  (m₂),g.",default=51.740,digits=(16, 3))
    weight_of_mercury_after_trail2 = fields.Float("Weight of mercury after palcing the sample in the permeability cell  (m₂),g.",default=51.760,digits=(16, 3))

    density_of_mercury = fields.Float("Density of mercury , g/cm3",default=13.53)

    bed_volume_trial1 = fields.Float("Bed Volume (V=m₂-m₁/D),cm3.",compute="_compute_bed_volume_trial1",digits=(16, 3))
    bed_volume_trial2 = fields.Float("Bed Volume (V=m₂-m₁/D),cm3.",compute="_compute_bed_volume_trial2",digits=(16, 3))

    average_bed_volume = fields.Float("Average Bed Volume (cm3)",compute="_compute_average_bed_volume",digits=(16, 3))

    difference_between_2_values = fields.Float("Difference between the two Values",compute="_compute_difference_bed_volume",digits=(16, 3))

    mass_of_sample_taken_fineness = fields.Float("mass of sample taken (g)" ,compute="_compute_mass_of_sample_taken_fineness")

    time_fineness_trial1 = fields.Float("Time(t),sec.",default=46.68)
    time_fineness_trial2 = fields.Float("Time(t),sec.",default=45.53)
    time_fineness_trial3 = fields.Float("Time(t),sec.",default=46.76)
    average_time_fineness = fields.Float("Average Time(tₒ),Sec",compute="_compute_time_average_fineness")

    specific_gravity_fineness = fields.Float(string="Specific Gravity",compute="_compute_specific_gravity_fineness")
    mass_of_sample_fineness = fields.Float(string="mass of sample taken (g)",compute="_compute_mass_of_sample_fineness")

    time_sample_trial1 = fields.Float("Time(t),sec.")
    time_sample_trial2 = fields.Float("Time(t),sec.")
    time_sample_trial3 = fields.Float("Time(t),sec.")
    average_sample_time = fields.Float("Average Time(tₒ),Sec",compute="_compute_average_sample_time")

    ss = fields.Float(string="Sₛ is the Specific surface of Standard Sample (m²/kg)",default=333)
    ps = fields.Float(string="ρₛ is the Density of Standard sample",default=2.23)
    p = fields.Float(string="ρ is the Density of Test sample",compute="_compute_specific_gravity_p")
    ts = fields.Float(string="√Ƭₛ is the Mean of three measured times of Standard Sample",compute="_compute_ts")
    t = fields.Float(string="√Ƭ is the Mean of three measured times of Test sample",compute="_compute_t")
    specific_surface = fields.Float("S is the Specific surface of Test sample (m²/kg)",compute="_compute_specific_surface")
    fineness_air_permeability = fields.Float("Fineness By Blaine Air Permeability Method (m2/kg)",compute="_compute_fineness_air_permeability")




    @api.depends('weight_of_mercury_before_trial1','weight_of_mercury_after_trail1','density_of_mercury')
    def _compute_bed_volume_trial1(self):
        if self.density_of_mercury !=0:
            self.bed_volume_trial1 = (self.weight_of_mercury_before_trial1 - self.weight_of_mercury_after_trail1) / self.density_of_mercury
        else:
            self.bed_volume_trial1 = 0
    
    @api.depends('weight_of_mercury_before_trial2','weight_of_mercury_after_trail2','density_of_mercury')
    def _compute_bed_volume_trial2(self):
        if self.density_of_mercury !=0:
            self.bed_volume_trial2 = (self.weight_of_mercury_before_trial2 - self.weight_of_mercury_after_trail2) / self.density_of_mercury
        else:
            self.bed_volume_trial2 = 0
    
    @api.depends('bed_volume_trial1','bed_volume_trial2')
    def _compute_average_bed_volume(self):
        self.average_bed_volume = round(((self.bed_volume_trial1 + self.bed_volume_trial2) / 2),3)
    
    @api.depends('bed_volume_trial1','bed_volume_trial2')
    def _compute_difference_bed_volume(self):
        self.difference_between_2_values = self.bed_volume_trial1 - self.bed_volume_trial2


    @api.depends('average_bed_volume')
    def _compute_mass_of_sample_taken_fineness(self):
        for record in self:
            record.mass_of_sample_taken_fineness = 0.5 * 2.23 * record.average_bed_volume

    @api.depends('time_fineness_trial1','time_fineness_trial2','time_fineness_trial3')
    def _compute_time_average_fineness(self):
        self.average_time_fineness = (self.time_fineness_trial1 + self.time_fineness_trial2 + self.time_fineness_trial3)/3


    @api.depends('average_specific_gravity')
    def _compute_specific_gravity_fineness(self):
        for record in self:
            record.specific_gravity_fineness = record.average_specific_gravity

    @api.depends('specific_gravity_fineness','average_bed_volume')
    def _compute_mass_of_sample_fineness(self):
        for record in self:
            record.mass_of_sample_fineness = 0.5 * record.specific_gravity_fineness * record.average_bed_volume


    @api.depends('time_sample_trial1','time_sample_trial2','time_sample_trial3')
    def _compute_average_sample_time(self):
        self.average_sample_time = (self.time_sample_trial1 + self.time_sample_trial2 + self.time_sample_trial3)/3



    @api.depends('average_specific_gravity')
    def _compute_specific_gravity_p(self):
        for record in self:
            record.p = record.average_specific_gravity


    @api.depends('average_time_fineness')
    def _compute_ts(self):
        for record in self:
            if record.average_time_fineness:
                record.ts = record.average_time_fineness ** 0.5
            else:
                record.ts = 0.0

    @api.depends('average_sample_time')
    def _compute_t(self):
        for record in self:
            if record.average_sample_time:
                record.t = record.average_sample_time ** 0.5
            else:
                record.t = 0.0


    @api.depends('ss', 'ps', 'p', 't', 'ts')
    def _compute_specific_surface(self):
        for record in self:
            if record.ss and record.ps and record.p and record.t and record.ts:
                specific_surface_value = (record.ss * record.ps * record.t) / (record.p * record.ts)
                record.specific_surface = round(specific_surface_value, 2)
            else:
                record.specific_surface = 0.0

    @api.depends('specific_surface')
    def _compute_fineness_air_permeability(self):
        for record in self:
            if record.specific_surface:
                rounded_specific_surface = round(record.specific_surface, 0)  # Round to nearest integer
                record.fineness_air_permeability = max(360.0, rounded_specific_surface)  # Ensure value is at least 360
            else:
                record.fineness_air_permeability = 0.0

    








   
   

        








   

           
       



    ### Compute Visible
    @api.depends('tests')
    def _compute_visible(self):
        normal_consistency_test = self.env['mechanical.cement.test'].search([('name', '=', 'Normal Consistency')])
        setting_time_test = self.env['mechanical.cement.test'].search([('name', '=', 'Setting Time')])
        particles_retained_test = self.env['mechanical.cement.test'].search([('name', '=', 'Particles retained on 45 micron IS sieve (wet sieving)')])
        soundness_test = self.env['mechanical.cement.test'].search([('name', '=', 'Soundness')])
        specific_gravity_test = self.env['mechanical.cement.test'].search([('name', '=', 'Specigic Gravity')])
        compressive_test = self.env['mechanical.cement.test'].search([('name', '=', 'Compressive Strength')])
        lime_reactivity_test = self.env['mechanical.cement.test'].search([('name', '=', 'Lime Reactivity')])
        # # casting_3days_test = self.env['mechanical.cement.test'].search([('name', '=', '3 Days')])
        # # casting_7days_test = self.env['mechanical.cement.test'].search([('name', '=', '7 Days')])
        # # casting_28days_test = self.env['mechanical.cement.test'].search([('name', '=', '28 Days')])
        fineness_blaine = self.env['mechanical.cement.test'].search([('name', '=', 'Fineness (Blaine)')])
 
        for record in self:
            record.normal_consistency_visible = False
            record.setting_time_visible  = False  
            record.particles_retained_visible = False
            record.soundness_visible = False
            record.specigic_gravity_visible = False
            record.compressive_visible = False
            record.lime_reactivity_visible = False
            record.fineness_blaine_visible = False

            if setting_time_test in record.tests:
                record.normal_consistency_visible = True
                record.setting_time_visible  = True
            if particles_retained_test in record.tests:
                record.particles_retained_visible = True
            if soundness_test in record.tests:
                record.normal_consistency_visible = True
                record.soundness_visible = True
            if specific_gravity_test in record.tests:
                 record.specigic_gravity_visible = True
            if compressive_test in record.tests:
                record.specigic_gravity_visible = True
                record.normal_consistency_visible = True
                record.compressive_visible = True
            if lime_reactivity_test in record.tests:
                record.normal_consistency_visible = True
                record.lime_reactivity_visible = True
            # if dry_sieving_test in record.tests:
            #     record.dry_sieving_visible = True
            if fineness_blaine in record.tests:
                record.fineness_blaine_visible = True
               


    @api.model
    def create(self, vals):
        # import wdb;wdb.set_trace()
        record = super(FlyaschNormalConsistency, self).create(vals)
        record.get_all_fields()
        record.eln_ref.write({'model_id':record.id})
        return record







    @api.depends('eln_ref')
    def _compute_sample_parameters(self):
        # records = self.env['lerm.eln'].search([('id','=', record.eln_id.id)]).parameters_result
        # print("records",records)
        # self.sample_parameters = records
        for record in self:
            records = record.eln_ref.parameters_result.parameter.ids
            record.sample_parameters = records
            print("Records",records)



    def get_all_fields(self):
        record = self.env['mechanical.flyasch.normalconsistency'].browse(self.ids[0])
        field_values = {}
        for field_name, field in record._fields.items():
            field_value = record[field_name]
            field_values[field_name] = field_value

        return field_values




class CementTest(models.Model):
    _name = "mechanical.cement.test"
    _rec_name = "name"
    name = fields.Char("Name")


class ParticlesRetainedLine(models.Model):
    _name= "particles.retained.line"

    parent_id = fields.Many2one('mechanical.flyasch.normalconsistency')

    sr_no = fields.Integer(string="Sr.No.", readonly=True, copy=False, default=1)
    sample_wt = fields.Float("Sample Weight (g)",default=100)
    retained_wt = fields.Float("Retained Weight on 45 mic sieve (g)")
    wt_retained = fields.Float("% Weight Retained",compute="_compute_retained")

    @api.depends('retained_wt','sample_wt')
    def _compute_retained(self):
        for record in self:
            if record.sample_wt != 0:
                record.wt_retained = (record.retained_wt / record.sample_wt) * 100



    @api.model
    def create(self, vals):
        # Set the serial_no based on the existing records for the same parent
        if vals.get('parent_id'):
            existing_records = self.search([('parent_id', '=', vals['parent_id'])])
            if existing_records:
                max_serial_no = max(existing_records.mapped('sr_no'))
                vals['sr_no'] = max_serial_no + 1

        return super(ParticlesRetainedLine, self).create(vals)

    def _reorder_serial_numbers(self):
        # Reorder the serial numbers based on the positions of the records in child_lines
        records = self.sorted('id')
        for index, record in enumerate(records):
            record.sr_no = index + 1

class SoundnessflyashLine(models.Model):
    _name= "flyash.soundness.line"

    parent_id = fields.Many2one('mechanical.flyasch.normalconsistency')
    sr_no = fields.Integer(string="Sr.No.", readonly=True, copy=False, default=1)
    initial_distance = fields.Float("Intial distance separating the indicator points (L1).mm")
    final_distance = fields.Float("Final distance separating the indicator points (L2).mm")
    expansion = fields.Float("Expansion",compute="_compute_expansion")

    @api.depends('initial_distance','final_distance')
    def _compute_expansion(self):
        for record in self:
            record.expansion = record.final_distance - record.initial_distance


    @api.model
    def create(self, vals):
        # Set the serial_no based on the existing records for the same parent
        if vals.get('parent_id'):
            existing_records = self.search([('parent_id', '=', vals['parent_id'])])
            if existing_records:
                max_serial_no = max(existing_records.mapped('sr_no'))
                vals['sr_no'] = max_serial_no + 1

        return super(SoundnessflyashLine, self).create(vals)

    def _reorder_serial_numbers(self):
        # Reorder the serial numbers based on the positions of the records in child_lines
        records = self.sorted('id')
        for index, record in enumerate(records):
            record.sr_no = index + 1


class Casting28DaysLine(models.Model):
    _name = "flyash.casting.28days.line"

    parent_id = fields.Many2one('mechanical.flyasch.normalconsistency')

    length = fields.Float("Length in mm")
    width = fields.Float("Width in mm")
    crosssectional_area = fields.Float("Crosssectional Area",compute="_compute_crosssectional_area")
    wt_of_cement_cube = fields.Float("wt of Cement Cube in gm")
    crushing_load = fields.Float("Crushing Load in KN")
    compressive_strength = fields.Float("Compressive Strength (N/mm²)",compute="_compute_compressive_strength")

    @api.depends('length','width')
    def _compute_crosssectional_area(self):
        for record in self:
            record.crosssectional_area = record.length * record.width

    @api.depends('crosssectional_area', 'crushing_load')
    def _compute_compressive_strength(self):
        for record in self:
            if record.crosssectional_area != 0:
                record.compressive_strength = (record.crushing_load / record.crosssectional_area) * 1000
            else:
                record.compressive_strength = 0.0
                
class Casting28DaysLines(models.Model):
    _name = "flyash.casting.28days.lines"

    parent_id = fields.Many2one('mechanical.flyasch.normalconsistency')

    lengths = fields.Float("Length in mm")
    widths = fields.Float("Width in mm")
    crosssectional_areas = fields.Float("Crosssectional Area",compute="_compute_crosssectional_areas")
    wt_of_cement_cubes = fields.Float("wt of Cement Cube in gm")
    crushing_loads = fields.Float("Crushing Load in KN")
    compressive_strengths = fields.Float("Compressive Strength (N/mm²)",compute="_compute_compressive_strengths")

    @api.depends('lengths','widths')
    def _compute_crosssectional_areas(self):
        for record in self:
            record.crosssectional_areas = record.lengths * record.widths

    @api.depends('crosssectional_areas', 'crushing_loads')
    def _compute_compressive_strengths(self):
        for record in self:
            if record.crosssectional_areas != 0:
                record.compressive_strengths = (record.crushing_loads / record.crosssectional_areas) * 1000
            else:
                record.compressive_strengths = 0


class Casting28DaysLiness(models.Model):
    _name = "flyash.casting.28days.liness"

    parent_id = fields.Many2one('mechanical.flyasch.normalconsistency')

    lengthss = fields.Float("Length in mm")
    widthss = fields.Float("Width in mm")
    crosssectional_areass = fields.Float("Crosssectional Area",compute="_compute_crosssectional_areass")
    wt_of_cement_cubess = fields.Float("wt of Cement Cube in gm")
    crushing_loadss = fields.Float("Crushing Load in KN")
    compressive_strengthss = fields.Float("Compressive Strength (N/mm²)",compute="_compute_compressive_strengthss")

    @api.depends('lengthss','widthss')
    def _compute_crosssectional_areass(self):
        for record in self:
            record.crosssectional_areass = record.lengthss * record.widthss

    @api.depends('crosssectional_areass', 'crushing_loadss')
    def _compute_compressive_strengthss(self):
        for record in self:
            if record.crosssectional_areass != 0:
                record.compressive_strengthss = (record.crushing_loadss / record.crosssectional_areass) * 1000
            else:
                record.compressive_strengthss = 0







