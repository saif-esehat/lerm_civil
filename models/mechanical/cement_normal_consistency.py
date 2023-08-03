from odoo import api, fields, models
from odoo.exceptions import UserError,ValidationError
from datetime import datetime



class CementNormalConsistency(models.Model):
    _name = "mechanical.cement.normalconsistency"
    _inherit = "lerm.eln"
    _rec_name = "name"


    name = fields.Char("Name",default="Cement")
    parameter_id = fields.Many2one('eln.parameters.result', string="Parameter")

    sample_parameters = fields.Many2many('eln.parameters.result',string="Parameters",compute="_compute_sample_parameters")

    temp_percent = fields.Float("Temperature %")
    humidity_percent = fields.Float("Humidity %")

    ## Normal Consistency

    tests = fields.Many2many("mechanical.cement.test",string="Tests")

    normal_consistency_name = fields.Char("Name",default="Normal Consistency")
    normal_consistency_visible = fields.Boolean("Normal Consistency Visible",compute="_compute_visible")

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


    #Density

    
    density_name = fields.Char("Name",default="Density")
    density_visible = fields.Boolean("Setting Time Visible",compute="_compute_visible")

    wt_of_cement_density_trial1 = fields.Float("Wt. of Cement(g)",default=64)
    wt_of_cement_density_trial2 = fields.Float("Wt. of Cement(g)",default=64)

    initial_volume_kerosene_trial1 = fields.Float("Initial Volume of kerosine (ml)V1")
    initial_volume_kerosene_trial2 = fields.Float("Initial Volume of kerosine (ml)V1")

    final_volume_kerosene_trial1 = fields.Float("Final Volume of kerosine and Cement (After immersion in constant water bath) (ml) V2")
    final_volume_kerosene_trial2 = fields.Float("Final Volume of kerosine and Cement (After immersion in constant water bath) (ml) V2")

    displaced_volume_trial1 = fields.Float("Displaced volume (cm³)",compute="_compute_displaced_volume_trial1")
    displaced_volume_trial2 = fields.Float("Displaced volume (cm³)",compute="_compute_displaced_volume_trial2")

    density_trial1 = fields.Float("Density (g/cm³)",compute="_compute_density_trial1")
    density_trial2 = fields.Float("Density (g/cm³)",compute="_compute_density_trial2")

    average_density = fields.Float("Average",compute="_compute_density_average")

    @api.depends('initial_volume_kerosene_trial1','final_volume_kerosene_trial1')
    def _compute_displaced_volume_trial1(self):
        self.displaced_volume_trial1 = self.final_volume_kerosene_trial1 - self.initial_volume_kerosene_trial1

    @api.depends('initial_volume_kerosene_trial2','final_volume_kerosene_trial2')
    def _compute_displaced_volume_trial2(self):
         self.displaced_volume_trial2 = self.final_volume_kerosene_trial2 - self.initial_volume_kerosene_trial2


    @api.depends('wt_of_cement_density_trial1','displaced_volume_trial1')
    def _compute_density_trial1(self):
        try:
            self.density_trial1 = self.wt_of_cement_density_trial1 / self.displaced_volume_trial1
        except:
            self.density_trial1 = 0

    @api.depends('wt_of_cement_density_trial2','displaced_volume_trial2')
    def _compute_density_trial2(self):
        try:
            self.density_trial2 = self.wt_of_cement_density_trial2 / self.displaced_volume_trial2
        except:
            self.density_trial2 = 0

    

    @api.depends('density_trial1','density_trial2')
    def _compute_density_average(self):
        self.average_density = (self.density_trial1 + self.density_trial2)/2

    # Density End  

    # Soundness Test
    soundness_name = fields.Char("Name",default="Soundness")
    soundness_visible = fields.Boolean("Soundness Visible",compute="_compute_visible")

    wt_of_cement_soundness = fields.Float("Weight of Cement(g)",default=100)
    wt_of_water_req_soundness = fields.Float("Weight of water required(g)",compute="_compute_water_weight_soundness")

    soundness_table = fields.One2many('cement.soundness.line','parent_id',string="Soundness")
    average_soundness = fields.Float("Average",compute="_compute_average_soundness")
    expansion_soundness = fields.Float("Expansion(mm)")

    @api.depends('soundness_table.expansion')
    def _compute_average_soundness(self):
        for record in self:
            try:
                record.average_soundness = sum(record.soundness_table.mapped('expansion'))/len(record.soundness_table)
            except:
                record.average_soundness = 0

    @api.depends('wt_of_cement_soundness','normal_consistency_trial1')
    def _compute_water_weight_soundness(self):
        self.wt_of_water_req_soundness = (((0.78*self.normal_consistency_trial1)/100)*self.wt_of_cement_soundness)


    # @api.constrains('soundness_table')
    # def check_soundness_table_limit(self):
    #     max_limit = 2  # Set the maximum limit here
    #     for record in self:
    #         if len(record.soundness_table) > max_limit:
    #             raise ValidationError(f"Maximum limit of {max_limit} rows exceeded for Related Records.")


    #Dry Sieving 

    
    dry_sieving_name = fields.Char("Name",default="Dry Sieving")
    dry_sieving_visible = fields.Boolean("Dry Sieving Visible",compute="_compute_visible")

    dry_sieving_table = fields.One2many('cement.dry.sieving.line','parent_id',string="Dry Sieving")
    average_fineness = fields.Float("Average",compute="_compute_average_fineness")
    fineness_dry_sieving = fields.Float("Fineness by dry sieving %")


    @api.depends('dry_sieving_table.fineness')
    def _compute_average_fineness(self):
        for record in self:
            try:
                record.average_fineness = sum(record.dry_sieving_table.mapped('fineness'))/len(record.dry_sieving_table)
            except:
                record.average_fineness = 0

    # Compressive Strength 

    compressive_name = fields.Char("Name",default="Compressive Strength")
    compressive_visible = fields.Boolean("Compressive Visible",compute="_compute_visible")

    wt_of_cement_compressive = fields.Float("Wt. of Cement(g)",default=200)
    wt_of_standard_sand_grade1 = fields.Float("Weight of Standard Sand (g) Grade-I",default=200)
    wt_of_standard_sand_grade2 = fields.Float("Weight of Standard Sand (g) Grade-II",default=200)
    wt_of_standard_sand_grade3 = fields.Float("Weight of Standard Sand (g) Grade-III",default=200)
    total_weight = fields.Float("Total Weight",compute="compute_total_weight_compressive")
    quantity_of_water = fields.Float("Quantity of Water",compute="_compute_quantity_of_water")

    @api.depends('wt_of_cement_compressive','wt_of_standard_sand_grade1','wt_of_standard_sand_grade2','wt_of_standard_sand_grade3')
    def compute_total_weight_compressive(self):
        self.total_weight = self.wt_of_cement_compressive + self.wt_of_standard_sand_grade1 + self.wt_of_standard_sand_grade2 + self.wt_of_standard_sand_grade3 

    @api.depends('normal_consistency_trial1','total_weight')
    def _compute_quantity_of_water(self):
        self.quantity_of_water = ((self.normal_consistency_trial1/4 +3)/100)*self.total_weight

    
    # 3 days Casting
    casting_3_name = fields.Char("Name",default="3 Days")
    casting_3_visible = fields.Boolean("3 days Visible",compute="_compute_visible")

    casting_3_days_tables = fields.One2many('cement.casting.3days.line','parent_id',string="3 Days")
    average_casting_3days = fields.Float("Average",compute="_compute_average_3days")
    compressive_strength_3_days = fields.Float("Compressive Strength")

    @api.depends('casting_3_days_tables.compressive_strength')
    def _compute_average_3days(self):
        for record in self:
            try:
                record.average_casting_3days = sum(record.casting_3_days_tables.mapped('compressive_strength'))/len(record.casting_3_days_tables)
            except:
                record.average_casting_3days = 0

    # 7 Days Casting

    casting_7_name = fields.Char("Name",default="7 Days")
    casting_7_visible = fields.Boolean("7 days Visible",compute="_compute_visible")

    casting_7_days_tables = fields.One2many('cement.casting.7days.line','parent_id',string="7 Days")
    average_casting_7days = fields.Float("Average",compute="_compute_average_7days")
    compressive_strength_7_days = fields.Float("Compressive Strength")

    @api.depends('casting_7_days_tables.compressive_strength')
    def _compute_average_7days(self):
        for record in self:
            try:
                record.average_casting_7days = sum(record.casting_7_days_tables.mapped('compressive_strength'))/len(record.casting_7_days_tables)
            except:
                record.average_casting_7days = 0


    #28 days Casting

    casting_28_name = fields.Char("Name",default="28 Days")
    casting_28_visible = fields.Boolean("28 days Visible",compute="_compute_visible")

    casting_28_days_tables = fields.One2many('cement.casting.28days.line','parent_id',string="28 Days")
    average_casting_28days = fields.Float("Average",compute="_compute_average_28days")
    compressive_strength_28_days = fields.Float("Compressive Strength")

    @api.depends('casting_28_days_tables.compressive_strength')
    def _compute_average_28days(self):
        for record in self:
            try:
                record.average_casting_28days = sum(record.casting_28_days_tables.mapped('compressive_strength'))/len(record.casting_28_days_tables)
            except:
                record.average_casting_28days = 0

    # Fineness Air Permeability Method

    fineness_blaine_name = fields.Char("Name",default="Fineness By Blaine Air Permeability Method")
    fineness_blaine_visible = fields.Boolean("Fineness Blaine Visible",compute="_compute_visible")

    weight_of_mercury_before_trial1 = fields.Float("Weight of mercury before placing the sample in the permeability cell  (m₁),g." ,default=83.150,digits=(16, 3))
    weight_of_mercury_before_trial2 = fields.Float("Weight of mercury before placing the sample in the permeability cell  (m₁),g.",default=83.130,digits=(16, 3))
    

    weight_of_mercury_after_trail1 = fields.Float("Weight of mercury after palcing the sample in the permeability cell  (m₂),g.",default=56.730,digits=(16, 3))
    weight_of_mercury_after_trail2 = fields.Float("Weight of mercury after palcing the sample in the permeability cell  (m₂),g.",default=56.734,digits=(16, 3))

    density_of_mercury = fields.Float("Density of mercury , g/cm3",default=13.53,digits=(16, 3))

    bed_volume_trial1 = fields.Float("Bed Volume (V=m₂-m₁/D),cm3.",compute="_compute_bed_volume_trial1",digits=(16, 3))
    bed_volume_trial2 = fields.Float("Bed Volume (V=m₂-m₁/D),cm3.",compute="_compute_bed_volume_trial2",digits=(16, 3))

    average_bed_volume = fields.Float("Average Bed Volume (cm3)",compute="_compute_average_bed_volume",digits=(16, 3))

    difference_between_2_values = fields.Float("Difference between the two Values",compute="_compute_difference_bed_volume",digits=(16, 3))

    density_fineness_reference = fields.Float("Density" ,compute="_compute_density_fineness")
    mass_of_sample_taken_fineness_reference = fields.Float("mass of sample taken (g)" ,compute="_compute_mass_taken_reference")

    time_fineness_trial1 = fields.Float("Time(t),sec.",default=48)
    time_fineness_trial2 = fields.Float("Time(t),sec.",default=47)
    time_fineness_trial3 = fields.Float("Time(t),sec.",default=49)
    average_time_fineness = fields.Float("Average Time(tₒ),Sec",compute="_compute_time_average_fineness")

    specific_surface_of_reference_sample = fields.Float("S0 is the Specific surface of reference sample (m²/kg)",default=274) 
    air_viscosity_of_three_temp = fields.Float("ɳₒ is the Air viscosity at the mean of the three temperatures",default=0.001359,digits=(16, 6))
    density_of_reference_sample = fields.Float("ρ0 is the Density of reference sample  (g/cm3)",default=3.16)
    mean_of_three_measured_times = fields.Float("t0 is the Mean of three measured times (sec)",default=48.00)
    apparatus_constant = fields.Float("Apparatus Constant(k)",compute="_compute_apparatus_constant")

    density_fineness_calculated = fields.Float("Density",compute="_compute_density_calculated")
    mass_of_sample_taken_fineness_calculated = fields.Float("mass of sample taken (g)",compute="_compute_mass_sample_calculated")

    time_sample_trial1 = fields.Float("Time(t),sec.")
    time_sample_trial2 = fields.Float("Time(t),sec.")
    time_sample_trial3 = fields.Float("Time(t),sec.")
    average_sample_time = fields.Float("Average Time(tₒ),Sec",compute="_compute_average_sample_time")

    fineness_of_sample = fields.Float("Fineness of Sample",compute="_compute_fineness_of_sample")
    fineness_air_permeability = fields.Float("Fineness By Blaine Air Permeability Method (m2/kg)")

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

    @api.depends('density_of_reference_sample')
    def _compute_density_fineness(self):
        self.density_fineness_reference = self.density_of_reference_sample

    @api.depends('average_bed_volume','density_fineness_reference')
    def _compute_mass_taken_reference(self):
        self.mass_of_sample_taken_fineness_reference = 0.5*self.average_bed_volume*self.density_fineness_reference

    @api.depends('time_fineness_trial1','time_fineness_trial2','time_fineness_trial3')
    def _compute_time_average_fineness(self):
        self.average_time_fineness = (self.time_fineness_trial1 + self.time_fineness_trial2 + self.time_fineness_trial3)/3

    @api.depends('specific_surface_of_reference_sample','air_viscosity_of_three_temp','density_of_reference_sample','mean_of_three_measured_times')
    def _compute_apparatus_constant(self):
        if self.mean_of_three_measured_times != 0:
            self.apparatus_constant = 1.414*self.specific_surface_of_reference_sample*self.density_of_reference_sample*((self.air_viscosity_of_three_temp)/(self.mean_of_three_measured_times**0.5))
        else:
            self.apparatus_constant = 0

    @api.depends('average_density')
    def _compute_density_calculated(self):
        self.density_fineness_calculated = self.average_density

    @api.depends('average_bed_volume','density_fineness_calculated')
    def _compute_mass_sample_calculated(self):
        self.mass_of_sample_taken_fineness_calculated = 0.5*self.average_bed_volume*self.density_fineness_calculated

    @api.depends('time_sample_trial1','time_sample_trial2','time_sample_trial3')
    def _compute_average_sample_time(self):
        self.average_sample_time = (self.time_sample_trial1 + self.time_sample_trial2 + self.time_sample_trial3)/3

    @api.depends('apparatus_constant','average_sample_time','density_fineness_calculated')
    def _compute_fineness_of_sample(self):
        if self.density_fineness_calculated != 0:
            self.fineness_of_sample = (521.08*self.apparatus_constant*(self.average_sample_time**0.5))/self.density_fineness_calculated
        else:
            self.fineness_of_sample = 0


            
    ### Compute Visible
    @api.depends('tests')
    def _compute_visible(self):
        normal_consistency_test = self.env['mechanical.cement.test'].search([('name', '=', 'Normal Consistency')])
        setting_time_test = self.env['mechanical.cement.test'].search([('name', '=', 'Setting Time')])
        density_test = self.env['mechanical.cement.test'].search([('name', '=', 'Density')])
        compressive_test = self.env['mechanical.cement.test'].search([('name', '=', 'Compressive Strength')])
        soundness_test = self.env['mechanical.cement.test'].search([('name', '=', 'Soundness')])
        dry_dieving_test = self.env['mechanical.cement.test'].search([('name', '=', 'Dry Sieve')])
        casting_3days_test = self.env['mechanical.cement.test'].search([('name', '=', '3 Days')])
        casting_7days_test = self.env['mechanical.cement.test'].search([('name', '=', '7 Days')])
        casting_28days_test = self.env['mechanical.cement.test'].search([('name', '=', '28 Days')])
        fineness_blaine = self.env['mechanical.cement.test'].search([('name', '=', 'Fineness (Blaine)')])
 
        for record in self:
            record.normal_consistency_visible = normal_consistency_test in record.tests
            record.setting_time_visible = setting_time_test in record.tests
            record.density_visible = density_test in record.tests
            record.compressive_visible = compressive_test in record.tests
            record.soundness_visible = soundness_test in record.tests
            record.dry_sieving_visible = dry_dieving_test in record.tests
            record.casting_3_visible = casting_3days_test in record.tests
            record.casting_7_visible = casting_7days_test in record.tests
            record.casting_28_visible = casting_28days_test in record.tests
            record.fineness_blaine_visible = fineness_blaine in record.tests







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

    def _compute_sample_parameters(self):
        records = self.env['lerm.eln'].search([])

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


