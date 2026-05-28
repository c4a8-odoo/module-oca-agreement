from odoo.tests.common import TransactionCase


class TestAgreement(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.agreement = cls.env["agreement"].create(
            {"code": "AGR-001", "name": "Agreement"}
        )
        cls.project = cls.env["project.project"].create(
            {"name": "Test Project", "agreement_id": cls.agreement.id}
        )
        cls.task = cls.env["project.task"].create(
            {"name": "Test Task", "project_id": cls.project.id}
        )

    def test_agreement_task_count(self):
        self.assertEqual(self.agreement.task_count, 1)
