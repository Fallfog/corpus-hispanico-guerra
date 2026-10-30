"""Regresión: fichas documentales con listas de hechos de formatos distintos."""
import pathlib
import sys
import unittest

ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build import facts_html


class FactsHtml(unittest.TestCase):
    def test_label_value_pairs_legacy(self):
        html=facts_html([['Fecha','12 de febrero de 1817'],['Lugar','Chacabuco']])
        self.assertIn('<dt>Fecha</dt><dd>12 de febrero de 1817</dd>',html)
        self.assertIn('<dt>Lugar</dt><dd>Chacabuco</dd>',html)

    def test_independent_statements(self):
        html=facts_html(['El ejército venció.','San Martín & Maroto'])
        self.assertIn('<dt>Dato 1</dt><dd>El ejército venció.</dd>',html)
        self.assertIn('<dt>Dato 2</dt><dd>San Martín &amp; Maroto</dd>',html)

    def test_label_value_dict(self):
        html=facts_html([{'label':'Resultado','value':'Victoria & saqueo'}])
        self.assertIn('<dt>Resultado</dt><dd>Victoria &amp; saqueo</dd>',html)

    def test_bad_structure_is_rejected(self):
        with self.assertRaises(ValueError):
            facts_html([{'wrong':'shape'}])


if __name__=='__main__':
    unittest.main()
