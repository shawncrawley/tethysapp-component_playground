import importlib


def generate_title(name):
    title = name.replace("_", " ").title()
    for k, v in {"Esri": "ESRI", "Geojson": "GeoJSON", "Wms": "WMS"}.items():
        title = title.replace(k, v)
    return title


def import_from_path(module_name, file_path):
    """Import a module given its name and file path."""
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    # sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module
