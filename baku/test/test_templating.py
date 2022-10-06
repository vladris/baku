from datetime import datetime
from baku import templating, utils
import os
import shutil
import unittest


class TestTemplating(unittest.TestCase):
    def setUp(self):
        self.test_template = os.path.join('testrun', 'test_template')


    def tearDown(self):
        if os.path.exists('testrun'):
            shutil.rmtree('testrun')


    def createTemplate(self, content):
        utils.ensure_path('testrun')
        with open(self.test_template, 'w+') as f:
            f.write(content)


    def renderTemplate(self, context):
        template = templating.VerySimpleTemplate(self.test_template)
        return templating.render(template, context)


    def test_simple_templating(self):
        self.createTemplate('Text {{ var }} text')

        self.assertEqual(
            self.renderTemplate({'var': 1}),
            'Text 1 text')


    def test_reference_expression(self):
        self.createTemplate('Text {{ a.b.c }} text')

        self.assertEqual(
            self.renderTemplate({'a': {'b': {'c': 1 }}}),
            'Text 1 text')


    def test_html_escape(self):
        self.createTemplate('Text {{ var & }} text')

        self.assertEqual(
            self.renderTemplate({'var': '< 1 >'}),
            'Text &lt; 1 &gt; text')


    def test_date_formatting(self):
        self.createTemplate('Text {{ var ~ %Y %m %d }} text')

        self.assertEqual(
            self.renderTemplate({'var': datetime(2022, 9, 1)}),
            'Text 2022 09 01 text')


    def test_if_expression(self):
        self.createTemplate('Text {{ if a }}cond{{ endif }} text')

        self.assertEqual(
            self.renderTemplate({'a': True}),
            'Text cond text')

        self.assertEqual(
            self.renderTemplate({'a': False}),
            'Text  text')


    def test_nested_ifs(self):
        self.createTemplate('Text {{ if a }}a{{ if b }}b{{ endif }}a{{endif}}.')

        self.assertEqual(
            self.renderTemplate({'a': False, 'b': False}),
            'Text .')

        self.assertEqual(
            self.renderTemplate({'a': True, 'b': False}),
            'Text aa.')

        self.assertEqual(
            self.renderTemplate({'a': False, 'b': True}),
            'Text .')

        self.assertEqual(
            self.renderTemplate({'a': True, 'b': True}),
            'Text aba.')


    def test_for_expression(self):
        self.createTemplate('Text {{ for a }}{{ $item }}{{ endfor }}.')

        self.assertEqual(
            self.renderTemplate({'a': []}),
            'Text .')

        self.assertEqual(
            self.renderTemplate({'a': [1, 2, 3]}),
            'Text 123.')


    def test_for_if(self):
        self.createTemplate('Text {{ for a }}#{{ if $item.on }}' + \
            '{{ $item.value }}{{ endif }}{{ endfor }}.')

        self.assertEqual(
            self.renderTemplate({'a': [{'on': False},
                {'on': True, 'value': 1}, {'on': True, 'value': 2}]}),
            'Text ##1#2.'
        )
