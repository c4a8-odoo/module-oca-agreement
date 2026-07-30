import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)

_rename_xmlids = [
    # user groups
    (
        "agreement_legal.group_agreement_readonly",
        "agreement.group_agreement_readonly",
    ),
    (
        "agreement_legal.group_agreement_user",
        "agreement.group_agreement_user",
    ),
    (
        "agreement_legal.group_agreement_manager",
        "agreement.group_agreement_manager",
    ),
]


@openupgrade.migrate()
def migrate(env, version):
    _logger.info("Start pre-migration script for version %s", version)

    # keep stages
    openupgrade.rename_xmlids(env.cr, _rename_xmlids)
