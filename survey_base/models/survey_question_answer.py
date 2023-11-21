
import logging
import textwrap
import uuid

from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from odoo.tools import float_is_zero

_logger = logging.getLogger(__name__)


class SurveyQuestionAnswer(models.Model):
    _inherit = 'survey.question.answer'

    record_reference = fields.Many2oneReference(model_field="record_reference_model", string="Record")
    record_reference_model = fields.Char("Record Model")