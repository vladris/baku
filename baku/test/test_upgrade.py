import os
import shutil
import unittest
from contextlib import redirect_stdout
from baku import consts, environment, upgrade, utils


class TestUpgrade(unittest.TestCase):
    def tearDown(self):
        os.chdir('..')
        if os.path.exists('testrun'):
            shutil.rmtree('testrun')


    def setUp(self):
        utils.ensure_path('testrun')
        os.chdir('testrun')


    def test_config_upgrade(self):
        # Silence print() from called function
        with redirect_stdout(None):
            environment.initialize()

        # Read config
        config = environment.load_config()

        del config['author']
        del config['title']

        # Update config file (remove keys)
        with utils.open_utf8(consts.CONFIG, 'w') as f:
            f.writelines([f'{k} = {v}\n' for k, v in config.items()])

        # Now package config should have 'author' and 'title' but blog
        # shouldn't. Test upgrade.
        config = environment.load_config()

        self.assertFalse('author' in config)
        self.assertFalse('title' in config)

        # Silence print() from called function
        with redirect_stdout(None):
            upgrade.upgrade_config()

        config = environment.load_config()

        self.assertTrue('author' in config)
        self.assertTrue('title' in config)


    def test_prep_files_upgrade(self):
        # Silence print() from called function
        with redirect_stdout(None):
            environment.initialize()

        # Remove one file and modify one file in newly setup blog
        os.remove(os.path.join('static', 'pygments.css'))
        with utils.open_utf8(os.path.join('templates', 'post.html'), 'w') as f:
            f.write('Modified')

        for u in upgrade.prep_files_upgrade():
            if u.current == os.path.join('static', 'pygments.css'):
                self.assertEqual('copy_new', u.action)
            elif u.current == os.path.join('templates', 'post.html'):
                self.assertEqual('upgrade', u.action)
            else:
                self.assertEqual('ignore', u.action)
