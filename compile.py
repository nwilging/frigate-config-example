import yaml
import os
from lib import build_config
import copy
import json

MQTT_CONFIG = "./mqtt.yml"
DETECTORS_CONFIG = "./detectors.yml"
OBJECTS_CONFIG = "./objects.yml"

CAMERA_CONFIGS = "./cameras"
TEMPLATE_CONFIGS = "./templates"

output = {}

with open(MQTT_CONFIG, 'r') as mqtt_config_file:
    loaded = yaml.safe_load(mqtt_config_file)['mqtt']
    output['mqtt'] = build_config.build(loaded)
    mqtt_config_file.close()
print("✅    Loaded MQTT config")

with open(DETECTORS_CONFIG, 'r') as detectors_config_file:
    loaded = yaml.safe_load(detectors_config_file)['detectors']
    output['detectors'] = build_config.build(loaded)
    detectors_config_file.close()
print("✅    Loaded Detectors config")

with open(OBJECTS_CONFIG, 'r') as objects_config_file:
    loaded = yaml.safe_load(objects_config_file)['objects']
    output['objects'] = build_config.build(loaded)
    objects_config_file.close()
print("✅    Loaded Objects config")

template_config_listing = os.listdir(TEMPLATE_CONFIGS)
templates = {}

print('Loading templates:')
for template_filename in template_config_listing:
    if not os.path.isfile(os.path.join(TEMPLATE_CONFIGS, template_filename)) or not (template_filename.endswith('.yml') or template_filename.endswith('.yaml')):
        continue

    with open(os.path.join(TEMPLATE_CONFIGS, template_filename)) as file:
        loaded = yaml.safe_load(file)['camera']
        file.close()

    template_name = template_filename.replace('.yml', '').replace('.yaml', '')

    print(f"✅   loaded camera template {template_name}")
    templates[template_name] = loaded

print('--- --- --- --- ---')
print('Loading cameras:')

camera_config_listing = os.listdir(CAMERA_CONFIGS)
cameras = {}

for camera_filename in camera_config_listing:
    if not os.path.isfile(os.path.join(CAMERA_CONFIGS, camera_filename)) or not (camera_filename.endswith('.yml') or camera_filename.endswith('yaml')):
        continue

    with open(os.path.join(CAMERA_CONFIGS, camera_filename)) as file:
        loaded = yaml.safe_load(file)['camera']
        file.close()

    camera_name = loaded['name']
    if 'template' in loaded:
        print(f"Camera {camera_name} uses template -> {loaded['template']}")
        if not loaded['template'] in templates:
            print(f"⚠️  Template {loaded['template']} is not valid. Skipping camera.")
            continue

        template = copy.deepcopy(templates)[loaded['template']]
        template['ffmpeg']['inputs'][0]['path'] = loaded['rtsp_url']

        if 'frigate' in loaded:
            frigate_config = loaded['frigate']
            template.update(frigate_config)

        cameras[camera_name] = build_config.build(template)
    else:
        cameras[camera_name] = build_config.build(loaded)

    print(f"✅   Loaded camera {camera_name}")

output['cameras'] = cameras
with open('output', 'w+') as file:
    file.write(json.dumps(yaml.dump(output)))
    file.close()
