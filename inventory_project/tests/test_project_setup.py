import subprocess
from pathlib import Path
from unittest import TestCase

from bx_py_utils.path import assert_is_dir, assert_is_file
from django.conf import settings
from django.core import checks
from django.core.cache import cache
from django.core.management import call_command
from manage_django_project.management.commands import code_style
from manageprojects.test_utils.project_setup import check_editor_config, get_py_max_line_length
from packaging.version import Version

from inventory import __version__
from manage import BASE_PATH


class ProjectSetupTestCase(TestCase):
    def test_project_path(self):
        project_path = settings.BASE_PATH
        assert_is_dir(project_path)
        assert_is_dir(project_path / 'inventory')
        assert_is_dir(project_path / 'inventory_project')

        self.assertEqual(project_path, BASE_PATH)

    def test_template_dirs(self):
        assert len(settings.TEMPLATES) == 1
        dirs = settings.TEMPLATES[0].get('DIRS')
        assert len(dirs) == 1
        template_path = Path(dirs[0]).resolve()
        assert template_path.is_dir()

    def test_manage_check(self):
        all_issues = checks.run_checks(
            app_configs=None,
            tags=None,
            include_deployment_checks=True,
            databases=None,
        )
        all_issue_ids = {issue.id for issue in all_issues}
        excpeted_issues = {
            'async.E001',  # DJANGO_ALLOW_ASYNC_UNSAFE set, because of playwright tests
            'security.W009',  # ignore fake SECRET_KEY in tests
        }
        if all_issue_ids != excpeted_issues:
            print('=' * 100)
            for issue in all_issues:
                print(issue)
            print('=' * 100)
            raise AssertionError(f'There are check issues (see blow): {all_issue_ids ^ excpeted_issues}')

    def test_cache(self):
        # django cache should work in tests, because some tests "depends" on it
        cache_key = 'a-cache-key'
        self.assertIs(cache.get(cache_key), None)
        cache.set(cache_key, 'the cache content', timeout=1)
        self.assertEqual(cache.get(cache_key), 'the cache content', f'Check: {settings.CACHES=}')
        cache.delete(cache_key)
        self.assertIs(cache.get(cache_key), None)

    def test_settings(self):
        self.assertEqual(settings.SETTINGS_MODULE, 'inventory_project.settings.tests')
        middlewares = [entry.rsplit('.', 1)[-1] for entry in settings.MIDDLEWARE]
        assert 'AlwaysLoggedInAsSuperUserMiddleware' not in middlewares
        assert 'DebugToolbarMiddleware' not in middlewares

    def test_version(self):
        self.assertIsNotNone(__version__)

        version = Version(__version__)  # Will raise InvalidVersion() if wrong formatted
        self.assertEqual(str(version), __version__)

        manage_bin = BASE_PATH / 'manage.py'
        assert_is_file(manage_bin)

        output = subprocess.check_output([manage_bin, 'version'], text=True)
        self.assertIn(__version__, output)

    def test_manage(self):
        manage_bin = BASE_PATH / 'manage.py'
        assert_is_file(manage_bin)

        output = subprocess.check_output([manage_bin, 'project_info'], text=True)
        self.assertIn('inventory_project', output)
        self.assertIn('inventory_project.settings.local', output)
        self.assertIn('inventory_project.settings.tests', output)
        self.assertIn(__version__, output)

        output = subprocess.check_output([manage_bin, 'check'], text=True)
        self.assertIn('System check identified no issues (0 silenced).', output)

        output = subprocess.check_output([manage_bin, 'makemigrations'], text=True)
        self.assertIn("No changes detected", output)

    def test_code_style(self):
        call_command(code_style.Command())

    def test_check_editor_config(self):
        check_editor_config(package_root=BASE_PATH)

        max_line_length = get_py_max_line_length(package_root=BASE_PATH)
        self.assertEqual(max_line_length, 119)
