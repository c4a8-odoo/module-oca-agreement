# Copyright (C) 2018 - TODAY, Pavlov Media
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class Agreement(models.Model):
    _name = "agreement"
    _inherit = ["agreement"]

    description = fields.Text(tracking=True, help="Description of the agreement")
    color = fields.Integer()

    special_terms = fields.Text(
        tracking=True,
        help="Any terms that you have agreed to and want to track on the "
        "agreement/contract.",
    )
    code = fields.Char(
        string="Reference",
        required=True,
        default=lambda self: self.env._("New"),
        tracking=True,
        copy=False,
        help="ID used for internal contract tracking.",
    )
    agreement_type_id = fields.Many2one(tracking=True)

    reviewed_date = fields.Date(tracking=True)
    reviewed_user_id = fields.Many2one("res.users", string="Reviewed By", tracking=True)
    approved_date = fields.Date(tracking=True)
    approved_user_id = fields.Many2one("res.users", string="Approved By", tracking=True)
    partner_id = fields.Many2one(
        "res.partner",
        string="Partner",
        required=False,
        copy=True,
        help="The customer or vendor this agreement is related to.",
    )
    partner_contact_id = fields.Many2one(
        "res.partner",
        string="Partner Contact",
        copy=True,
        help="The primary partner contact (If Applicable).",
    )
    partner_contact_phone = fields.Char(
        related="partner_contact_id.phone", string="Partner Phone"
    )

    company_contact_id = fields.Many2one(
        "res.partner",
        string="Company Contact",
        copy=True,
        help="The primary contact in the company.",
    )
    company_contact_phone = fields.Char(
        related="company_contact_id.phone", string="Phone"
    )
    company_partner_id = fields.Many2one(
        related="company_id.partner_id", string="Company's Partner"
    )

    assigned_user_id = fields.Many2one(
        "res.users",
        string="Assigned To",
        tracking=True,
        help="Select the user who manages this agreement.",
    )

    def recompute_from_template(self):
        res = super().recompute_from_template()
        if self.template_id:
            self.write(
                {
                    "reviewed_user_id": self.env.uid,
                    "reviewed_date": fields.Date.today(),
                }
            )
        return res

    def _fill_create_vals(self, vals):
        if vals.get("code", self.env._("New")) == self.env._("New"):
            vals["code"] = self.env["ir.sequence"].next_by_code(
                "agreement"
            ) or self.env._("New")
        return vals

    @api.model_create_multi
    def create(self, vals_list):
        return super().create([self._fill_create_vals(vals) for vals in vals_list])

    def copy(self, default=None):
        """Assign a value for code is New"""
        default = dict(default or {})
        if not default.get("code", False):
            default.setdefault("code", self.env._("New"))
        return super().copy(default)
