# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import models, fields, _
from odoo.exceptions import UserError


class SurveyUserInput(models.Model):
    _inherit = "survey.user_input"

    generated_record_ids = fields.One2many('survey.generated.record', 'user_input_id', 'Generated records')
    generated_records_count = fields.Integer("Attempts Count", compute='_compute_generated_records_count')

    def _compute_generated_records_count(self):
        for user_input in self:
            user_input.generated_records_count = len(user_input.generated_record_ids)

    def action_redirect_to_generated_records(self):
        self.ensure_one()

        action = self.env['ir.actions.act_window']._for_xml_id('survey_record_generation.survey_generated_record_action')
        """ context = dict(self.env.context or {})

        context['create'] = False
        context['search_default_survey_id'] = self.survey_id.id
        context['search_default_group_by_survey'] = False
        if self.partner_id:
            context['search_default_partner_id'] = self.partner_id.id
        elif self.email:
            context['search_default_email'] = self.email

        action['context'] = context """

        return action

    def _mark_done(self, ignore_when_res_partner_mandatory_fields_are_missing = False):
        # generate records
        for user_input in self:
            created_records = {}
            fields_to_update = []

            for record_creation in user_input.survey_id.survey_record_creation_ids.sorted('sequence'):
                model = record_creation.model_id.model
                vals = {}
                ModelClass = self.env[model]
                
                for field_value in record_creation.field_values_ids:
                    if field_value.value_origin == 'fixed':
                        vals[field_value.field_id.name] = field_value.get_fixed_value_for_record_creation()
                    elif field_value.value_origin == 'question':
                        # find user_input_lines of the question
                        user_input_lines = [user_input_line for user_input_line in user_input.user_input_line_ids if user_input_line.question_id == field_value.question_id]

                        if not user_input_lines:
                            continue

                        if field_value.question_id.question_type in ['simple_choice', 'multiple_choice','matrix']:
                            if field_value.question_id.answer_values_type == 'record':
                                record_ids = []
                                for user_input_line in user_input_lines:                            
                                    if user_input_line.suggested_answer_id and user_input_line.suggested_answer_id.record_id:
                                        record_ids.append(user_input_line.suggested_answer_id.record_id.id)
                                if field_value.question_id.question_type == 'simple_choice':
                                    vals[field_value.field_id.name] = record_ids[0]
                                else:
                                    vals[field_value.field_id.name] = record_ids
                            if field_value.question_id.answer_values_type == 'value':
                                vals[field_value.field_id.name] = user_input_lines[0].suggested_answer_id.value_char
                        elif user_input_lines[0].answer_type: # if value not filled by user, answer_type not set
                            vals[field_value.field_id.name] = user_input_lines[0][f"value_{user_input_lines[0].answer_type}"]
                        else:
                            vals[field_value.field_id.name] = None
                    elif field_value.value_origin == 'other_record':
                        fields_to_update.append(field_value)
                        # check if the field to update is mandatory
                        if ModelClass._fields[field_value.field_id.name].required:
                            # check if the other record is already created, if yes add it to vals
                            if len(created_records) > 0 and created_records[field_value.other_created_record_id.id]:
                                linked_record = created_records[field_value.other_created_record_id.id]
                                vals[field_value.field_id.name] = linked_record.id
                            else:
                                raise UserError(
                                    _("The field %s is mandatory. In Record Creation tab, drag %s at the top of the table")
                                    % (field_value.field_id.display_name, field_value.other_created_record_id.name)
                                )
                # check duplicates
                uniq_fields = [field_value.field_id.name for field_value in record_creation.field_values_ids.filtered(lambda r:r.unicity_check)]
                duplicate = None
                if uniq_fields:
                    uniq_domain = []
                    for uniq_field in uniq_fields:
                        uniq_domain.append((uniq_field,'=',vals[uniq_field]))
                    duplicate = self.env[model].search(uniq_domain, limit=1)

                if duplicate:
                    record = duplicate
                else:
                    if model == "res.partner" and ignore_when_res_partner_mandatory_fields_are_missing:
                        # this part has been developed for Calim specific needs : being able to create several Contacts with the same survey
                        # TODO : find a way to make it generic for all models ?
                        if not vals.get("lastname") and not vals.get("firstname"):
                            continue
                    # Create record
                    record = self.env[model].create(vals)
                    # Link generated records to user input
                    self.env['survey.generated.record'].create({
                        'survey_record_creation_name':record_creation.name,
                        'survey_record_creation_id':record_creation.id, 
                        'user_input_id':user_input.id, 
                        "created_record_id":"%s,%s" % (model,record.id)
                    })

                created_records[record_creation.id] = record

            # update linked records
            for field_to_update in fields_to_update:
                record_to_update = created_records.get(field_to_update.survey_record_creation_id.id)
                if record_to_update:
                    linked_record = created_records[field_to_update.other_created_record_id.id]
                    record_to_update.write({field_to_update.field_id.name:linked_record.id})

        return super()._mark_done()
