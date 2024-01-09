# Copyright 2022 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import fields, models, _


class SurveyUserInput(models.Model):
    _inherit = "survey.user_input"

    def _create_opportunity_post_process(self):
        """After lead creation from survey answer (module survey_crm_generation), 
        if answer (survey_user_input) contains event_type_ids, copy it in lead.
        """
        self.opportunity_id.event_type_ids = self.event_type_ids.ids

        return super(SurveyUserInput, self)._create_opportunity_post_process()
