{'name':'LERM_CIVIL',
 'summary': "LERM_CIVIL",
 'author': "Usman Shaikhnag", 
 'website': "http://www.esehat.org", 
 'category': 'Uncategorized', 
 'version': '13.0.1', 
 'depends':['base' , 'contacts','stock','product' , 'mail','documents','documents_spreadsheet','lerm_civil_inv'],
 'data': [
    'data/sequence.xml',
    'views/lerm.xml',
    'views/groups.xml',
    'views/material.xml',
    'views/srf.xml',
    'views/parameter_master.xml',
    'views/datasheet_master.xml',
    'views/sample.xml',
    'views/sample_range.xml',
    'views/eln.xml',
    'views/contractor.xml',
    'views/mechanical/sieve_analysis.xml',
    'views/mechanical/pavel_block.xml',
    'views/mechanical/free_swell_index.xml',
    'views/mechanical/soil_cbr.xml',
    'views/mechanical/heavy_ligth_compaction.xml',
    'views/mechanical/plastic_limit.xml',
    'views/mechanical/liquid_limit.xml',
    'views/mechanical/compressive_strength_solid.xml',
    'views/ndt/crack_depth.xml',
    'views/ndt/acil_crack_depth.xml',
    'views/ndt/cover_meter.xml',
    'views/ndt/carbonation_test.xml',
    'views/ndt/rebound_hammer.xml',
    'views/ndt/acil_upv.xml', 
    'views/ndt/upv.xml',
    'views/mechanical/cement_normal_consistency.xml',
    'views/mechanical/cement_setting_time.xml',
    'reports/eln_report_action.xml',
    'reports/eln_report_template.xml',
    'reports/sample_report_template.xml',
    'reports/srf_report_action.xml',
    'reports/srf_report_template.xml',
    'security/security.xml',
    'security/ir.model.access.csv',
    'reports/sample_report_action.xml',
    'reports/datasheet_templates.xml'
    ],
        'assets': {
    'web.assets_backend':[
        '/lerm_civil/static/src/js/spreadsheet.js'
    ],
    'web.report_assets_common': [
            '/lerm_civil/static/src/css/eln_report.scss',
            '/lerm_civil/static/src/css/data_sheet_styles.scss',
        ],
    'web.assets_qweb': [
        '/lerm_civil/static/src/xml/spreadsheet.xml'

    ],

        }
}
