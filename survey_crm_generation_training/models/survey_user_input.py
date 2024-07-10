# Copyright 2022 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import fields, models, _, Command


class SurveyUserInput(models.Model):
    _inherit = "survey.user_input"

    def _prepare_opportunity(self):
        res = super(SurveyUserInput, self)._prepare_opportunity()
        
        #if answer (survey_user_input) contains event_type_ids, copy it in lead.
        res["event_type_ids"] = [Command.set(self.event_type_ids.ids)]


        # use survey responsible as seller instead of manager of sale department
        if self.survey_id.user_id:
            res["user_id"] = self.survey_id.user_id.id


        return res

