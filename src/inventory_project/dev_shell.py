import os
import sys
from pathlib import Path

import cmd2
from creole.setup_utils import assert_rst_readme, update_rst_readme
from dev_shell.base_cmd2_app import DevShellBaseApp
from dev_shell.command_sets import DevShellBaseCommandSet
from dev_shell.command_sets.dev_shell_commands import DevShellCommandSet as OriginDevShellCommandSet
from dev_shell.command_sets.dev_shell_commands import run_linters
from dev_shell.config import DevShellConfig
from dev_shell.utils.assertion import assert_is_dir
from dev_shell.utils.colorful import blue, bright_yellow, print_error
from dev_shell.utils.subprocess_utils import argv2str, make_relative_path, verbose_check_call
from poetry_publish.publish import poetry_publish

import inventory
from inventory_project.manage import main


PACKAGE_ROOT = Path(inventory.__file__).parent.parent.parent
assert_is_dir(PACKAGE_ROOT / 'src' / 'inventory')


class TempCwd:
    def __init__(self, cwd: Path):
        assert_is_dir(cwd)
        self.cwd = cwd

    def __enter__(self):
        self.old_cwd = Path().cwd()
        os.chdir(self.cwd)

    def __exit__(self, exc_type, exc_val, exc_tb):
        os.chdir(self.old_cwd)


def call_manage_py(*args, cwd):
    print()
    print('_' * 100)
    cwd_rel = make_relative_path(cwd, relative_to=Path.cwd())
    print(f'+ {cwd_rel}$ {bright_yellow("manage.py")} {blue(argv2str(args))}\n')
    args = list(args)
    args.insert(0, 'manage.py')  # Needed for argparse!
    with TempCwd(cwd):
        try:
            main(argv=args)
        except SystemExit as err:
            print_error(f'finished with exit code {err}')
        except BaseException as err:
            print_error(err)


@cmd2.with_default_category('PyInventory commands')
class PyInventoryCommandSet(DevShellBaseCommandSet):
    def do_manage(self, statement: cmd2.Statement):
        """
        Call PyInventory test "manage.py"
        """
        call_manage_py(*statement.arg_list, cwd=PACKAGE_ROOT / 'src' / 'inventory')

    def do_run_testserver(self, statement: cmd2.Statement):
        """
        Start Django dev server with the test project
        """
        # Start the "[tool.poetry.scripts]" script via subprocess
        # This works good with django dev server reloads
        verbose_check_call('run_testserver', *statement.arg_list, cwd=PACKAGE_ROOT)

    def do_makemessages(self, statement: cmd2.Statement):
        """
        Make and compile locales message files
        """
        call_manage_py(
            'makemessages',
            '--all',
            '--no-location',
            '--no-obsolete',
            '--ignore=.*',
            '--ignore=htmlcov',
            '--ignore=volumes',
            cwd=PACKAGE_ROOT / 'src' / 'inventory'
        )
        call_manage_py(
            'compilemessages',
            cwd=PACKAGE_ROOT / 'src' / 'inventory'
        )

    def do_update_rst_readme(self, statement: cmd2.Statement):
        """
        update README.rst from README.creole
        """
        update_rst_readme(
            package_root=PACKAGE_ROOT,
            filename='README.creole'
        )

    def do_ckeditor_info(self, statement: cmd2.Statement):
        """
        Print some information about CKEditor
        """
        import ckeditor

        ckeditor_path = Path(ckeditor.__file__).parent
        print('Django-CKEditor path:', ckeditor_path)

        build_config_path = Path(ckeditor_path, 'static/ckeditor/ckeditor/build-config.js')
        print('Build config:', build_config_path)

        plugins_path = Path(ckeditor_path, 'static/ckeditor/ckeditor/plugins')
        print('Plugin path:', plugins_path)

        assert plugins_path.is_dir()

        plugins = {item.name for item in plugins_path.iterdir() if item.is_dir()}

        in_plugins = False
        with build_config_path.open('r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                if line == 'plugins : {':
                    in_plugins = True
                    continue

                if in_plugins:
                    if line == '},':
                        break
                    plugin_name = line.split(':', 1)[0].strip(" '")
                    plugins.add(plugin_name)

        print("'removePlugins': (")
        for plugin_name in sorted(plugins):
            print(f"    '{plugin_name}',")
        print(')')

    def do_fill_verbose_name_translations(self, statement: cmd2.Statement):
        """
        Auto fill "verbose_name" translations:
        Just copy the model field name as translation.
        """
        MESSAGE_MAP = {'id': 'ID'}

        for lang_code in ('de', 'en'):
            print('_' * 100)
            print(lang_code)
            po_file_path = PACKAGE_ROOT / f'src/inventory/locale/{lang_code}/LC_MESSAGES/django.po'
            old_content = []
            new_content = []
            with po_file_path.open('r') as f:
                for line in f:
                    old_content.append(line)

                    if line.startswith('msgid "'):
                        msgstr = ''
                        msgid = line[7:-2]
                        try:
                            model, attribute, kind = msgid.strip().split('.')
                        except ValueError:
                            pass
                        else:
                            if kind == 'verbose_name':
                                if attribute in MESSAGE_MAP:
                                    msgstr = MESSAGE_MAP[attribute]
                                else:
                                    words = attribute.replace('_', ' ').split(' ')
                                    msgstr = ' '.join(i.capitalize() for i in words)
                            elif kind == 'help_text':
                                msgstr = ' '  # "hide" empty "help_text"

                    elif (line == 'msgstr ""\n' or line == 'msgstr "&nbsp;"\n') and msgstr:
                        line = f'msgstr "{msgstr}"\n'

                    line = line.replace('Content Tonie', 'Content-Tonie')
                    new_content.append(line)

            if new_content == old_content:
                print('Nothing to do, ok.')
                return

            with po_file_path.open('w') as f:
                f.write(''.join(new_content))

            print(f'updated: {po_file_path}')


class DevShellCommandSet(OriginDevShellCommandSet):

    # TODO:
    # pyupgrade --exit-zero-even-if-changed --py3-plus --py36-plus --py37-plus --py38-plus
    # `find . -name "*.py" -type f ! -path "./.tox/*" ! -path "./htmlcov/*" ! -path "*/volumes/*"

    def do_publish(self, statement: cmd2.Statement):
        """
        Publish "dev-shell" to PyPi
        """
        # don't publish if README is not up-to-date:
        assert_rst_readme(package_root=PACKAGE_ROOT, filename='README.creole')

        # don't publish if code style wrong:
        run_linters()

        # don't publish if test fails:
        verbose_check_call('pytest', '-x')

        poetry_publish(
            package_root=PACKAGE_ROOT,
            version=inventory.__version__,
            creole_readme=True  # don't publish if README.rst is not up-to-date
        )


class DevShellApp(DevShellBaseApp):
    pass


def get_devshell_app_kwargs():
    """
    Generate the kwargs for the cmd2 App.
    (Separated because we needs the same kwargs in tests)
    """
    config = DevShellConfig(package_module=inventory)

    # initialize all CommandSet() with context:
    kwargs = dict(
        config=config
    )

    app_kwargs = dict(
        config=config,
        command_sets=[
            PyInventoryCommandSet(**kwargs),
            DevShellCommandSet(**kwargs),
        ]
    )
    return app_kwargs


def devshell_cmdloop():
    """
    Entry point to start the "dev-shell" cmd2 app.
    Used in: [tool.poetry.scripts]
    """
    c = DevShellApp(**get_devshell_app_kwargs())
    sys.exit(c.cmdloop())
