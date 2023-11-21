# Copyright 2016-2020 Akretion France (<https://www.akretion.com>)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Survey event generation attachment",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "author": "Elabore",
    "website": "https://www.elabore.coop",
    "category": "",
    'summary': 'Link Attachments from Surveys to generated event registration',
    'description': """
Link Attachments from Surveys to generated event registration
----------------------------------------------------
* Create new attachments on event registration creation, based on attached file of survey answer (survey.user_input.line)

""",
    "depends": ["survey_base","survey_event_registration_generation"],
    "data": [        
        
    ],
    "installable": True,
    "auto_install":True
}
