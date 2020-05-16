# coding: utf-8
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import base64
from lxml import etree, objectify

from odoo import api, SUPERUSER_ID
from odoo.addons.l10n_mx_edi.hooks import _load_xsd_files


def post_init_hook(cr, registry):
    url = 'http://www.sat.gob.mx/sitio_internet/cfd/terceros/terceros11.xsd'
    load_xsd_complement(cr, url)


def load_xsd_complement(cr, url):
    """Utility function to load the XSD file of the complement being
        implemented
    """
    db_fname = _load_xsd_files(cr, None, url)
    env = api.Environment(cr, SUPERUSER_ID, {})
    xsd = env.ref('l10n_mx_edi.xsd_cached_cfdv33_xsd', False)
    if not xsd:
        return False
    complement = {
        'namespace': 'http://www.sat.gob.mx/leyendasFiscales',
        'schemaLocation': db_fname,
    }
    node = etree.Element(
        '{http://www.w3.org/2001/XMLSchema}import', complement)
    res = objectify.fromstring(base64.b64decode(xsd.datas))
    res.insert(0, node)
    xsd_string = etree.tostring(res, pretty_print=True)
    xsd.datas = base64.b64encode(xsd_string)
    return True
