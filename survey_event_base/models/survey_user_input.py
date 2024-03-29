
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

    events_ids = fields.Many2many('event.event', string='Events', compute="compute_events_ids", search="search_events_ids") #related events
    event_type_ids = fields.Many2many('event.type', string='Formations', compute="compute_event_type_ids", search="search_event_type_ids") #related event products 

    def search_events_ids(self, operator, value):                
        user_input_ids = set()
        user_input_lines = self.env['survey.user_input.line'].search([('record_reference_model','=','event.event'),('record_reference','=', value)])
        for user_input_line in user_input_lines:
            user_input_ids.add(user_input_line.user_input_id.id)
        return [('id',operator,list(user_input_ids))]

    @api.depends('user_input_line_ids')
    def compute_events_ids(self):
        """get all answers of type "event.event"
        """
        for user_input in self:
            event_ids = []
            for user_input in self:
                for user_input_line in user_input.user_input_line_ids:
                    if user_input_line.record_reference_model == 'event.event':
                        event_ids.append(user_input_line.record_reference)                        
        user_input.events_ids = event_ids


    def search_event_type_ids(self, operator, value):                
        user_input_ids = set()
        user_input_lines = self.env['survey.user_input.line'].search([('record_reference_model','=','event.type'),('record_reference','=', value)])
        for user_input_line in user_input_lines:
            user_input_ids.add(user_input_line.user_input_id.id)
        return [('id',operator,list(user_input_ids))]
        

            
    @api.depends('user_input_line_ids')
    def compute_event_type_ids(self):
        """get all answers of type "event.type"
        """
        for user_input in self:
            event_type_ids = []
            for user_input in self:
                for user_input_line in user_input.user_input_line_ids:
                    if user_input_line.record_reference_model == 'event.type':
                        event_type_ids.append(user_input_line.record_reference)
        user_input.event_type_ids = event_type_ids

