from odoo.addons.survey.tests.common import SurveyCase


class TestSurveyRecordCreation(SurveyCase):
    def setUp(self):
        super(TestSurveyRecordCreation, self).setUp()

        self.survey = self.env["survey.survey"].create({
            "title": "Test Survey",
        })

        self.question_name = self._add_question(
            page=None,
            name="Name",
            qtype="char_box",
            survey_id=self.survey.id,
            sequence=1
        )

        self.answer = self._add_answer(survey=self.survey, partner=False, email="jean@test.fr")
        self._add_answer_line(question=self.question_name, answer=self.answer, answer_value="Jean")

    def test_record_is_created(self):
        self.model_id = self.env["ir.model"]._get("res.partner")
        self.survey_record_creation = self.env["survey.record.creation"].create(
            {
                "name": "Contact",
                "survey_id": self.survey.id,
                "model_id": self.model_id.id,
            }
        )
        name_field = self.env["ir.model.fields"].search([("model", "=", "res.partner"), ("name", "=", "name")])
        self.env["survey.record.creation.field.values"].create(
            {
                "survey_record_creation_id": self.survey_record_creation.id,
                "survey_id": self.survey.id,
                "model_id": self.model_id.id,
                "field_id": name_field.id,
                "value_origin": "question",
                "question_id": self.question_name.id
            }
        )
        self.answer._mark_done()
        partner = self.env["res.partner"].search(
            [("name", "=", "Jean")]
        )
        self.assertTrue(partner.name == "Jean")

