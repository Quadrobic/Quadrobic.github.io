"""Inserted section labels must preserve links, graph edges and proof scope."""
import json
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import manifesto
import model_annotations


SOURCE = """# Test

## 🜁 Книга Вторая. Встреча

### §8. Встреча
См. §10, §8а, §8, §9 и §99.

### §8а. Форма
См. §8 и §9.

### §9. Хватка
См. §8a.

### §10. Край
Текст.
"""

SNAPSHOT = {
    'claims': {}, 'readings': {}, 'agda': 'test', 'source_sha256': '0' * 64,
    'statuses': {'uncovered': ('·', 'Не охвачено моделью', 'Not covered by the model')},
}


class InsertedSectionTests(unittest.TestCase):
    def test_both_spellings_have_one_stable_identifier(self):
        for source in (SOURCE, SOURCE.replace('8а', '8a')):
            doc = manifesto.parse(source)
            sections = [s for b in doc['books'] for s in b['sections'] if s['num']]
            self.assertEqual([s['num'] for s in sections], ['8', '8a', '9', '10'])
        self.assertIn('<span class="ref">§8а</span>', manifesto.inline('См. §8а.'))

    def test_graph_does_not_confuse_insertion_with_section_eight(self):
        sections = model_annotations.entries(manifesto.parse(SOURCE))
        self.assertEqual(sections[0]['refs'], ['8a', '9', '10'])
        self.assertEqual(sections[1]['refs'], ['8', '9'])
        self.assertEqual(sections[2]['refs'], ['8a'])
        graph = model_annotations.render_map(SNAPSHOT, manifesto.parse(SOURCE), 'ru')
        self.assertIn('data-from="8" data-to="8a"', graph)
        self.assertNotIn('data-from="8" data-to="8" ', graph)
        self.assertIn('href="index.html#p8a"', graph)

    def test_new_section_does_not_inherit_section_eights_proofs(self):
        for lang in ('ru', 'en'):
            ui = model_annotations.reading_ui(SNAPSHOT, manifesto.parse(SOURCE), lang)
            payload = ui['assets'][f'formalization/notes.{lang}.js']
            data = json.loads(payload.removeprefix('window.iqjModelNotes = ')[:-2])
            self.assertIn('8a', data['sections'])
            self.assertIn('data-status="uncovered"', data['sections']['8a']['html'])
            self.assertNotIn('data-status="theorem"', data['sections']['8a']['html'])

    def test_duplicate_normalized_labels_fail_instead_of_overwriting(self):
        with self.assertRaisesRegex(ValueError, 'Duplicate numbered'):
            model_annotations.entries(manifesto.parse(SOURCE + '\n### §8a. Duplicate\nText.\n'))


if __name__ == '__main__':
    unittest.main()
