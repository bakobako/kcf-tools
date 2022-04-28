import json


def print_keys(config_params):
    for param in config_params:
        key_param = "KEY_" + param.replace('#', '').upper() + f' = \"{param}\"'
        print(key_param)
        if isinstance(config_params[param], dict):
            for sub_param in config_params[param]:
                sub_key_param = "KEY_" + param.replace('#', '').upper() + "_" + \
                                sub_param.replace('#', '').upper() + f' = \"{sub_param}\"'
                print(sub_key_param)

        if isinstance(config_params[param], list) and len(config_params[param]) > 0:
            if isinstance(config_params[param][0], dict):
                for sub_param in config_params[param][0]:
                    sub_key_param = "KEY_" + param.replace('#', '').upper() + "_" + \
                                    sub_param.replace('#', '').upper() + f' = \"{sub_param}\"'
                    print(sub_key_param)


def print_initializers(config_params):
    for param in config_params:
        intializer = param.replace("#", "") + " = params.get(" + "KEY_" + f"{param.replace('#', '').upper()})"
        print(intializer)
        if isinstance(config_params[param], dict):
            for sub_param in config_params[param]:
                sub_intializer = param.replace("#", "") + "_" + sub_param.replace("#", "") + " = " + \
                                 "params.get(" + "KEY_" + f"{param.replace('#', '').upper() + '_' + sub_param.replace('#', '').upper()})"
                print(sub_intializer)

        if isinstance(config_params[param], list) and len(config_params[param]) > 0:
            if isinstance(config_params[param][0], dict):
                for sub_param in config_params[param][0]:
                    sub_intializer = param.replace("#", "") \
                                     + "_" + sub_param.replace("#", "") + \
                                     "params.get(" + "KEY_" + f"{param.replace('#', '').upper() + '_' + sub_param.replace('#', '').upper()})"
                    print(sub_intializer)


def generate_key_definitions():
    config_params = get_config()
    print_keys(config_params)
    print()
    print_initializers(config_params)


def get_config():
    with open("data/config.json") as json_file:
        return json.load(json_file).get("parameters")


if __name__ == "__main__":
    generate_key_definitions()
