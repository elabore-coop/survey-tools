
import logging
import textwrap
import uuid

from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from odoo.tools import float_is_zero

_logger = logging.getLogger(__name__)


class SurveyUserInputLine(models.Model):
    _inherit = 'survey.user_input.line'

    #attachment fields
    value_file = fields.Binary(string="File")
    value_file_fname = fields.Char(string="File Name")

    #record reference fields
    record_reference = fields.Many2oneReference(model_field="record_reference_model", string="Record")
    record_reference_model = fields.Char('Record model')

    """set record_reference when saving survey_user_input line
    """
    def set_record_reference_data(self, vals):
        if vals.get('answer_type') == "suggestion" and 'suggested_answer_id' in vals:
            #find model
            answer = self.env['survey.question.answer'].browse(vals['suggested_answer_id'])
            vals['record_reference_model'] = answer.record_reference_model
            vals['record_reference'] = answer.record_reference

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            self.set_record_reference_data(vals)
        return super(SurveyUserInputLine, self).create(vals_list)


    def write(self, vals):
        self.set_record_reference_data(vals)
        return super(SurveyUserInputLine, self).write(vals)
    
    
