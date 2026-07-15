import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)

_to_install = [
    "agreement_legal",
    "agreement_signature",
    "agreement_termination",
    "agreement_legal_content",
    "agreement_product",
    "agreement_revision",
    "agreement_stage",
    "agreement_type",
]

_views_to_delete = [
    "agreement_legal.partner_agreement_type_list_view",
    "agreement_legal.partner_agreement_type_form_view",
]
# disable
_rename_xmlids = [
    (
        "agreement_legal.agreement_stage_new",
        "agreement_stage.agreement_stage_new",
    ),
    (
        "agreement_legal.agreement_stage_draft",
        "agreement_stage.agreement_stage_draft",
    ),
    (
        "agreement_legal.agreement_stage_reviewed",
        "agreement_stage.agreement_stage_reviewed",
    ),
    (
        "agreement_legal.agreement_stage_negotiation",
        "agreement_stage.agreement_stage_negotiation",
    ),
    (
        "agreement_legal.agreement_stage_out",
        "agreement_stage.agreement_stage_out",
    ),
    (
        "agreement_legal.agreement_stage_internal",
        "agreement_stage.agreement_stage_internal",
    ),
    (
        "agreement_legal.agreement_stage_active",
        "agreement_stage.agreement_stage_active",
    ),
    (
        "agreement_legal.agreement_stage_expired",
        "agreement_stage.agreement_stage_expired",
    ),
    (
        "agreement_legal.agreement_stage_terminated",
        "agreement_stage.agreement_stage_terminated",
    ),
    (
        "agreement_legal.agreement_stage_cancelled",
        "agreement_stage.agreement_stage_cancelled",
    ),
]


def install_module(cr, module_name):
    cr.execute(
        """
        UPDATE ir_module_module
        SET state = 'to install'
        WHERE name = %s AND state != 'installed'
        """,
        (module_name,),
    )


@openupgrade.migrate()
def migrate(env, version):
    _logger.info("Start odoo pre-migration script for version %s", version)

    openupgrade.delete_records_safely_by_xml_id(env, _views_to_delete, True)

    for module in _to_install:
        _logger.info("Install module %s", module)
        install_module(env.cr, module)

    # pre-create parent_type_id column for migration
    env.cr.execute(
        """
        ALTER TABLE agreement_type
        ADD COLUMN IF NOT EXISTS parent_type_id INTEGER REFERENCES agreement_type(id)
        ON DELETE CASCADE
        """
    )
    # move subtypes to type
    env.cr.execute(
        """
        INSERT INTO agreement_type (name, active, parent_type_id)
        SELECT name, active, agreement_type_id from agreement_subtype;
        """
    )

    # change agreement.type_id to subtype_id if set
    env.cr.execute(
        """
        UPDATE agreement
        SET agreement_type_id = COALESCE((
            SELECT id FROM agreement_type
            WHERE parent_type_id = agreement.agreement_type_id
            AND name = (SELECT name FROM agreement_subtype WHERE
            id = agreement.agreement_subtype_id)
            LIMIT 1
        ), agreement.agreement_type_id)
        WHERE agreement_type_id IS NOT NULL;
        """
    )

    # keep stages
    openupgrade.rename_xmlids(env.cr, _rename_xmlids)
