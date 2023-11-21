# Copyright 2016-2020 Akretion France (<https://www.akretion.com>)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Survey event visibility",
    "version": "16.0.0.0.0",
    "license": "AGPL-3",
    "author": "Elabore",
    'summary': 'Add visibility field in event stage',
    'description': """
Add visibility information in product and events
----------------------------------------------------

The product and event visibility is computed from event stage visibility.
""",
    "website": "https://www.elabore.coop",
    "category": "",
    "depends": ["survey"],
    "data": [        
        'views/event_stage_views.xml',         
    ],    
    "installable": True,
}
