
import logging

from odoo import api, fields, models, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class SurveyQuestion(models.Model):
    _inherit = 'survey.question'

    model_id = fields.Many2one('ir.model', string="Model")
    answer_values_type = fields.Selection([('no', 'No values'),('value','Value'),('record','Record')], string="Associate value to answer", default="no", required=True)
    
    @api.onchange('model_id')
    def onchange_model_id(self):
        if self.model_id:
            rec = self.env[self.model_id.model].search([], limit=1)
            if not rec:
                raise UserError(_('No record found in %s',self.model_id.name))
            else:
                for answer in self.suggested_answer_ids:
                    answer.record_id = f"{self.model_id.model},{rec.id}"

