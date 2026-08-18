# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from datetime import timedelta

from odoo import fields
from odoo.tests.common import TransactionCase


class TestAgreementContent(TransactionCase):
    def setUp(self):
        super().setUp()
        self.test_customer = self.env["res.partner"].create({"name": "TestCustomer"})
        self.agreement_type = self.env["agreement.type"].create(
            {"name": "Test Agreement Type", "domain": "sale"}
        )
        self.test_agreement = self.env["agreement"].create(
            {
                "name": "TestAgreement",
                "description": "Test",
                "special_terms": "Test",
                "partner_id": self.test_customer.id,
                "start_date": fields.Date.today(),
                "end_date": fields.Date.today() + timedelta(days=365),
            }
        )

    # TEST 01: Set 'Field' for dynamic placeholder, test onchange method
    def test_onchange_copyvalue(self):
        agreement_01 = self.test_agreement
        field_01 = self.env["ir.model.fields"].search(
            [("model", "=", "agreement"), ("name", "=", "active")]
        )
        agreement_01.field_id = field_01.id
        agreement_01.onchange_copyvalue()
        self.assertEqual(agreement_01.copyvalue, "{{object.active or ''}}")

    # TEST 02: Set related 'Field' for dynamic placeholder to
    # test onchange method
    def test_onchange_copyvalue2(self):
        agreement_01 = self.test_agreement
        field_01 = self.env["ir.model.fields"].search(
            [("model", "=", "agreement"), ("name", "=", "agreement_type_id")]
        )
        sub_field_01 = self.env["ir.model.fields"].search(
            [("model", "=", "agreement.type"), ("name", "=", "active")]
        )
        agreement_01.field_id = field_01.id
        agreement_01.onchange_copyvalue()
        self.assertEqual(agreement_01.sub_object_id.model, "agreement.type")
        agreement_01.sub_model_object_field_id = sub_field_01.id
        agreement_01.onchange_copyvalue()
        self.assertEqual(
            agreement_01.copyvalue, "{{object.agreement_type_id.active or ''}}"
        )

    # TEST 03: Test Description Dynamic Field
    def test_compute_dynamic_description(self):
        agreement_01 = self.test_agreement
        agreement_01.description = "{{object.name}}"
        self.assertEqual(agreement_01.dynamic_description, "TestAgreement")

    # TEST 04: Test Parties Dynamic Field
    def test_compute_dynamic_parties(self):
        agreement_01 = self.test_agreement
        agreement_01.parties = "{{object.name}}"
        self.assertEqual(agreement_01.dynamic_parties, "<p>TestAgreement</p>")

    # TEST 05: Test Special Terms Dynamic Field
    def test_compute_dynamic_special_terms(self):
        agreement_01 = self.test_agreement
        agreement_01.special_terms = "{{object.name}}"
        self.assertEqual(agreement_01.dynamic_special_terms, "TestAgreement")

    def test_recompute_logic(self):
        self.template = self.env["agreement"].create(
            {
                "name": "Template Agreement",
                "is_template": True,
            }
        )

        self.section = self.env["agreement.section"].create(
            {
                "name": "Section Test",
                "agreement_id": self.template.id,
            }
        )

        self.clause = self.env["agreement.clause"].create(
            {
                "name": "Clause Test",
                "agreement_id": self.template.id,
                "section_id": self.section.id,
            }
        )

        self.appendix = self.env["agreement.appendix"].create(
            {
                "name": "Appendix A",
                "agreement_id": self.template.id,
                "title": "Anex A",
            }
        )

        self.test_agreement.template_id = self.template.id

        self.old_appendix = self.env["agreement.appendix"].create(
            {
                "name": "Appendix Old",
                "agreement_id": self.test_agreement.id,
                "title": "Anex Old",
            }
        )
        self.test_agreement.recompute_from_template()

        self.assertEqual(len(self.test_agreement.sections_ids), 1)
        new_section = self.test_agreement.sections_ids[0]
        self.assertEqual(len(new_section.clauses_ids), 1)
        self.assertEqual(len(self.test_agreement.clauses_ids), 1)
        self.assertEqual(self.test_agreement.clauses_ids.section_id, new_section)
