import os
import unittest

from preview_utils import  get_repository_process_preview


class TestPreviewUtils(unittest.TestCase):
    def setUp(self):
        self.test_data_path = os.path.join(os.path.dirname(__file__), '../test_data')
        self.example_repo_path = os.path.join(self.test_data_path, 'example_repo')

    def test_preview(self):
        expected_output = \
"""└── example_repo (124 characters) (100.00%)
    ├── folder1 (50 characters) (40.32%)
    │   ├── file3.py (32 characters) (25.81%)
    │   └── file4.txt (18 characters) (14.52%)
    ├── file2.py (40 characters) (32.26%)
    ├── file1.txt (18 characters) (14.52%)
    └── .gptignore (16 characters) (12.90%)
"""
        dont_need_ignore_fn = lambda x: False
        result = get_repository_process_preview(self.example_repo_path, should_ignore_fn=dont_need_ignore_fn)
        self.assertEqual(expected_output, result)
