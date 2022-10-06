import os
import shutil
import unittest
from contextlib import redirect_stdout
from baku import cmdline, utils


class TestPost(unittest.TestCase):
    def setUp(self):
        utils.ensure_path('testrun')
        os.chdir('testrun')


    def tearDown(self):
        os.chdir('..')
        if os.path.exists('testrun'):
            shutil.rmtree('testrun')


    def test_e2e(self):
        # Initialize a blog
        self.__initialize()

        # Create a draft
        self.__create_draft()

        # Promote the created draft to post
        self.__promote_draft()

        # Create a second post
        self.__create_post()

        # Build the blog
        self.__build()


    def __initialize(self):
        self.assertFalse(os.path.exists('blog.cfg'))
        self.assertFalse(os.path.exists('templates'))
        self.assertFalse(os.path.exists('static'))

        # Silence print() from called function
        with redirect_stdout(None):
            cmdline.main(['--init'])

        self.assertTrue(os.path.exists('blog.cfg'))
        self.assertTrue(os.path.exists('templates'))
        self.assertTrue(os.path.exists('static'))


    def __create_draft(self):
        draft = os.path.join('drafts', 'post-1.md')
        self.assertFalse(os.path.exists(draft))

        # Silence print() from called function
        with redirect_stdout(None):
            cmdline.main(['--draft', 'Post 1'])

        self.assertTrue(os.path.exists(draft))


    def __promote_draft(self):
        post = os.path.join('2022', '09', '01', 'post-1.md')
        self.assertFalse(os.path.exists(post))

        # Silence print() from called function
        with redirect_stdout(None):
            cmdline.main(['--post',
                os.path.join('drafts', 'post-1.md'), '--date', '2022/09/01'])

        self.assertTrue(os.path.exists(post))


    def __create_post(self):
        post = os.path.join('2022', '09', '02', 'post-2.md')
        self.assertFalse(os.path.exists(post))

        # Silence print() from called function
        with redirect_stdout(None):
            cmdline.main(['--post', 'Post 2', '--date', '2022/09/02'])

        self.assertTrue(os.path.exists(post))


    def __build(self):
        self.assertFalse(os.path.exists('html'))

        # Silence print() from called function
        with redirect_stdout(None):
            cmdline.main(['--build'])

        # Build output
        self.assertTrue(os.path.exists('html'))

        # Rendered posts
        self.assertTrue(os.path.exists(os.path.join(
            'html', '2022', '09', '01', 'post-1.html')))
        self.assertTrue(os.path.exists(os.path.join(
            'html', '2022', '09', '02', 'post-2.html')))

        # Static assets
        self.assertTrue(os.path.exists(os.path.join(
            'html', 'static')))

        # RSS
        self.assertTrue(os.path.exists(os.path.join(
            'html', 'rss.xml')))
