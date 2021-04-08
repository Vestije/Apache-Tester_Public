
def get_settings():
    with open('recommended_settings.txt') as f:
        lines = f.readlines()
    settings_dict = {}
    for line in lines:
        setting = line.split(':')
        settings_dict[setting[0]] = setting[1].strip()
    return settings_dict


