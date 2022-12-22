import os
import shutil
import subprocess
import sys
from pathlib import Path

from django.conf import settings
from django.core import checks
from django.core.cache import cache
from django.test import TestCase
from django_tools.unittest_utils.project_setup import check_editor_config
from packaging.version import Version

import inventory


PACKAGE_ROOT = Path(inventory.__file__).parent.parent.parent


def assert_file_contains_string(file_path, string):
    with file_path.open('r') as f:
        for line in f:
            if string in line:
                return
    raise AssertionError(f'File {file_path} does not contain {string!r} !')


def test_version(package_root=None, version=None):
    if package_root is None:
        package_root = PACKAGE_ROOT

    if version is None:
        version = inventory.__version__

    ver_obj = Version(inventory.__version__)

    if not ver_obj.is_prerelease:
        version_string = f'v{version}'

        assert_file_contains_string(
            file_path=Path(package_root, 'README.md'), string=version_string
        )

    assert_file_contains_string(
        file_path=Path(package_root, 'pyproject.toml'),
        string=f'version = "{version}"'
    )

    assert_file_contains_string(
        file_path=Path(package_root, 'deployment', 'project.env'),
        string=f'PROJECT_VERSION={version}'
    )


def test_poetry_check(package_root=None):
    if package_root is None:
        package_root = PACKAGE_ROOT

    poerty_bin = shutil.which('poetry')

    output = subprocess.check_output(
        [poerty_bin, 'check'],
        text=True,
        env=os.environ,
        stderr=subprocess.STDOUT,
        cwd=str(package_root),
    )
    print(output)
    assert output == 'All set!\n'


class ProjectSettingsTestCase(TestCase):
    def test_project_path(self):
        project_path = settings.PROJECT_PATH
        assert project_path.is_dir()
        assert Path(project_path, 'inventory').is_dir()
        assert Path(project_path, 'inventory_project').is_dir()

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
            'security.W008',  # settings.SECURE_SSL_REDIRECT=False
            'async.E001',  # os.environ['DJANGO_ALLOW_ASYNC_UNSAFE'] exists
        }
        if all_issue_ids != excpeted_issues:
            print('=' * 100)
            for issue in all_issues:
                print(issue)
            print('=' * 100)
            raise AssertionError('There are check issues!')

    def test_cache(self):
        # django cache should work in tests, because some tests "depends" on it
        cache_key = 'a-cache-key'
        assert cache.get(cache_key) is None
        cache.set(cache_key, 'the cache content', timeout=1)
        assert cache.get(cache_key) == 'the cache content'
        cache.delete(cache_key)
        assert cache.get(cache_key) is None

    def test_settings(self):
        assert settings.SETTINGS_MODULE == 'inventory_project.settings.tests'
        middlewares = [entry.rsplit('.', 1)[-1] for entry in settings.MIDDLEWARE]
        assert 'AlwaysLoggedInAsSuperUserMiddleware' not in middlewares
        assert 'DebugToolbarMiddleware' not in middlewares


def test_check_editor_config():
    check_editor_config(package_root=PACKAGE_ROOT)


class CodeStyleTestCase(TestCase):
    def call(self, prog, *args):
        venv_bin_path = Path(sys.executable).parent
        prog = shutil.which(prog, path=venv_bin_path)
        assert prog

        # Darker will call other programs like "flake8", "git"
        # Use first our venv bin path:
        env_path = f'{venv_bin_path}{os.pathsep}{os.environ["PATH"]}'

        return subprocess.check_output(
            (prog,) + args,
            text=True,
            env=dict(PATH=env_path),
            stderr=subprocess.STDOUT,
            cwd=str(PACKAGE_ROOT),
        )

    def check_code_style(self):
        self.call('darker', '--check')
        self.call('isort', '--check-only', '.')
        self.call('flake8', '.')

    def test_code_style(self):
        # lint: ## Run code formatters and linter
        # 	poetry run darker --check
        # 	poetry run isort --check-only .
        # 	poetry run flake8 .
        #
        # fix-code-style: ## Fix code formatting
        # 	poetry run darker
        # 	poetry run isort .

        # First try:
        try:
            self.check_code_style()
        except subprocess.CalledProcessError:
            # Fix and test again:
            try:
                self.call('darker')
                self.call('isort', '.')
                self.check_code_style()  # Check again
            except subprocess.CalledProcessError as err:
                raise AssertionError(f'Linting error:\n{"-"*100}\n{err.stdout}\n{"-"*100}')
