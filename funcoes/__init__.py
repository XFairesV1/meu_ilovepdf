import os
import importlib

plugins = []
pkg_dir = os.path.dirname(__file__)

for fname in os.listdir(pkg_dir):
    if fname.endswith(".py") and fname not in ("__init__.py",):
        mod_name = f"funcoes.{fname[:-3]}"
        mod = importlib.import_module(mod_name)
        # cada módulo deve expor:
        # name, display_name, description, icon_class, route, multiple (bool),
        # accept (string p/ atributo accept), output_ext, media_type, run()
        plugins.append({
            "name": mod.name,
            "display_name": mod.display_name,
            "description": mod.description,
            "icon_class": mod.icon_class,
            "route": mod.route,
            "multiple": mod.multiple,
            "accept": mod.accept,
            "output_ext": mod.output_ext,
            "media_type": mod.media_type,
            "run": mod.run
        })
