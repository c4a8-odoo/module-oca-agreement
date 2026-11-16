# Copyright (C) 2018 - TODAY, Pavlov Media
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class Agreement(models.Model):
    _inherit = "agreement"

    line_ids = fields.One2many(
        "agreement.line", "agreement_id", string="Products/Services", copy=False
    )
