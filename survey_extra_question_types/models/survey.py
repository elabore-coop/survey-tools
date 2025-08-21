from odoo import fields, models


class SurveyQuestion(models.Model):
    _inherit = "survey.question"
    _description = "Inherit Survey Question for extra question types"

    question_type = fields.Selection(selection_add=[
        ("checkbox", "Checkbox"),
    ])

    # TODO : remove answers page form checkbox type + answers section in options tab

class SurveyUserInputLine(models.Model):
    _inherit = "survey.user_input.line"
    _description = "Survey User Input Line for extra question types"

    value_checkbox = fields.Boolean("Checkbox answer")

    answer_type = fields.Selection(selection_add=[
        ("checkbox", "Checkbox")
    ])

class SurveyUserInput(models.Model):
    _inherit = "survey.user_input"
    _description = "Survey User Input for extra question types"

    def save_lines(self, question, answer, comment=None):
        """ Save answers to questions, depending on question type

            If an answer already exists for question and user_input_id, it will be
            overwritten (or deleted for 'choice' questions) (in order to maintain data consistency).
        """
        old_answers = self.env['survey.user_input.line'].search([
            ('user_input_id', '=', self.id),
            ('question_id', '=', question.id)
        ])

        if question.question_type in ["checkbox"]:
            return super(SurveyUserInput, self)._save_line_simple_answer(question, old_answers, answer)

        return super(SurveyUserInput, self).save_lines(question=question, answer=answer)
