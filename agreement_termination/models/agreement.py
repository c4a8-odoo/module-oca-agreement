# Copyright (C) 2018 - TODAY, Pavlov Media
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class Agreement(models.Model):
    _name = "agreement"
    _inherit = ["agreement"]

    expiration_notice = fields.Integer(
        string="Exp. Notice (Days)",
        tracking=True,
        help="Number of Days before expiration to be notified.",
    )
    change_notice = fields.Integer(
        string="Change Notice (Days)",
        tracking=True,
        help="Number of Days to be notified before changes.",
    )
    termination_requested = fields.Date(
        string="Termination Requested Date",
        tracking=True,
        help="Date that a request for termination was received.",
    )
    termination_date = fields.Date(
        tracking=True, help="Date that the contract was terminated."
    )
    notification_address_id = fields.Many2one(
        "res.partner",
        string="Notification Address",
        help="The address to send notifications to, if different from "
        "customer address.(Address Type = Other)",
    )
