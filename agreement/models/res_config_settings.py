# Copyright (C) 2018 - TODAY, Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    # Extensions
    group_use_agreement_type = fields.Boolean(
        "Use agreement types", implied_group="agreement.group_use_agreement_type"
    )
    group_use_agreement_template = fields.Boolean(
        "Use agreement template", implied_group="agreement.group_use_agreement_template"
    )

    module_agreement_signature = fields.Boolean(
        help="Track signatories and the signed document of agreements"
    )
    module_agreement_termination = fields.Boolean(
        help="Term dates, notices and termination tracking for agreements"
    )
    module_agreement_stage = fields.Boolean(
        help="Add a stage workflow to legal agreements"
    )
    module_agreement_type = fields.Boolean(
        help="Hierarchical agreement types (with sub-types) and review reminders"
    )
    module_agreement_revision = fields.Boolean(
        help="Track versions and revisions of legal agreements"
    )
    module_agreement_legal = fields.Boolean(help="Manage legal aspects of agreements")
    module_agreement_legal_content = fields.Boolean(
        help="Add legal content to agreements"
    )

    # Connect to agreement modules
    module_agreement_rebate = fields.Boolean(help="Rebate in agreements")
    module_agreement_product = fields.Boolean(help="Agreement on products")

    module_agreement_maintenance = fields.Boolean(
        help="Manage maintenance agreements and contracts."
    )
    module_agreement_mrp = fields.Boolean(
        help="Link your manufacturing orders to an agreement."
    )
    module_agreement_project = fields.Boolean(
        help="Link your projects and tasks to an agreement."
    )
    module_agreement_repair = fields.Boolean(
        help="Link your repair orders to an agreement."
    )
    module_agreement_rma = fields.Boolean(help="Link your RMAs to an agreement.")
    module_agreement_sale = fields.Boolean(
        help="Create an agreement when the sale order is confirmed."
    )
    module_agreement_sale_subscription = fields.Boolean(
        help="Link your subscriptions to an agreement."
    )
    module_agreement_stock = fields.Boolean(help="Link your pickings to an agreement.")
    module_fieldservice_agreement = fields.Boolean(
        help="Link your Field Service orders and equipments to an agreement."
    )
    module_agreement_helpdesk = fields.Boolean(
        help="Link your Helpdesk tickets to an agreement."
    )
