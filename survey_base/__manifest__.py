# Copyright 2016-2020 Akretion France (<https://www.akretion.com>)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Survey base",
    'summary': 'Add fields used by several survey addons',
    'description': """
Add fields used by several survey addons
----------------------------------------------------
* Add record reference in survey_question and survey.user_input.line
* Add value_file in survey.user_input.line
* Implementation of theses fields should be in another module

""", 
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "author": "Elabore",
    "website": "https://www.elabore.coop",
    "category": "",
    "depends": ["survey"],
    "data": [        
      
    ],    
    "installable": True,
}
