from odoo.tests.common import TransactionCase


class TestAgreement(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.agreement = cls.env["agreement"].create(
            {"code": "AGR-001", "name": "Agreement 1"}
        )
        cls.agreement2 = cls.env["agreement"].create(
            {"code": "AGR-002", "name": "Agreement 2"}
        )
        cls.project = cls.env["project.project"].create(
            {"name": "Test Project", "agreement_id": cls.agreement2.id}
        )
        cls.task = cls.env["project.task"].create(
            {"name": "Test Task", "project_id": cls.project.id}
        )

    def test_task_inherits_agreement_from_project(self):
        self.assertEqual(self.task.agreement_id, self.agreement2)

    def test_agreement_task_count(self):
        self.agreement2._compute_task_count()
        self.assertEqual(self.agreement2.task_count, 1)

    def test_agreement_project_ids(self):
        self.assertIn(self.project, self.agreement2.project_ids)
