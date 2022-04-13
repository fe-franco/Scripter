import configparser
config = configparser.ConfigParser()
# Add the structure to the file we will create
config.add_section('postgresql')
config.set('postgresql', 'host', 'localhost')
config.set('postgresql', 'user', 'finxter1')
config.set('postgresql', 'port', '5543')
config.set('postgresql', 'password', 'myfinxterpw')
config.set('postgresql', 'db', 'postgres')
config.add_section('user_info')
config.set('user_info', 'admin', 'David Yeoman')
config.set('user_info', 'login', 'finxter_freelancer')
config.set('user_info', 'password', 'freelancer_freedom')
# Write the new structure to the new file
with open("configfile.ini", 'w') as configfile:
    config.write(configfile)