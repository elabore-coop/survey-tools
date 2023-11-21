# Copyright 2016-2020 Akretion France (<https://www.akretion.com>)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Survey lead generation attachment",    
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "author": "Elabore",
    'summary': 'Link Attachments from Surveys to generated leads',
    'description': """
Link Attachments from Surveys to generated leads
----------------------------------------------------
* Create new attachments on lead creation, based on attached file of survey answer (survey.user_input.line)

""",
    "website": "https://www.elabore.coop",
    "category": "",
    "depends": ["survey_base","survey_crm_generation"],
    "data": [        
        
    ],
    "installable": True,
    "auto_install":True
}
