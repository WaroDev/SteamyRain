import os
import re
import subprocess
import configparser

class CaseSensitiveConfigParser(configparser.ConfigParser):
    def optionxform(self, optionstr):
        return optionstr
#__________________________________________________________________________________________________________________________#
#-------------------------------------------Function to update Update skin window------------------------------------------#

def update_rainmeter_status(status_message):
    subprocess.call([RainmeterPath, '!SetVariable', 'Status', fr'{status_message}', fr'{skinPath}Update'])
    subprocess.call([RainmeterPath, '!UpdateMeter', 'Status', fr'{skinPath}Update'])
#__________________________________________________________________________________________________________________________#
#----------------------------------------------Function to retrieve variables----------------------------------------------#

def get_variables(config_file):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, config_file)
    config = configparser.ConfigParser()
    config.read(config_path)
    variables = {}
    if 'Variables' in config:
        variables = dict(config['Variables'])
    return variables

#__________________________________________________________________________________________________________________________#
#-------------------------------------Function to retrieve data from appmanifest files-------------------------------------#

def process_appmanifest_files(appmanifest_files, gamedir_path):
    processed_ids = []
    games_info = []

    for appmanifest_file in appmanifest_files:
        status = f"Processing file {appmanifest_file}"
        update_rainmeter_status(status)
        app_id = appmanifest_file[12:-4]  # Extract numerical part of the file name
        app_ids_to_skip = {'228980'}
        game_names_to_skip = {
            'Linux Runtime',
            'Proton'
        }
        
        if not app_id.isdigit():
            continue
            
        if app_id not in app_ids_to_skip:
            processed_ids.append(app_id)

            # Read appmanifest file to get game information
            appmanifest_path = os.path.join(gamedir_path, appmanifest_file)
            with open(appmanifest_path, 'r') as manifest_file:
                manifest_data = manifest_file.read()

                # Extract the appid and name from the appmanifest file
                app_id = appmanifest_file[12:-4]  # Extract numerical part of the file name
                game_name = re.search(r'"name"\s*"(.*?)"', manifest_data)
                game_name = game_name.group(1)
                game_name = re.sub(r'[^a-zA-Z0-9\s]+', '', game_name)
                skip_game = False

                for game_to_skip in game_names_to_skip:
                    if game_name.find(game_to_skip) != -1:
                        skip_game = True
                if skip_game == True:
                    continue
                
                games_info.append({'appid': app_id, 'name': game_name, 'image': ""})

    return processed_ids, games_info
#__________________________________________________________________________________________________________________________#
#------------------------------------------------Function to create meters-------------------------------------------------#
def create_meter(id_key, index, image, image_path, search, is_hidden, is_extra=False, extra_index=None):
  
    section_prefix = 'E' if is_extra else ''
    HiddenValue = ('1' if search else
                    f'(1-#Vis{index}#)' if is_hidden and not is_extra else
                    f'(1-#{id_key}Vis#)' if is_hidden and is_extra else
                    f'#Vis{index}#' if not is_hidden and not is_extra else
                    f'#{id_key}Vis#')

    meter_data = {
        'Name': {
            'Meter': 'String',
            'Text': f'#{id_key}name#' if not is_extra else f'#{id_key}#',
            'LeftMouseUpAction': f'[steam://rungameid/#{id_key}#]' if not is_extra else f'[#{id_key}Path#]',
            'MeterStyle': 'NameStyle',
            'Hidden': f'{HiddenValue}',
            'Group': f'Games | {section_prefix}G{index}',
        },
        'Image': {
            'Meter': 'Image',
            'MeterStyle': 'GameStyle',
            'ImageName': f'{image_path}\\#{id_key}#\\{get_image_for_game(image_path, id_key) if image == "Logo" else "icon.jpg"}' if not is_extra else f'#@#img\\E{image}\\{extra_index:03d}.jpg',
            'LeftMouseUpAction': f'[steam://rungameid/#{id_key}#]' if not is_extra else f'[#{id_key}Path#]',
            'Hidden': f'{HiddenValue}',
            'Group': f'Games | {section_prefix}G{index}',
        },
        'String': {
            'Meter': 'String',
            'MeterStyle': 'VisStyle',
            'LeftMouseUpAction': f'[!WriteKeyValue Variables "Vis{index}" {"0" if is_hidden else "1"} "#@#GamesInfo.inc"]'
                                 f'[!WriteKeyValue Variables GameCountPLUS "(Clamp((#GameCountPLUS#{"+" if is_hidden else "-"}1),0,#GameCount#))" "#@#GamesInfo.inc"]'
                                 f'[!SetVariable GameCountPLUS "(Clamp((#GameCountPLUS#{"+" if is_hidden else "-"}1),0,#GameCount#))"]'
                                 f'[!SetVariable Vis{index} {"0" if is_hidden else "1"}]'
                                 f'[!UpdateMeasure HideGame][!Updatemeasure Lenght][!HideMeterGroup {section_prefix}G{index}][!UpdateMeterGroup Games][!ReDraw]'
                                 f'[!SetVariable UpdateVar "Vis{index}"][!SetVariable UpdateVar2 "GameCountPLUS"][!SetVariable UpdateVar3 "G{index}"][!Updatemeasure HiddenWindow]'
                                 if not is_extra else f'[!WriteKeyValue Variables "{id_key}Vis" {"0" if is_hidden else "1"} "#@#NonSteamGames.inc"]'
                                 f'[!WriteKeyValue Variables ExtraGameCountPLUS "(Clamp((#ExtraGameCountPLUS#{"+" if is_hidden else "-"}1),0,#ExtraGamesCount#))" "#@#NonSteamGames.inc"]'
                                 f'[!SetVariable ExtraGameCountPLUS "(Clamp((#ExtraGameCountPLUS#{"+" if is_hidden else "-"}1),0,#ExtraGamesCount#))"]'
                                 f'[!SetVariable {id_key}Vis {"0" if is_hidden else "1"}]'
                                 f'[!UpdateMeasure HideGame][!Updatemeasure Lenght][!HideMeterGroup {section_prefix}G{index}][!UpdateMeterGroup Games][!ReDraw]'
                                 f'[!SetVariable UpdateVar "{id_key}Vis"][!SetVariable UpdateVar2 "ExtraGameCountPLUS"][!SetVariable UpdateVar3 "EG{index}"][!Updatemeasure HiddenWindow]',
            'Hidden': f'{HiddenValue}',
            'Group': f'Games | {section_prefix}G{index}',
        },
        'Gap': {
            'Meter': 'Image',
            'MeterStyle': 'GapStyle',
        }
    }
    return meter_data
