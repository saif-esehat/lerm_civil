{'name':'LERM_CIVIL',
 'summary': "LERM_CIVIL",
 'author': "Usman Shaikhnag", 
 'website': "http://www.esehat.org", 
 'category': 'Uncategorized', 
 'version': '13.0.1', 
 'depends':['base' , 'contacts','stock','product' , 'mail','lerm_civil_inv','documents','documents_spreadsheet'],
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
    'reports/eln_report_action.xml',
    'reports/eln_report_template.xml',
    'reports/srf_report_action.xml',
    'reports/srf_report_template.xml',
    'security/security.xml',
    'security/ir.model.access.csv'
    ],
        'assets': {
    'web.assets_backend':[
        '/lerm_civil/static/src/js/spreadsheet.js'
    ],
    'web.report_assets_common': [
            '/lerm_civil/static/src/css/eln_report.scss',
        ],
    'web.assets_qweb': [
        '/lerm_civil/static/src/xml/spreadsheet.xml'

    ],

        }
}
