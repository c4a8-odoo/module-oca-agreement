# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from datetime import timedelta

from odoo import fields
from odoo.tests.common import TransactionCase


class TestAgreement(TransactionCase):
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

    def test_partner_action(self):
        action = self.test_agreement.partner_id.action_open_agreement()
        self.assertIn(
            self.test_agreement, self.env[action["res_model"]].search(action["domain"])
        )
        self.assertEqual(1, self.test_agreement.partner_id.agreements_count)
