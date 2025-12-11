<img src="doc/imgs/CVLab.png" alt="alt text" width="60%">
# CVLabCore
This package contains all the necessary drivers to control the CVLab platform.
## Examples
For all the examples is necessary to load the configuration files as follows (the given values are just examples): 

```
CWD_PATH = os.getcwd()
CONF_PATH = CWD_PATH + '\\backend\\data\\conf\\'
ROUTINES_PATH = CWD_PATH + '\\backend\\data\\routines\\'

sample = {
        "sample_id": "Carbon",
        "mass": 50.0,
        "tolerance": 1.0,          # optional
        "algorithm": "standard",    # optional, "standard" or "advanced"
        "tapper_intensity": 50,     # optional
        "tapper_duration": 3        # optional
        }
liquid = {
        "liquid_id": "water",
        "volume": 2,
        "source_port": "I1",
        "destination_port": "O1",   
        "waste_port": "O3"
}

config = load_config(conf_file=CONF_PATH+'conf_dummy.json')
```

### Arm
For the Gantry arm of CVLab the Arm class can be configured as follows:
```
arm = Arm(
        name="Arm", 
        arm_url=config.ARM_URL, 
        arm_aux_url=config.PLC_URL, 
        arm_aux_port=config.PLC_PORT)
```
The Arm class can control the gantry robot of CVLab with the following methods:

```
arm.close_gripper();time.sleep(0.3)
arm.close_gripper();time.sleep(0.3)
arm.send_gcode('G1 X10');time.sleep(0.3)
arm.unlock();time.sleep(0.3)
arm.home();time.sleep(0.3)
arm.settings();time.sleep(0.3)
arm.sleep();time.sleep(0.3)
arm.get_position();time.sleep(0.3)
arm.status();time.sleep(0.3)
arm.reset();time.sleep(0.3)
arm.wait_until_idle();time.sleep(0.3)
arm.execute_routine(file=ROUTINES_PATH+'arm\\pick_cartridge_from_tower_1.json');time.sleep(0.3)
```

### Electrochemistry station (Echem)
Echem is the station of CVLab that perform the Cyclic Voltametry tests, it can be defined as follows: 

```
echem = Echem(
        name="Echem", 
        echem_url=config.ECHEM_URL, 
        echem_aux_url=config.ECHEM_AUX_URL, 
        echem_aux_port=config.ECHEM_AUX_PORT,
        pipette_url=config.PIPETTE_URL, 
        pipette_aux_url=config.PIPETTE_AUX_URL,
        pipette_aux_port=config.PIPETTE_AUX_PORT, 
        plc_url=config.PLC_URL,
        plc_port=config.PLC_PORT)
```
Echem can execute the following instructions:

```
    echem.send_gcode('G1 X10');time.sleep(0.3)
    echem.unlock();time.sleep(0.3)
    echem.home();time.sleep(0.3)
    echem.settings();time.sleep(0.3)
    echem.sleep();time.sleep(0.3)
    echem.get_position();time.sleep(0.3)
    echem.reset();time.sleep(0.3)
    echem.wait_until_idle();time.sleep(0.3)
    echem.execute_routine(file=ROUTINES_PATH+'echem\\pre_submerge_in_row_1.json');time.sleep(0.3)
    echem.polisher_on();time.sleep(0.3)
    echem.polisher_off();time.sleep(0.3)
    echem.polisher_dropper_on();time.sleep(0.3)
    echem.polisher_dropper_off();time.sleep(0.3)
    echem.dryer_on();time.sleep(0.3)
    echem.dryer_off();time.sleep(0.3)
    echem.purger_on();time.sleep(0.3)
    echem.purger_off();time.sleep(0.3)
    echem.polisher_set_speed('slow');time.sleep(0.3)
    echem.pipette_arm_home();time.sleep(0.3)
    echem.pipette_arm_unlock();time.sleep(0.3)
    echem.pipette_arm_sleep();time.sleep(0.3)
    echem.pipette_arm_reset();time.sleep(0.3)
    echem.pipete_arm_send_gcode(gcode="G90");time.sleep(0.3)
    echem.pipette_arm_execute_routine(file=ROUTINES_PATH+'pipette\\above_electrode_1.json');time.sleep(0.3)
    echem.pipette_home();time.sleep(0.3)
    echem.pipette_eject_tip();time.sleep(0.3)
    echem.pipette_preload();time.sleep(0.3)
    echem.pipette_load();time.sleep(0.3)
    echem.pipette_unload();time.sleep(0.3)
    echem.pipette_set_speed(speed='slow');time.sleep(0.3)
```