#__________________________________________________________________________________________________________________________#
#--------------------------------------------Function to check image existance---------------------------------------------#
def get_image_for_game(image_path, id_key):
    idx = int(id_key[2:])
    appid = processed_ids[idx - 1]
    tail = ["header", 
            "library_header", 
            f"library_header_{locale}",
            "library_header_blur",
            "library_hero",
            "library_hero_blur",
            "logo",
            "library_600x900"
    ]
    image_types = [
        "jpg",
        "png"
    ]
            
    items = os.listdir(f"{image_path}/{appid}")
    # looking for tail + imagetype per folder
    for t in tail:
        for img_type in image_types:
            looking_for_file = f'{t}.{img_type}'

            if os.path.exists(f'{image_path}/{appid}/{looking_for_file}'):
                return f'{looking_for_file}'

            for item in items:
                if os.path.isdir(f"{image_path}/{appid}/{item}"):
                    if os.path.exists(f'{image_path}/{appid}/{item}/{looking_for_file}'):
                        return f"{item}/{looking_for_file}"
    
    # take any other image you can find
    for item in items:
        for img_type in image_types:
            if item.endswith(image_types):
                return item

#__________________________________________________________________________________________________________________________#
#------------------------------------------------Function to write meters--------------------------------------------------#

def write_meters(output, image, image_path, search, hidden_games):
    output_folder = 'dynamicMeters'
    subfolder_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), output_folder)
    os.makedirs(subfolder_path, exist_ok=True)
    config_combined = CaseSensitiveConfigParser()

    # Loop through each regular game ID and create meters
    for i in range(1, game_count + 1):
        id_key = f'ID{i}'
        is_hidden = hidden_games
        meter_data = create_meter(id_key, i, image, image_path, search, is_hidden)
        if search or hidden_games:
            config_combined[f'Name{i}'] = meter_data['Name']
        config_combined[f'Game{i}'] = meter_data['Image']
        if not search:
            config_combined[f'Vis{i}'] = meter_data['String']
        config_combined[f'Gap{i}'] = meter_data['Gap']

    # Loop through each extra game and create meters
    for i in range(1, extra_games_count + 1):
        id_key = f'Egame{i}'
        is_hidden = hidden_games
        meter_data = create_meter(id_key, i, image, image_path, search, is_hidden, is_extra=True, extra_index=i)
        if search or hidden_games:
            config_combined[f'EName{i}'] = meter_data['Name']
        config_combined[f'EGame{i}'] = meter_data['Image']
        if not search:
            config_combined[f'EVis{i}'] = meter_data['String']
        config_combined[f'EGap{i}'] = meter_data['Gap']

    # Write meters to a single file
    output_name = 'dynamicSearchMeters' if search else 'dynamicMeters' if output == 1 else ('dynamicListMeters' if output == 2 and not hidden_games else 'dynamicHiddenMeters')
    output_file = os.path.join(subfolder_path, f'{output_name}.inc')
    with open(output_file, 'w') as configfile:
        for section in config_combined.sections():
            configfile.write(f'[{section}]\n')
            for option, value in config_combined.items(section):
                configfile.write(f'{option}={value}\n')
            configfile.write('\n')
#__________________________________________________________________________________________________________________________#
#--------------------------------------------Function To update GamesInfo.inc----------------------------------------------#

