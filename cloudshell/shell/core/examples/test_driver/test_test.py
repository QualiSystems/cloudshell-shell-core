import cloudshell.configuration as configuration
import os
import imp



# print(configuration.__path__)
# package = sys.modules[configuration]
# print(dir(package))


def search_files(search_path, pattern):
    if not isinstance(search_path, list):
        search_path = [search_path]
    found_files = []
    for path in search_path:
        for file in os.listdir(path):
            full_path = os.path.join(path, file)
            if os.path.isfile(full_path):
                if file == pattern:
                    found_files.append(full_path)
            else:
                found_files += search_files(full_path, pattern)
    return found_files



def import_module(path):
    module_dir, module_file = os.path.split(path)
    module_name, module_ext = os.path.splitext(module_file)
    f, pathname, desc = imp.find_module(module_name, [module_dir])
    module_obj = imp.load_module(module_name, f, pathname, desc)
    f.close()
    return module_obj



config_list = search_files(configuration.__path__, 'configuration.py')

for config in config_list:
    print(config)
    module = import_module(config)
    print(module.__name__)
    # sys.path.append(os.path.dirname(config))
    # module = importlib.import_module()

    # print(os.path.)
    # print(config)
    # mod = importlib.import_module(config)
    # dir(mod)
# print(sys.path)



