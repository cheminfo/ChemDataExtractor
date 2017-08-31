# -*- coding: utf-8 -*-
"""
test_parse_doi
~~~~~~~~~~~~~~

Test DOI parser.

"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import logging
import unittest

from lxml import etree

from chemdataextractor.doc.text import Sentence
from chemdataextractor.parse.hrms import hrms

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


class TestParseHRMS(unittest.TestCase):
    maxDiff = None

    def do_parse(self, input, expected):
        s = Sentence(input)
        log.debug(s)
        log.debug(s.tagged_tokens)
        result = next(hrms.scan(s.tagged_tokens))[0]
        log.debug(etree.tostring(result, pretty_print=True, encoding='unicode'))
        self.assertEqual(expected, etree.tostring(result, encoding='unicode'))

    def test_hrms1(self):
        s = 'HRMS (ESI) calcd for C34H28N4OP 539.1995 [M + H]+, found 539.1997.'
        output = '<hrms><structure>C34H28N4OP</structure></hrms>'
        self.do_parse(s, output)

    def test_hrms2(self):
        s = 'HRMS: 184.0767 [M + Na]+.'
        output = '<hrms/>'
        self.do_parse(s, output)

    def test_hrms3(self):
        s = 'HRMS-ESI (m/z): calcd. for C42H52NO9 [M + NH4]+ 714.3637, found 714.3633.'
        output = '<hrms><structure>C42H52NO9</structure></hrms>'
        self.do_parse(s, output)

    def test_hrms4(self):
        s = 'MALDI-HRMS (matrix: HCCA) Calculated for C32H48N4O6: [M + H]+ m/z 585.3607, Found 585.3636.'
        output = '<hrms><structure>C32H48N4O6</structure></hrms>'
        self.do_parse(s, output)

    def test_hrms5(self):
        s = 'HRMS (m/z): 827.6005 [M+Na]+ (calcd. for C48H84O9Na: 827.6013). '
        output = '<hrms><structure>C48H84O9Na</structure></hrms>'
        self.do_parse(s, output)

    def test_hrms6(self):
        s = 'HRMS [M−H]+ m/z calcd. for C24H32N9+ 446.2781, found 446.2775.'
        output = '<hrms><structure>C24H32N9+</structure></hrms>'
        self.do_parse(s, output)

    def test_hrms7(self):
        s = 'DCI-HRMS: m/z 289.0916 [M+H]+; (Calcd for C12H16O8, 288.0845)'
        output = '<hrms><structure>C12H16O8</structure></hrms>'
        self.do_parse(s, output)

    def test_hrms8(self):
        s = 'ES-HRMS: m/z 115.0393 [M−H]−; (Calcd for C5H7O3, 116.0473).'
        output = '<hrms><structure>C5H7O3</structure></hrms>'
        self.do_parse(s, output)