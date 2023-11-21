# Copyright 2023 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import fields, models


class CrmLead(models.Model):
    _inherit = "crm.lead"

    event_products_ids = fields.Many2many('product.product', string='Event product')

   
    def action_view_survey_user_input_id(self):
        form_view_id = self.env.ref('survey.survey_user_input_view_form').id
        if self.survey_user_input_id:
            action = self.env["ir.actions.actions"]._for_xml_id("survey.action_survey_user_input")
            action['res_id'] = self.survey_user_input_id.id
            action['domain'] = [('id', '=', self.survey_user_input_id.id)]
            action['view_type'] = 'form'
            action['view_mode'] = 'form'
            action['binding_view_types'] = 'form'
            action['view_id'] = form_view_id
            action['views'] = [(form_view_id, 'form')]
            return action
