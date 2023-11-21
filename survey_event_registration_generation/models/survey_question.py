from email.policy import default
from odoo import models, fields, api


class SurveyQuestion(models.Model):
    _inherit = 'survey.question'

    event_registration_allowed_field_ids = fields.Many2many(
        comodel_name="ir.model.fields",
        compute="_compute_event_registration_allowed_field_ids",
    ) #fields of event registration, proposed in question, to associate answer to good event registration field, during event registration creation
    event_registration_field = fields.Many2one(
        string="Event registration field",
        comodel_name="ir.model.fields",
        domain="[('id', 'in', event_registration_allowed_field_ids)]",
    ) #field of event registration selected, used in event registration creation

    @api.depends("question_type")
    def _compute_event_registration_allowed_field_ids(self):
        """propose all event registration fields corresponding to selected question type
        """
        type_mapping = {
            "char_box": ["char", "text"],
            "text_box": ["html"],
            "numerical_box": ["integer", "float", "html", "char"],
            "date": ["date", "text", "char"],
            "datetime": ["datetime", "html", "char"],
            "simple_choice": ["many2one", "html", "char"],
            "multiple_choice": ["many2many", "html", "char"],              
        }
        for record in self:  
            search_domain = [
                        ("model", "=", "event.registration"),
                        ("ttype", "in", type_mapping.get(record.question_type, [])),                        
                    ]            

            record.event_registration_allowed_field_ids = self.env["ir.model.fields"].search(search_domain).ids
            