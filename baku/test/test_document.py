import os
import shutil
import unittest
from contextlib import redirect_stdout
from datetime import datetime
from baku import document, utils


class TestDocument(unittest.TestCase):
    def tearDown(self):
        os.chdir('..')
        if os.path.exists('testrun'):
            shutil.rmtree('testrun')


    def setUp(self):
        utils.ensure_path('testrun')
        os.chdir('testrun')


    def test_document(self):
        doc = document.Document('Test post', 'doc')

        self.assertEqual(doc.title, 'Test post')
        self.assertEqual(doc.name, 'test-post')
        self.assertEqual(doc.path, os.path.join('doc', 'test-post.md'))

        self.assertFalse(os.path.exists(doc.path))


    def test_create_document(self):
        doc = document.Document('Test post', 'doc')
        self.assertFalse(os.path.exists(doc.path))

        document.create_document('Test post', 'doc')

        self.assertTrue(os.path.exists(doc.path))

        with open(doc.path, 'r', encoding='utf8') as f:
            self.assertEqual(f.read(), '# Test post\n\n')


    def test_create_draft(self):
        doc = document.Document('Test post', 'drafts')
        self.assertFalse(os.path.exists(doc.path))

        document.create_draft('Test post')

        self.assertTrue(os.path.exists(doc.path))


    def test_double_create_throws(self):
        document.create_draft('Test post')

        self.assertRaises(Exception, lambda: 
            document.create_draft('Test post'))


    def test_move(self):
        document.create_draft('Test post')

        self.assertTrue(os.path.exists(
            os.path.join('drafts', 'test-post.md')))
        self.assertFalse(os.path.exists(
            os.path.join('doc', 'test-post.md')))

        document.move(os.path.join('drafts', 'test-post.md'), 'doc')

        self.assertFalse(os.path.exists(
            os.path.join('drafts', 'test-post.md')))
        self.assertTrue(os.path.exists(
            os.path.join('doc', 'test-post.md')))


    def test_move_over_existing_throws(self):
        document.create_document('Test post', 'doc')
        document.create_draft('Test post')

        self.assertTrue(os.path.exists(
            os.path.join('drafts', 'test-post.md')))
        self.assertTrue(os.path.exists(
            os.path.join('doc', 'test-post.md')))

        self.assertRaises(Exception, lambda:
            document.move(os.path.join('drafts', 'test-post.md'), 'doc'))


    def test_create_or_move_post_create(self):
        self.assertFalse(os.path.exists(
            os.path.join('2022', '09', '01', 'test-post.md')))

        # Silence print() from called function
        with redirect_stdout(None):
            document.create_or_move_post('Test post', datetime(2022, 9, 1))

        self.assertTrue(os.path.exists(
            os.path.join('2022', '09', '01', 'test-post.md')))


    def test_create_or_move_post_move(self):
        document.create_draft('Test post')

        self.assertFalse(os.path.exists(
            os.path.join('2022', '09', '01', 'test-post.md')))
        self.assertTrue(os.path.exists(
            os.path.join('drafts', 'test-post.md')))

        # Silence print() from called function
        with redirect_stdout(None):
            document.create_or_move_post(
                os.path.join('drafts', 'test-post.md'), datetime(2022, 9, 1))

        self.assertTrue(os.path.exists(
            os.path.join('2022', '09', '01', 'test-post.md')))
        self.assertFalse(os.path.exists(
            os.path.join('drafts', 'test-post.md')))


    def test_create_or_move_draft_create(self):
        self.assertFalse(os.path.exists(
            os.path.join('drafts', 'test-post.md')))

        # Silence print() from called function
        with redirect_stdout(None):
            document.create_or_move_draft('Test post')

        self.assertTrue(os.path.exists(
            os.path.join('drafts', 'test-post.md')))
        

    def test_create_or_move_draft_move(self):
        # Silence print() from called function
        with redirect_stdout(None):
            document.create_or_move_post('Test post', datetime(2022, 9, 1))

        self.assertTrue(os.path.exists(
            os.path.join('2022', '09', '01', 'test-post.md')))
        self.assertFalse(os.path.exists(
            os.path.join('drafts', 'test-post.md')))

        # Silence print() from called function
        with redirect_stdout(None):
            document.create_or_move_draft(
                os.path.join('2022', '09', '01', 'test-post.md'))

        self.assertFalse(os.path.exists(
            os.path.join('2022', '09', '01', 'test-post.md')))
        self.assertTrue(os.path.exists(
            os.path.join('drafts', 'test-post.md')))
        
