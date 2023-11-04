from odoo import api, fields, models
from odoo.exceptions import UserError,ValidationError
import math

class ChemicalFlyAsh(models.Model):
    _name = "chemical.flyash"
    _inherit = "lerm.eln"
    _rec_name = "name"

    name = fields.Char("Name",default="Fly Ash")
    parameter_id = fields.Many2one('eln.parameters.result',string="Parameter")
    sample_parameters = fields.Many2many('lerm.parameter.master',string="Parameters",compute="_compute_sample_parameters",store=True)
    eln_ref = fields.Many2one('lerm.eln',string="Eln")


    # % Silica

    Silica_name = fields.Char("Name",default="% Silica")
    Silica_visible = fields.Boolean("% Silica",compute="_compute_visible")

    siliceous1 = fields.Char(string="Siliceous Pulverized Fuel Ash")
    calcareous1 = fields.Char(string="Calcareous Pulverized Fuel Ash")

    wt_of_sample = fields.Float("Wt of sample taken W1 (gm)")
    wt_of_two_rp = fields.Float("Wt of two residue and paper after ignition at 1100˚C in crucible gm")
    wt_of_two_r = fields.Float("Weight of residues in crucible after HF at 1100˚C gm")
    difference_in_wt = fields.Float("Difference in weight = ( B - C )",compute="_compute_difference_in_wt")
    Silica = fields.Float("SiO₂ = D x 100/A",compute="_compute_silica_percentage")

    @api.depends('wt_of_two_rp', 'wt_of_two_r')
    def _compute_difference_in_wt(self):
        for record in self:
            record.difference_in_wt = record.wt_of_two_rp - record.wt_of_two_r


    @api.depends('difference_in_wt', 'wt_of_sample')
    def _compute_silica_percentage(self):
        for record in self:
            if record.wt_of_sample:
                record.Silica = (record.difference_in_wt * 100) / record.wt_of_sample
            else:
                record.Silica = 0.0


    # Combined Ferric Oxide and Alumina

    r2o3_name = fields.Char("Name",default="Combined Ferric Oxide and Alumina")
    r2o3_visible = fields.Boolean("Combined Ferric Oxide and Alumina",compute="_compute_visible")

    siliceous2 = fields.Char(string="Siliceous Pulverized Fuel Ash")
    calcareous2 = fields.Char(string="Calcareous Pulverized Fuel Ash")

    wt_of_empty_combine = fields.Float("Wt of empty crucible (gm)")
    wt_of_cr_combine = fields.Float("Wt of  empty  crucible + residue (gm)")
    wt_of_sample_combine = fields.Float("Wt of sample (gm)")
    difference_in_wt_combaine = fields.Float("Difference in weight = (B - A)",compute="_compute_difference_in_wt_combaine")
    r2o3 = fields.Float("Combined Ferric Oxide and Alumina (R2O3) = D x 100/C",compute="_compute_r2o3")


    @api.depends('wt_of_cr_combine', 'wt_of_empty_combine')
    def _compute_difference_in_wt_combaine(self):
        for record in self:
            record.difference_in_wt_combaine = record.wt_of_cr_combine - record.wt_of_empty_combine

    @api.depends('difference_in_wt_combaine', 'wt_of_sample_combine')
    def _compute_r2o3(self):
        for record in self:
            if record.wt_of_sample_combine:
                record.r2o3 = (record.difference_in_wt_combaine * 100) / record.wt_of_sample_combine
            else:
                record.r2o3 = 0.0



    # %Ferric Oxide

    ferric_oxide_name = fields.Char("Name",default="% Ferric Oxide")
    ferric_oxide_visible = fields.Boolean("% Ferric Oxide",compute="_compute_visible")

    siliceous3 = fields.Char(string="Siliceous Pulverized Fuel Ash")
    calcareous3 = fields.Char(string="Calcareous Pulverized Fuel Ash")

    wt_of_sample_ferric_oxide = fields.Float("Wt of sample (gm)")
    burette_ferric_oxide  = fields.Float("Burette reading of KMnO4 for sampl (ml)")
    normality_ferric_oxide = fields.Float("Normality of KMnO4")
    ferric_oxide = fields.Float("Ferric Oxide = B x Cx 0.05585 x 1.43 x 100/A",compute="_compute_ferric_oxide")

    @api.depends('burette_ferric_oxide', 'normality_ferric_oxide', 'wt_of_sample_ferric_oxide')
    def _compute_ferric_oxide(self):
        for record in self:
            if record.wt_of_sample_ferric_oxide:
                record.ferric_oxide = record.burette_ferric_oxide * record.normality_ferric_oxide * 0.05585 * 1.43 * 100 / record.wt_of_sample_ferric_oxide
            else:
                record.ferric_oxide = 0.0

    
    # %Alumina

    alumina_name = fields.Char("Name",default="% Alumina")
    alumina1_visible = fields.Boolean("% Alumina",compute="_compute_visible")

    siliceous4 = fields.Char(string="Siliceous Pulverized Fuel Ash")
    calcareous4 = fields.Char(string="Calcareous Pulverized Fuel Ash")

    alumina = fields.Float(string="Alumina = R2O3 - Ferric oxide",compute="_compute_alumina")

    @api.depends('r2o3', 'ferric_oxide')
    def _compute_alumina(self):
        for record in self:
            record.alumina = record.r2o3 - record.ferric_oxide



    # CaO

    
    cao_name = fields.Char("Name",default="CaO")
    cao_visible = fields.Boolean("CaO",compute="_compute_visible")

    siliceous5 = fields.Char(string="Siliceous Pulverized Fuel Ash")
    calcareous5 = fields.Char(string="Calcareous Pulverized Fuel Ash")

    wt_of_sample_cao = fields.Float("Wt of sample (gm)")
    burette_cao  = fields.Float("BR of 0.01N EDTA")
    normality_cao = fields.Float("Normality OF EDTA")
    dilution_cao = fields.Float("Dilution")
    cao = fields.Float("BR*0.05608*N*100*dilution/S.wt",compute="_compute_cao")


    @api.depends('burette_cao', 'normality_cao', 'dilution_cao', 'wt_of_sample_cao')
    def _compute_cao(self):
        for record in self:
            if record.wt_of_sample_cao != 0:  # Check for division by zero
                record.cao = (record.burette_cao * record.normality_cao * 0.05608 * record.dilution_cao * 100) / record.wt_of_sample_cao
            else:
                record.cao = 0  # Handle the case where wt_of_sample_cao is zero



    # MgO
    mgo_name = fields.Char("Name",default="MgO")
    mgo_visible = fields.Boolean("MgO",compute="_compute_visible")

    siliceous6 = fields.Char(string="Siliceous Pulverized Fuel Ash")
    calcareous6 = fields.Char(string="Calcareous Pulverized Fuel Ash")

    wt_of_sample_mgo = fields.Float("Wt of sample (gm)")
    burette_mgo  = fields.Float("BR of 0.01N EDTA")
    normality_mgo = fields.Float("Normality OF EDTA")
    dilution_mgo = fields.Float("Dilution")
    mgo = fields.Float("BR*N*0.04032*25*100/S.wt",compute="_compute_mgo")


    @api.depends('burette_mgo', 'normality_mgo', 'dilution_mgo', 'wt_of_sample_mgo')
    def _compute_mgo(self):
        for record in self:
            if record.wt_of_sample_mgo != 0:  # Check for division by zero
                record.mgo = (record.burette_mgo * record.normality_mgo * 0.04032 * record.dilution_mgo * 100) / record.wt_of_sample_mgo
            else:
                record.mgo = 0  # Handle the case where wt_of_sample_cao is zero



    # % Calicum Oxide

    calicum_oxide_name = fields.Char("Name",default="% Calicum Oxide")
    calicum_oxide_visible = fields.Boolean("MgO",compute="_compute_visible")

    siliceous7 = fields.Char(string="Siliceous Pulverized Fuel Ash")
    calcareous7 = fields.Char(string="Calcareous Pulverized Fuel Ash")

    wt_of_sample_calicum_oxide = fields.Float("sample wt (gm)")
    wt_cr_calicum_oxide  = fields.Float("wt of crucible + residue (gm)")
    wt_empty_calicum_oxide = fields.Float("wt of empty crucible (gm)")
    difference_calicum_oxide = fields.Float("Difference = ( B - C ) gm",compute="_compute_difference_calicum_oxide")
    calicum_oxide = fields.Float("% CaO = D  x 100/A",compute="_compute_calicum_oxide")


    @api.depends('wt_cr_calicum_oxide', 'wt_empty_calicum_oxide')
    def _compute_difference_calicum_oxide(self):
        for record in self:
            record.difference_calicum_oxide = record.wt_cr_calicum_oxide - record.wt_empty_calicum_oxide


    @api.depends('wt_cr_calicum_oxide', 'wt_empty_calicum_oxide', 'wt_of_sample_calicum_oxide')
    def _compute_calicum_oxide(self):
        for record in self:
            if record.wt_of_sample_calicum_oxide != 0:  # Check for division by zero
                record.calicum_oxide = ((record.wt_cr_calicum_oxide - record.wt_empty_calicum_oxide) * 100) / record.wt_of_sample_calicum_oxide
            else:
                record.calicum_oxide = 0 



    # %Magnesium Oxide
    magnesium_oxide_name = fields.Char("Name", default="% Magnesium Oxide")
    magnesium_oxide_visible = fields.Boolean("MgO", compute="_compute_visible")

    siliceous8 = fields.Char(string="Siliceous Pulverized Fuel Ash")
    calcareous8 = fields.Char(string="Calcareous Pulverized Fuel Ash")

    wt_of_sample_magnesium_oxide = fields.Float("sample wt (gm)")
    wt_cr_magnesium_oxide = fields.Float("wt of crucible + residue (gm)")
    wt_empty_magnesium_oxide = fields.Float("wt of empty crucible (gm)")
    difference_magnesium_oxide = fields.Float("Difference = ( B - C ) gm", compute="_compute_difference_magnesium_oxide")
    magnesium_oxide = fields.Float("% MgO = D x 0.3621 x 100/A", compute="_compute_magnesium_oxide")

    @api.depends('wt_cr_magnesium_oxide', 'wt_empty_magnesium_oxide')
    def _compute_difference_magnesium_oxide(self):
        for record in self:
            record.difference_magnesium_oxide = record.wt_cr_magnesium_oxide - record.wt_empty_magnesium_oxide

    @api.depends('wt_cr_magnesium_oxide', 'wt_empty_magnesium_oxide', 'wt_of_sample_magnesium_oxide')
    def _compute_magnesium_oxide(self):
        for record in self:
            if record.wt_of_sample_magnesium_oxide != 0:  # Check for division by zero
                record.magnesium_oxide = ((record.wt_cr_magnesium_oxide - record.wt_empty_magnesium_oxide) * 36.21) / record.wt_of_sample_magnesium_oxide
            else:
                record.magnesium_oxide = 0

    # %Sulphur trioxide (SO3)
    so3_name = fields.Char("Name", default="% Sulphur trioxide (SO3)")
    so3_visible = fields.Boolean("SO3", compute="_compute_visible")

    siliceous9 = fields.Char(string="Siliceous Pulverized Fuel Ash")
    calcareous9 = fields.Char(string="Calcareous Pulverized Fuel Ash")

    wt_of_sample_so3 = fields.Float("sample wt (gm)")
    wt_cr_so3 = fields.Float("wt of crucible + residue (gm)")
    wt_empty_co3 = fields.Float("wt of empty crucible (gm)")
    difference_co3 = fields.Float("Residue weight = (B - C) gm", compute="_compute_difference_so3")
    so3 = fields.Float("% Sulphur trioxide (SO3)", compute="_compute_so3")

    @api.depends('wt_cr_so3', 'wt_empty_co3')
    def _compute_difference_so3(self):
        for record in self:
            record.difference_co3 = record.wt_cr_so3 - record.wt_empty_co3

    @api.depends('difference_co3', 'wt_of_sample_so3')
    def _compute_so3(self):
        for record in self:
            if record.wt_of_sample_so3 != 0:  # Check for division by zero
                record.so3 = record.difference_co3 * 34.3 / record.wt_of_sample_so3
            else:
                record.so3 = 0

    # %Loss on Ignition
    loi_name = fields.Char("Name", default="% Loss on Ignition")
    loi_visible = fields.Boolean("% Loss on Ignition", compute="_compute_visible")

    siliceous10 = fields.Char(string="Siliceous Pulverized Fuel Ash")
    calcareous10 = fields.Char(string="Calcareous Pulverized Fuel Ash")

    wt_of_empty_loi = fields.Float("wt of empty crucible (gm)")
    wt_empty_cs_loi = fields.Float("wt of empty crucible + sample before ignition gm")
    wt_cs_loi = fields.Float("wt of crucible + sample after ignition gm")
    wt_of_sample_loi = fields.Float("Wt of sample gm = B - C", compute="_compute_wt_of_sample_loi")
    loi_in_wt = fields.Float("Loss in weight = B - A", compute="_compute_loi_in_wt")
    loi = fields.Float("Loss on ignition = E x 100/ D", compute="_compute_loi")

    @api.depends('wt_empty_cs_loi', 'wt_cs_loi')
    def _compute_wt_of_sample_loi(self):
        for record in self:
            record.wt_of_sample_loi = record.wt_empty_cs_loi - record.wt_cs_loi

    @api.depends('wt_empty_cs_loi', 'wt_of_empty_loi')
    def _compute_loi_in_wt(self):
        for record in self:
            record.loi_in_wt = record.wt_empty_cs_loi - record.wt_of_empty_loi

    @api.depends('wt_of_sample_loi', 'loi_in_wt')
    def _compute_loi(self):
        for record in self:
            if record.loi_in_wt != 0:  # Check for division by zero
                record.loi = (record.wt_of_sample_loi * 100) / record.loi_in_wt
            else:
                record.loi = 0



    # Alkali as Na₂O Clause  

    na2o_name = fields.Char("Name", default="Alkali as Na₂O")
    na2o_visible = fields.Boolean("Alkali as Na₂O", compute="_compute_visible")

    siliceous11 = fields.Char(string="Siliceous Pulverized Fuel Ash")
    calcareous11 = fields.Char(string="Calcareous Pulverized Fuel Ash")

    wt_of_sample_na2o = fields.Float("Weight of sample taken")
    dilution_na2o = fields.Float("Dilution")
    sodium_reading_na2o = fields.Float("Sodium reading")
    ffg_na2o = fields.Float("Factor from graph")
    na2o_calculation = fields.Float("Dilution *Reading* factor *100/10000*wt of sample*A4",compute="_compute_na2o_calculation")
    na2o_round = fields.Float("Na * 1.3480",compute="_compute_na2o_round")
    

    @api.depends('dilution_na2o', 'sodium_reading_na2o', 'ffg_na2o', 'wt_of_sample_na2o')
    def _compute_na2o_calculation(self):
        for record in self:
            denominator = 10000 * record.wt_of_sample_na2o
            if denominator != 0:
                record.na2o_calculation = (record.dilution_na2o * record.sodium_reading_na2o * record.ffg_na2o * 100) / denominator
            else:
                record.na2o_calculation = 0

    @api.depends('na2o_calculation')
    def _compute_na2o_round(self):
        for record in self:
            record.na2o_round = record.na2o_calculation * 1.3480


    # Alkali as K₂O 

    k2o_name = fields.Char("Name", default="Alkali as K₂O")
    k2o_visible = fields.Boolean("Alkali as K₂O", compute="_compute_visible")

    siliceous12 = fields.Char(string="Siliceous Pulverized Fuel Ash")
    calcareous12 = fields.Char(string="Calcareous Pulverized Fuel Ash")

    wt_of_sample_k2o = fields.Float("Weight of sample taken")
    dilution_k2o = fields.Float("Dilution")
    potasium_reading_k2o = fields.Float("Potasium reading")
    ffg_k2o = fields.Float("Factor from graph")
    k2o_calculation = fields.Float("Dilution *Reading* factor *100/10000*wt of sample*A4",compute="_compute_k2o_calculation")
    k2o_round = fields.Float("K *1.20",compute="_compute_k2o_round")

    @api.depends('dilution_k2o', 'potasium_reading_k2o', 'ffg_k2o', 'wt_of_sample_k2o')
    def _compute_k2o_calculation(self):
        for record in self:
            denominator = 10000 * record.wt_of_sample_k2o
            if denominator != 0:
                record.k2o_calculation = (record.dilution_k2o * record.potasium_reading_k2o * record.ffg_k2o * 100) / denominator
            else:
                record.k2o_calculation = 0

    @api.depends('k2o_calculation')
    def _compute_k2o_round(self):
        for record in self:
            record.k2o_round = record.k2o_calculation * 1.20


    # Available alkalis  % = A+B (0.65)

    available_alkalis_name = fields.Char("Name", default="Available alkalis")
    available_alkalis_visible = fields.Boolean("Available alkalis", compute="_compute_visible")

    siliceous13 = fields.Char(string="Siliceous Pulverized Fuel Ash")
    calcareous13 = fields.Char(string="Calcareous Pulverized Fuel Ash")

    available_alkalis = fields.Float("Available alkalis  % = A+B (0.65)",compute="_compute_available_alkalis")

    @api.depends('na2o_round', 'k2o_round')
    def _compute_available_alkalis(self):
        for record in self:
            record.available_alkalis = record.na2o_round + (record.k2o_round * 0.65)






    #Chloride
    chloride_name = fields.Char("Name",default="Chloride")
    chloride_visible = fields.Boolean("Chloride",compute="_compute_visible")

    siliceous14 = fields.Char(string="Siliceous Pulverized Fuel Ash")
    calcareous14 = fields.Char(string="Calcareous Pulverized Fuel Ash")

    burette_reading_chloride = fields.Float("Burette reading for Blank")
    burette_reading_sample_chloride = fields.Float("Burette reading  for sample (ml)")
    diff_chloride = fields.Float("Diff. in Burette readings = (A - B )",compute="_compute_diff_chloride")
    normality_chloride = fields.Float("Normarility of 0.025N NH₄SCN")
    wt_of_sample_chloride  = fields.Float("weight of sample (gm)")
    chloride = fields.Float("Chloride % = C x D x 0.03545 x 100 / E",compute="_compute_chloride")

    @api.depends('burette_reading_chloride', 'burette_reading_sample_chloride')
    def _compute_diff_chloride(self):
        for record in self:
            record.diff_chloride = record.burette_reading_chloride - record.burette_reading_sample_chloride


    @api.depends('diff_chloride', 'normality_chloride', 'wt_of_sample_chloride')
    def _compute_chloride(self):
        for record in self:
            if record.wt_of_sample_chloride != 0:
                record.chloride = (record.diff_chloride * record.normality_chloride * 0.03545 * 100) / record.wt_of_sample_chloride
            else:
                record.chloride = 0


     #combined_percentage
    combined_percentage_name = fields.Char("Name",default="SiO2 + Al2O3 + Fe2O3 %")
    combined_percentage_visible = fields.Boolean("SiO2 + Al2O3 + Fe2O3 %",compute="_compute_visible")

    siliceous15 = fields.Char(string="Siliceous Pulverized Fuel Ash")
    calcareous15 = fields.Char(string="Calcareous Pulverized Fuel Ash")

    combined_percentage = fields.Float("SiO2 + Al2O3 + Fe2O3 %", compute="_compute_combined_percentage")

    @api.depends('Silica', 'alumina', 'ferric_oxide')
    def _compute_combined_percentage(self):
        for record in self:
            combined_percentage = record.Silica + record.alumina + record.ferric_oxide
            record.combined_percentage = combined_percentage


 
    


   

    @api.depends('sample_parameters')
    def _compute_visible(self):
        for record in self:
            record.Silica_visible = False
            record.r2o3_visible = False
            record.ferric_oxide_visible = False
            record.alumina1_visible = False
            record.cao_visible = False
            record.mgo_visible = False
            record.calicum_oxide_visible = False
            record.magnesium_oxide_visible = False
            record.so3_visible = False
            record.loi_visible = False
            record.na2o_visible = False
            record.k2o_visible = False
            record.available_alkalis_visible = False
            record.chloride_visible = False
            record.combined_percentage_visible = False
           
            for sample in record.sample_parameters:
                print("Samples internal id",sample.internal_id)
                if sample.internal_id == '6b064931-b820-44dd-a096-99c2666bd191':
                    record.Silica_visible = True
                if sample.internal_id == 'de00fb1d-bf64-4c65-b098-b22066eed595':
                    record.r2o3_visible = True
                if sample.internal_id == 'f41a3a24-c81f-480d-88b1-5f0711870d3d':
                    record.ferric_oxide_visible = True
                if sample.internal_id == '399adf9d-d71d-486b-b40b-676b09173d18':
                    record.alumina1_visible = True
                if sample.internal_id == 'cad7aa77-fad0-44bf-a374-48c100f86bfe':
                    record.cao_visible = True
                if sample.internal_id == 'a50a3026-4c50-4314-83b2-8c66b259756a':
                    record.mgo_visible = True
                if sample.internal_id == '4ddec5e4-d9eb-480b-8965-78c1d92f7349':
                    record.calicum_oxide_visible = True
                if sample.internal_id == 'bff1cbf6-c067-430d-9391-616a077daa73':
                    record.magnesium_oxide_visible = True
                if sample.internal_id == '789c0940-27b3-42a0-aacf-4d2a8d2e9a19':
                    record.so3_visible = True
                if sample.internal_id == 'e09ddd61-2d20-4d5a-b922-bea8bbdeea72':
                    record.loi_visible = True
                if sample.internal_id == '3ccd6049-2b3d-42a0-a78f-b83e49eeff6a':
                    record.na2o_visible = True
                if sample.internal_id == 'b6fb80a6-b992-477e-9048-c40b58e28a6c':
                    record.k2o_visible = True
                if sample.internal_id == '5ab486ca-fb44-437b-adeb-8b6928ac43b0':
                    record.available_alkalis_visible = True
                if sample.internal_id == 'ab368a42-36c6-44f2-81af-7b81a6ea81e7':
                    record.chloride_visible = True
                if sample.internal_id == 'fca3ebf1-b4fd-4597-81e1-37bf499c5a35':
                    record.combined_percentage_visible = True
               

    
          

    @api.model
    def create(self, vals):
        # import wdb;wdb.set_trace()
        record = super(ChemicalFlyAsh, self).create(vals)
        record.get_all_fields()
        record.eln_ref.write({'model_id':record.id})
        return record


        
    def get_all_fields(self):
        record = self.env['chemical.flyash'].browse(self.ids[0])
        field_values = {}
        for field_name, field in record._fields.items():
            field_value = record[field_name]
            field_values[field_name] = field_value

        return field_values
    


    @api.depends('eln_ref')
    def _compute_sample_parameters(self):
        for record in self:
            records = record.eln_ref.parameters_result.parameter.ids
            record.sample_parameters = records
            print("Records",records)