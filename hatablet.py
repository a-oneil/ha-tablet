#! ./venv/bin/python3
# -*- coding: utf-8 -*-
from gpiozero import Button
from signal import pause
import requests,os,json
from dotenv import load_dotenv,dotenv_values
load_dotenv()
config=dotenv_values(os.getenv('ENVLOCATION'))

class HomeAssistant:
    HA_BASE_URL=config['HA_BASE_URL']
    HA_API_KEY=config['HA_API_KEY']
    headers = {'Authorization': f'Bearer {HA_API_KEY}','Content-Type': 'application/json'}

    def __init__(self):
        pass

    def post(self, payload, url):
        response = requests.request("POST", url, headers=self.headers, data=payload)

    def turnon_light(self, light, percentage):
        url = f"{self.HA_BASE_URL}/services/light/turn_on"
        self.payload = json.dumps({
        "entity_id": f"light.{light}",
        "brightness_pct": f"{percentage}",
        })
        self.post(self.payload, url)

    def turnoff_light(self, light):
        url = f"{self.HA_BASE_URL}/services/light/turn_off"
        self.payload = json.dumps({
        "entity_id": f"light.{light}",
        })
        self.post(self.payload, url)

    def toggle_light(self, light):
        url = f"{self.HA_BASE_URL}/services/light/toggle"
        self.payload = json.dumps({
        "entity_id": f"light.{light}",
        })
        self.post(self.payload, url)

    def turnon_switch(self, switch):
        url = f"{self.HA_BASE_URL}/services/switch/turn_on"
        self.payload = json.dumps({
        "entity_id": f"switch.{switch}",
        })
        self.post(self.payload, url)

    def turnoff_switch(self, switch):
        url = f"{self.HA_BASE_URL}/services/switch/turn_off"
        self.payload = json.dumps({
        "entity_id": f"switch.{switch}",
        })
        self.post(self.payload, url)

    def toggle_switch(self, switch):
        url = f"{self.HA_BASE_URL}/services/switch/toggle"
        self.payload = json.dumps({
        "entity_id": f"switch.{switch}",
        })
        self.post(self.payload, url)

    def run_automation(self, automation):
        url = f"{self.HA_BASE_URL}/services/automation/trigger"
        self.payload = json.dumps({
        "entity_id": f"automation.{automation}",
        })
        self.post(self.payload, url)

    def run_script(self, script):
        url = f"{self.HA_BASE_URL}/services/script/turn_on"
        self.payload = json.dumps({
        "entity_id": f"script.{script}",
        })
        self.post(self.payload, url)

ha = HomeAssistant()

held_for=0.0
trigger1time = 0.1
trigger2time = 0.5
trigger3time = 2

noise_message = f"held for under {trigger1time} seconds, probably noise..."

### Top Buttons ###
# CNC Killswitch
def top_right_rls():
	global held_for
	print("released after", held_for, "seconds.")
	if (held_for > trigger1time):
		print('Running actions')
		ha.turnoff_switch("cnc_estop")
		ha.turnoff_switch("cnc_lights")
		ha.turnoff_switch("garage_vacuum")
	elif (held_for < trigger1time):
		print(f"top_right {noise_message}")
	held_for = 0.0

def top_right_hld():
	global held_for
	held_for = max(held_for, top_right.held_time + top_right.hold_time)
	print("held for", held_for, "seconds.")

# Desktop Toggle
def top_left_rls():
	global held_for
	print("released after", held_for, "seconds.")
	if (held_for > trigger1time):
		print('Running actions')
		ha.turnon_switch("desktop_power")
	elif (held_for < trigger1time):
		print(f"top_left {noise_message}")
	held_for = 0.0

def top_left_hld():
	global held_for
	held_for = max(held_for, top_left.held_time + top_left.hold_time)
	print("held for", held_for, "seconds.")

### Middle Buttons ###
# Ender 3 Killswitch
def middle_right_rls():
	global held_for
	print("released after", held_for, "seconds.")
	if (held_for > trigger1time):
		print('Running actions')
		ha.toggle_switch("3d_printer")
		ha.toggle_switch("3d_light")
	elif (held_for < trigger1time):
		print(f"middle_right {noise_message}")
	held_for = 0.0

def middle_right_hld():
	global held_for
	held_for = max(held_for, middle_right.held_time + middle_right.hold_time)
	print("held for", held_for, "seconds.")

# Toggle Basement Lights
def middle_left_rls():
	global held_for
	print("released after", held_for, "seconds.")
	if (held_for > trigger1time) and (held_for < trigger2time):
		print('Running actions 1')
		ha.run_script("toggle_basement_lights")
	elif (held_for > trigger2time):
		print('Running actions 2')
		ha.run_script("basement_lights_100")
	elif (held_for < trigger1time):
		print(f"middle_left {noise_message}")
	held_for = 0.0

def middle_left_hld():
	global held_for
	held_for = max(held_for, middle_left.held_time + middle_left.hold_time)
	print("held for", held_for, "seconds.")

### Bottom Buttons ###
# Toggle Ring Home
def bottom_right_rls():
	global held_for
	print("released after", held_for, "seconds.")
	if (held_for > trigger1time):
		print('Running actions')
		ha.run_script("toggle_ring")
	elif (held_for < trigger1time):
		print(f"bottom_right {noise_message}")
	held_for = 0.0

def bottom_right_hld():
	global held_for
	held_for = max(held_for, bottom_right.held_time + bottom_right.hold_time)
	print("held for", held_for, "seconds.")

# Toggle Basement LED
def bottom_left_rls():
	global held_for
	print("released after", held_for, "seconds.")
	if (held_for > trigger1time):
		print('Running actions')
		ha.toggle_light("basement_strip")
	elif (held_for < trigger1time):
		print(f"bottom_left {noise_message}")
	held_for = 0.0

def bottom_left_hld():
	global held_for
	held_for = max(held_for, bottom_left.held_time + bottom_left.hold_time)
	print("held for", held_for, "seconds.")

top_right=Button(6, hold_time=trigger1time, hold_repeat=True, pull_up = False)
top_left=Button(27, hold_time=trigger1time, hold_repeat=True, pull_up = False)
middle_right=Button(13, hold_time=trigger1time, hold_repeat=True, pull_up = False)
middle_left=Button(22, hold_time=trigger1time, hold_repeat=True, pull_up = False)
bottom_right=Button(26, hold_time=trigger1time, hold_repeat=True, pull_up = False)
bottom_left=Button(23, hold_time=trigger1time, hold_repeat=True, pull_up = False)

top_right.when_held = top_right_hld
top_right.when_released = top_right_rls
top_left.when_held = top_left_hld
top_left.when_released = top_left_rls
middle_right.when_held = middle_right_hld
middle_right.when_released = middle_right_rls
middle_left.when_held = middle_left_hld
middle_left.when_released = middle_left_rls
bottom_right.when_held = bottom_right_hld
bottom_right.when_released = bottom_right_rls
bottom_left.when_held = bottom_left_hld
bottom_left.when_released = bottom_left_rls

pause()
