import os
from importlib import import_module

for module in os.listdir(os.path.dirname(__file__)):
    if module == '__init__.py' or module[-3:] != '.py':
        continue

    module_name = module[:-3]
    class_name = module_name[0].upper() + module_name[1:]

    __import__('core.models.' + module_name, locals(), globals(), [class_name])

del module
