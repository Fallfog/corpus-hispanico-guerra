"""Pruebas sintéticas para el publicador de intervalos de quince minutos."""
import copy
import datetime as dt
import json
import pathlib
import sys
import tempfile
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / 'scripts'))
from editorial import digest, CHECKS
from publish_next import run_quarter_hour, save


class QuarterHourPublication(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = pathlib.Path(self.tmp.name)
        (self.root / 'content/cola').mkdir(parents=True)
        (self.root / 'content/entries').mkdir()
        save(self.root / 'editorial/config.json', {
            'paused': False, 'max_publications_per_day': 96,
            'reserved_release_times': {},
        })
        save(self.root / 'editorial/publications.json', {})
        save(self.root / 'editorial/inventory.json', [])
        self.now = dt.datetime(2026, 10, 29, 8, 7, tzinfo=dt.timezone.utc)

    def draft(self, ident='CHG-A-9999'):
        d = {
            'id': ident, 'slug': ident.lower(), 'topic_key': 'tema-' + ident.lower(),
            'title': 'PRUEBA SINTÉTICA NO PUBLICABLE', 'category': 'Acciones militares',
            'period': 'Prueba', 'era': 'Prueba', 'date': 'Prueba',
            'location': 'Prueba', 'summary': 'Prueba', 'facts': [['Tipo', 'Prueba']],
            'sections': [{'heading': str(i), 'paragraphs': [('prueba ' * 390) + '[1][2]']} for i in range(8)],
            'sources': [{
                'n': n, 'name': 'Fuente sintética', 'kind': 'Prueba',
                'url': 'https://example.org/' + str(n), 'verified_at': '2026-10-28',
                'verification_note': 'Material de simulación, sin contenidos reales'
            } for n in range(1, 6)],
            'editorial_note': 'Solo para tests', 'keywords': [], 'eyebrow': 'Prueba',
            'related': [], 'chronology': 0, 'status': 'revisado',
        }
        d['approval'] = {
            'reviewer': 'Simulación', 'date': '2026-10-28',
            'notes': 'Material de pruebas exclusivamente', 'checks': dict.fromkeys(CHECKS, True),
            'content_sha256': digest(d)
        }
        return d

    def queue(self, ident='CHG-A-9999'):
        save(self.root / 'content/cola' / (ident + '.json'), self.draft(ident))

    def test_no_approved_articles(self):
        result = run_quarter_hour(self.root, self.now)
        self.assertEqual(result['result'], 'empty_or_held')

    def test_publish_once_per_window(self):
        self.queue()
        self.assertEqual(run_quarter_hour(self.root, self.now)['result'], 'published')
        self.assertEqual(run_quarter_hour(self.root, self.now)['result'], 'already_published')
        self.assertTrue((self.root / 'content/entries/CHG-A-9999.json').exists())
        self.assertTrue((self.root / 'editorial/publications.json').exists())

    def test_no_second_publication_before_15_minutes(self):
        self.queue()
        run_quarter_hour(self.root, self.now)
        self.queue('CHG-A-9998')
        self.assertEqual(run_quarter_hour(self.root, self.now + dt.timedelta(minutes=8))['result'], 'cooldown')
        self.assertEqual(run_quarter_hour(self.root, self.now + dt.timedelta(minutes=15))['result'], 'published')

    def test_two_articles_in_different_slots(self):
        self.queue()
        run_quarter_hour(self.root, self.now)
        self.queue('CHG-P-9998')
        result = run_quarter_hour(self.root, self.now + dt.timedelta(minutes=15))
        self.assertEqual(result['result'], 'published')
        ledger = json.loads((self.root / 'editorial/publications.json').read_text())
        self.assertEqual(len(ledger), 2)
        self.assertTrue(all('/auto-' in key for key in ledger))

    def test_dry_run_retains_queue(self):
        self.queue()
        self.assertEqual(run_quarter_hour(self.root, self.now, dry_run=True)['result'], 'would_publish')
        self.assertTrue((self.root / 'content/cola/CHG-A-9999.json').exists())
        self.assertEqual(len(json.loads((self.root / 'editorial/publications.json').read_text())), 0)

    def test_reserved_until_fixed_local_time(self):
        self.queue()
        p = self.root / 'editorial/config.json'
        config = json.loads(p.read_text())
        config['reserved_release_times'] = {'CHG-A-9999': '2026-10-29T21:17:00+01:00'}
        save(p, config)
        self.assertEqual(run_quarter_hour(self.root, self.now)['result'], 'empty_or_held')
        due = dt.datetime(2026, 10, 29, 21, 22, tzinfo=dt.timezone(dt.timedelta(hours=1)))
        self.assertEqual(run_quarter_hour(self.root, due)['result'], 'published')

    def test_daily_limit(self):
        self.queue()
        p = self.root / 'editorial/config.json'
        config = json.loads(p.read_text())
        config['max_publications_per_day'] = 0
        save(p, config)
        self.assertEqual(run_quarter_hour(self.root, self.now)['result'], 'daily_limit')

    def test_unapproved_article_is_never_published(self):
        draft = self.draft()
        draft['status'] = 'borrador'
        save(self.root / 'content/cola/test.json', draft)
        result = run_quarter_hour(self.root, self.now)
        self.assertEqual(result['result'], 'empty_or_held')
        self.assertTrue(result['held'])

    def test_duplicate_topic_and_legacy_register_do_not_block_each_other(self):
        self.queue()
        save(self.root / 'editorial/publications.json', {
            '2026-10-29/extra-A-0001': {'id': 'CHG-A-0001', 'at': '2026-10-29T09:00:00+01:00'}
        })
        self.assertEqual(run_quarter_hour(self.root, self.now)['result'], 'published')


if __name__ == '__main__':
    unittest.main()
