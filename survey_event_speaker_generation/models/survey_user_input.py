
import logging
import textwrap
import uuid

from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, _, Command
from odoo.exceptions import ValidationError
from odoo.tools import float_is_zero

_logger = logging.getLogger(__name__)


class SurveyUserInput(models.Model):
    _inherit = 'survey.user_input'

    speaker_id = fields.Many2one('res.partner', 'Event speaker') #created partner when submit survey
    

    def _create_speaker_post_process(self, speaker):
        for event in self.events_ids:      
            """Add message to chatter to note speaker creation and association with event"""
            speaker.message_post_with_view(
                "survey_event_speaker_generation.message_event_speaker_assigned",
                values={"speaker": speaker, "user_input": self, "event":event},
                subtype_id=self.env.ref("mail.mt_note").id,
            )

    def _mark_done(self):
        """Attach partner as speaker of event"""
        res = super()._mark_done()
        for user_input in self.filtered(lambda r: r.survey_id.generate_speaker and not r.speaker_id and r.partner_id):                        
            user_input.update({"speaker_id": user_input.partner_id.id})
            for event in user_input.events_ids:                
                event.speaker_ids = [Command.link(user_input.speaker_id.id)]            
            user_input._create_speaker_post_process(user_input.speaker_id)
                

        return res
