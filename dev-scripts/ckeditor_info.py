"""
    Helpter
"""

from pathlib import Path

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
