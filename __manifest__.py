{'name':'LERM_CIVIL',
 'summary': "LERM_CIVIL",
 'author': "Usman Shaikhnag", 
 'website': "http://www.esehat.org", 
 'category': 'Uncategorized', 
 'version': '13.0.1', 
 'depends':['base' , 'contacts','stock','product' , 'mail','lerm_civil_inv'],
 'data': [
    'data/sequence.xml',
    'views/lerm.xml',
    'views/groups.xml',
    'views/material.xml',
    'views/srf.xml',
    'views/parameter_master.xml',
    'views/datasheet_master.xml',
    'views/sample.xml',
    'views/eln.xml',
    'security/security.xml',
    'security/ir.model.access.csv'
    ],
'assets': {
    'web.assets_backend':[
        '/lerm_civil/static/src/js/spreadsheet.js'
    ],
    'web.assets_qweb': [
        '/lerm_civil/static/src/xml/spreadsheet.xml'

    ],

        }
}
