import os,yaml,logging
from dotenv import load_dotenv
logger = logging.getLogger(__name__)
def import_env_params():
    def check_path_to_dir(directory: str):
        if directory.startswith('/'):
            return directory
        else:
            return os.path.dirname(os.path.abspath(__file__))+"/../"+directory
    load_dotenv()
    result={key: os.getenv(key) for key in os.environ}
    for key in result.keys():
        if "_DIR" in key or "_FILE" in key:
            result.update({key:check_path_to_dir(result[key])})
    return result

env_params=import_env_params()

def read_yaml_configuration(configuration_file : str):
    with open(configuration_file, 'r') as stream:
        try:
            config=yaml.safe_load(stream)
            return config
        except yaml.YAMLError:
            print(yaml.YAMLError)
            return False
def read_yamls_from_dir(directory : str):
    result={}
    conf_files=[item for item in os.listdir(env_params["CONFIGURATIONS_DIR"]+directory) if ".yml" in item and not "_example.yml" in item]
    for file in conf_files:
        params=read_yaml_configuration(env_params["CONFIGURATIONS_DIR"]+directory+file)
        result.update({file.split('.')[0] : params})
    return result
