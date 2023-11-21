
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

    def _mark_done(self):
        """Copy attachments to event registration"""
        res = super()._mark_done()
        for user_input in self:
            if user_input.survey_id.generate_registration and user_input.registration_id:
                for user_input_line in user_input.user_input_line_ids:
                    if user_input_line.value_file:
                        self.env['ir.attachment'].create({
                            'res_model':'event.registration', 
                            'res_id':user_input.registration_id.id, 
                            'name': user_input_line.value_file_fname, 
                            'datas': user_input_line.value_file, 
                            'type': 'binary'
                        })                           
        return res
