from baku import markdown, post, utils
import os
import shutil
import unittest


class TestPost(unittest.TestCase):
    def tearDown(self):
        os.chdir('..')
        if os.path.exists('testrun'):
            shutil.rmtree('testrun')


    def setUp(self):
        utils.ensure_path('testrun')
        os.chdir('testrun')


    def make_post(self, year, month, day, name, content):
        dir = os.path.join('.', year, month, day)
        doc = os.path.join(dir, name)
        utils.ensure_path(dir)
        with open(doc, 'w+') as f:
            f.write(content)

        return doc


    def test_post(self):
        p = post.Post(
            self.make_post('2022', '09', '01', 'test.md', '# Test post'))

        self.assertEqual(p.date.year, 2022)
        self.assertEqual(p.date.month, 9)
        self.assertEqual(p.date.day, 1)
        self.assertEqual(p.text, '# Test post')
        self.assertEqual(p.rel_path, './2022/09/01/test.html')
        self.assertEqual(p.href, '../../../2022/09/01/test.html')
        self.assertEqual(p.title, 'Test post')

        self.assertIsNone(p.prev)
        self.assertIsNone(p.next)


    def test_get_dest(self):
        p = post.Post(
            self.make_post('2022', '09', '01', 'test.md', '# Test post'))

        dest_dir, dest = p.get_dest()

        self.assertEqual(dest_dir,
            os.path.join('.', 'html', '2022', '09', '01'))
        self.assertEqual(dest,
            os.path.join('.', 'html', '2022', '09', '01', 'test.html'))


    def test_link_prev_next(self):
        prev = post.Post(
            self.make_post('2022', '08', '01', 'prev.md', '# Previous post'))
        next = post.Post(
            self.make_post('2022', '10', '01', 'next.md', '# Next post'))

        p = post.Post(
            self.make_post('2022', '09', '01', 'post.md', '# Test post'))

        self.assertIsNone(p.prev)

        p.link_prev(prev)

        self.assertEqual(p.prev, prev)

        self.assertIsNone(p.next)

        p.link_next(next)

        self.assertEqual(p.next, next)


    def test_process(self):
        p = post.Post(
            self.make_post('2022', '09', '01', 'post.md', '# Test post'))

        p.process_markdown(markdown.make_markdown_processor())

        self.assertEqual(p.body, '<h1>Test post</h1>\n')

