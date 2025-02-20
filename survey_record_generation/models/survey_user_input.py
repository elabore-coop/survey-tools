# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import models


class SurveyUserInput(models.Model):
    _inherit = "survey.user_input"

    def _mark_done(self):
        # generate records
        for user_input in self:
            created_records = {}
            fields_to_update = []

            for record_creation in user_input.survey_id.survey_record_creation_ids:
                model = record_creation.model_id.model
                vals = {}
                
                for field_value in record_creation.field_values_ids:
                    if field_value.value_origin == 'fixed':
                        vals[field_value.field_id.name] = field_value.get_fixed_value_for_record_creation()
                    elif field_value.value_origin == 'question':
                        # find user_input_lines of the question
                        user_input_lines = [user_input_line for user_input_line in user_input.user_input_line_ids if user_input_line.question_id == field_value.question_id]

                        if field_value.question_id.question_type in ['simple_choice', 'multiple_choice','matrix']:
                            if field_value.question_id.answer_value_type == 'record':
                                record_ids = []
                                for user_input_line in user_input_lines:                            
                                    if user_input_line.suggested_answer_id and user_input_line.suggested_answer_id.record_id:
                                        record_ids.append(user_input_line.suggested_answer_id.record_id.id)
                                if field_value.question_id.question_type == 'simple_choice':
                                    vals[field_value.field_id.name] = record_ids[0]
                                else:
                                    vals[field_value.field_id.name] = record_ids
                            if field_value.question_id.answer_value_type == 'value':
                                vals[field_value.field_id.name] = user_input_line.suggested_answer_id.value_char
                        else:
                            user_input_line = user_input_lines[0]
                            vals[field_value.field_id.name] = user_input_line[0][f"value_{user_input_line.answer_type}"]
                    elif field_value.value_origin == 'other_record':
                        fields_to_update.append(field_value)

                # Create record
                record = self.env[model].create(vals)
                created_records[record_creation.id] = record

            # update linked records
            for field_to_update in fields_to_update:
                record_to_update = created_records[field_to_update.survey_record_creation_id.id]
                linked_record = created_records[field_to_update.other_created_record_id.id]
                record_to_update.write({field_to_update.field_id.name:linked_record.id})

        return super()._mark_done()
