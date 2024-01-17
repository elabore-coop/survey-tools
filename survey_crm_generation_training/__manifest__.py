# Copyright 2016-2020 Akretion France (<https://www.akretion.com>)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Survey Crm Generation Training",    
    'summary': 'Customize lead creation from survey according to trainings',
    'description': """
Customize lead creation from survey according to trainings
----------------------------------------------------
* add event type in crm.lead
* Copy event type selected in survey answer, to created lead

""",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "author": "Elabore",
    "website": "https://www.elabore.coop",
    "category": "",
    "depends": ["event","survey_crm_generation","survey_event_registration_generation","survey_event_base"],
    "data": [        
        "views/crm_lead_views.xml", 
    ],
    "installable": True,
    "auto_install":True
}
