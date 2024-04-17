
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
        res = super(SurveyUserInput, self)._mark_done()
        msg = _('New <b>%(response)s</b> ', response=self._get_html_link(_("response")))
        if self.partner_id:
            msg += _('of <b>%(partner)s</b> ', partner=self.partner_id._get_html_link(self.partner_id.name))
        msg += _('for survey <b>%(survey)s</b> ', survey=self.survey_id._get_html_link(self.survey_id.title))
        self.survey_id.message_post(body=msg)
        return res