def write_game_info(processed_ids, games_info):
    combined_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'GamesInfo.inc')
    existing_hidden_values = {}
    
    if os.path.exists(combined_file_path):
        with open(combined_file_path, 'r') as combined_file:
            for line in combined_file:
                parts = line.strip().split('=')
                if len(parts) == 2:
                    existing_hidden_values[parts[0]] = parts[1]

    with open(combined_file_path, 'w') as combined_file:
        combined_file.write('[Variables]\n')
        game_count_value = len(processed_ids)
        combined_file.write(f'GameCount={game_count_value}\n')
        hidden_variable_value = len(processed_ids) - sum(1 for app_id in set(processed_ids) if existing_hidden_values.get(app_id, '0') == '1')
        combined_file.write(f'GameCountPLUS={hidden_variable_value}\n')

        for index, game_info in enumerate(games_info, start=1):
            app_id = str(game_info.get('appid', ''))
            if app_id in processed_ids:
                combined_file.write(f'ID{index}={app_id}\n')
                game_name = game_info.get('name', '')
                game_name = ''.join(e for e in game_name if e.isalnum() or e.isspace())
                combined_file.write(f'ID{index}name="{game_name}"\n')

                # Change the next line to add Vis#=0 or Vis#=1 based on the hidden status
                hidden_value = existing_hidden_values.get(app_id, '0')
                combined_file.write(f'Vis{index}={hidden_value}\n' if int(hidden_value) % 2 != 0 else f'Vis{index}=0\n')
#__________________________________________________________________________________________________________________________#
#----------------------------------------------------SCRIPT START HERE-----------------------------------------------------#

# 1: Set Variables
variables = get_variables('SkinInfo.inc')
steam_path = variables.get('steampath', '')
image_path = steam_path + '/appcache/librarycache'
game_dirs = variables.get('gamedirs', '')
game_dirs = game_dirs.split(',')
for i in range(len(game_dirs)):
    game_dirs[i] = game_dirs[i].strip() + '\steamapps'
locale = variables.get('locale', '').lower()
RainmeterPath = variables.get('rainmeterexe', '')
skinMode = variables.get('mode')
skinPath = 'SteamyRain\\'

config_file = fr'SteamyRain.ini' if skinMode == '1' else fr'SteamyRainList.ini'

subprocess.call([RainmeterPath, '!ActivateConfig', fr'{skinPath}Update'])
subprocess.call([RainmeterPath, '!DeactivateConfig', fr'{skinPath}', fr'{config_file}'])

# 2: Find installed game IDs and Names from appmanifest files
status = "Processing appmanifest files..."
processed_ids = []
games_info = []
update_rainmeter_status(status)
for game_dir in game_dirs:
    status = f"Processing files of {game_dir}"
    update_rainmeter_status(status)
    appmanifest_files = [f for f in os.listdir(os.path.join(game_dir)) if f.startswith('appmanifest_')]
    processed_ids_gamedir, games_info_gamedir = process_appmanifest_files(appmanifest_files, game_dir)
    processed_ids = processed_ids + processed_ids_gamedir 
    games_info = games_info + games_info_gamedir
#appmanifest_files = [f for f in os.listdir(os.path.join(manifest_path)) if f.startswith('appmanifest_')]
#processed_ids, games_info = process_appmanifest_files(appmanifest_files, manifest_path)

# 3: Write new GamesInfo.inc
status = "Writing new GamesInfo.inc..."
update_rainmeter_status(status)
write_game_info(processed_ids, games_info)

# 4: Set variables for meters creation
game_count = len(processed_ids)
config_extra_games = CaseSensitiveConfigParser()
config_extra_games.read('NonSteamGames.inc', encoding='utf-8')
extra_games_count = int(config_extra_games.get('Variables', 'ExtraGamesCount', fallback='0'))
#extra_games_count = int(config_extra_games['Variables']['ExtraGamesCount'])

# 5: Create meters dynamically
status = "Creating Dynamic Meters Files..."
update_rainmeter_status(status)

if game_count > 0 or extra_games_count > 0:
    output = 1
    image = 'Logo'
    hidden_games = False
    search = False
    write_meters(output, image, image_path, search, hidden_games)

    output = 2
    hidden_games = False
    write_meters(output, image, image_path, search, hidden_games)

    image = 'Icon'
    hidden_games = True
    write_meters(output, image, image_path, search, hidden_games)

    search = True
    write_meters(output, image, image_path, search, hidden_games)
else:
    # No games found, create empty output files
    subfolder_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dynamicMeters')
    output_file1 = os.path.join(subfolder_path, 'dynamicMeters.inc')
    output_file2 = os.path.join(subfolder_path, 'dynamicListMeters.inc')
    output_file3 = os.path.join(subfolder_path, 'dynamicHiddenMeters.inc')
    output_file4 = os.path.join(subfolder_path, 'dynamicSearchMeters.inc')
    open(output_file1, 'w').close()
    open(output_file2, 'w').close()
    open(output_file3, 'w').close()
    open(output_file4, 'w').close()

subprocess.call([RainmeterPath, '!SetVariable', 'Loop', '3', fr'{skinPath}Update'])