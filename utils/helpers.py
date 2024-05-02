import configparser


def read_config_file(file_path):
    config = configparser.ConfigParser()
    config.read(file_path)
    return config  # Return the configparser object, not the read result


def get_conf_info(config, log_key, *, section='path'):
    try:
        return config[section][log_key]  # Make sure the 'path' section exists in your config file
    except KeyError as e:
        raise KeyError(f"Key error accessing log path: {e}") from e


def get_path(config, log_key, include_root=True):
    if include_root:
        return config["path"]["root"] + get_conf_info(config, log_key)
    else:
        return get_conf_info(config, log_key)


def get_row_data(row, field):
    return row[field.value]