class SoundnessCementLine(models.Model):
    _name= "cement.soundness.line"

    parent_id = fields.Many2one('mechanical.cement.normalconsistency')
    initial_distance = fields.Float("Intial distance separating the indicator points (L1).mm")
    final_distance = fields.Float("Final distance separating the indicator points (L2).mm")
    expansion = fields.Float("Expansion",compute="_compute_expansion")

    @api.depends('initial_distance','final_distance')
    def _compute_expansion(self):
        for record in self:
            record.expansion = record.final_distance - record.initial_distance

class DrySievingLine(models.Model):
    _name = "cement.dry.sieving.line"

    parent_id = fields.Many2one('mechanical.cement.normalconsistency')
    sample_weight_fineness = fields.Float("Sample Weight(g)",default=10)
    retained_weight = fields.Float("Retained Weight on 90 mic sieve (g)")
    fineness = fields.Float("Fineness by dry sieving %",compute="_compute_fineness")

    @api.depends('retained_weight','sample_weight_fineness')
    def _compute_fineness(self):
        for record in self:
            if record.sample_weight_fineness != 0:
                record.fineness = (record.retained_weight / record.sample_weight_fineness )*100
            else:
                record.fineness = 0


class Casting3DaysLine(models.Model):
    _name = "cement.casting.3days.line"

    parent_id = fields.Many2one('mechanical.cement.normalconsistency',string="Parent Id")
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

    @api.depends('crosssectional_area','crushing_load')
    def _compute_compressive_strength(self):
        for record in self:
            if record.crosssectional_area != 0:
                record.compressive_strength = (record.crushing_load / record.crosssectional_area)*1000
            else:
                record.compressive_strength = 0

class Casting7DaysLine(models.Model):
    _name = "cement.casting.7days.line"

    parent_id = fields.Many2one('mechanical.cement.normalconsistency')

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

    @api.depends('crosssectional_area','crushing_load')
    def _compute_compressive_strength(self):
        for record in self:
            if record.crosssectional_area != 0:
                record.compressive_strength = (self.crushing_load / self.crosssectional_area)*1000
            else:
                record.compressive_strength = 0

class Casting28DaysLine(models.Model):
    _name = "cement.casting.28days.line"

    parent_id = fields.Many2one('mechanical.cement.normalconsistency')

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

    @api.depends('crosssectional_area','crushing_load')
    def _compute_compressive_strength(self):
        for record in self:
            if record.crosssectional_area != 0:
                record.compressive_strength = (self.crushing_load / self.crosssectional_area)*1000
            else:
                record.compressive_strength = 0