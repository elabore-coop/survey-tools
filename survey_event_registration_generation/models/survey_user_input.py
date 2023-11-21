
import logging
import textwrap
import uuid

from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from odoo.tools import float_is_zero

_logger = logging.getLogger(__name__)


class SurveyUserInput(models.Model):
    _inherit = 'survey.user_input'

    registration_id = fields.Many2one('event.registration', 'Event registration') #registration created automaticaly on survey post

    

    def _prepare_registration(self):
        """Extract registration values from the answers"""
        
        elegible_inputs = self.user_input_line_ids.filtered(
            lambda x: x.question_id.event_registration_field and not x.skipped
        )

        vals = {}
        for line in elegible_inputs:
            if line.question_id.event_registration_field.ttype == 'many2one':
                vals[line.question_id.event_registration_field.name] = line.suggested_answer_id.record_reference
            else:
                vals[line.question_id.event_registration_field.name] = line[f"value_{line.answer_type}"]
     
        
        return vals

    def _create_registration_post_process(self, registration):
        """After creating the event registration send an internal message with the input link"""
        registration.message_post_with_view(
            "mail.message_origin_link",
            values={"self": registration, "origin": self},
            subtype_id=self.env.ref("mail.mt_note").id,
        )

    def _mark_done(self):
        """Generate registration when the survey is submitted"""
        for user_input in self.filtered(
            lambda r: r.survey_id.generate_registration and not self.registration_id
        ):
            vals = user_input._prepare_registration()

            # check doublon : if old draft registration already exists : update it
            email = vals.get('email')
            event_id = vals.get('event_id')
            old_registration = False
            if email and event_id:
                old_registration = self.env["event.registration"].search([('email','=',email),('event_id','=',event_id)])
                if old_registration:
                    old_registration = old_registration[0]
                    if old_registration.state == 'draft':
                        registration = old_registration
                        registration.write(vals)
                        registration.message_post_with_view(
                            "mail.message_origin_link",
                            values={"edit":True, "self": registration, "origin": user_input},
                            subtype_id=self.env.ref("mail.mt_note").id,
                        )

            if not old_registration:
                registration = self.env["event.registration"].create(vals)
                self._create_registration_post_process(registration)
                
            self.update({"registration_id": registration.id})
        res = super()._mark_done()

        # after all, set partner id of registration as the partner of user input
        for user_input in self:
            if user_input.registration_id and user_input.partner_id:
                user_input.registration_id.partner_id = user_input.partner_id
        return res
