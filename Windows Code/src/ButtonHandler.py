from ConfigHandler import *
from pynput.keyboard import Key, Controller
import psutil
import os


class Button:
    def __init__(self, but_num, sub_settings, leds_on, log):
        self.sub_settings = sub_settings  # give the first button a number (used to open the program)
        self.leds_on = leds_on # Get the debugging settings
        self.but_num = but_num  # give a ID to the button
        self.l = log  # assign logger class
        self.keyboard = Controller()  # assign the controllor class for the keyboard simulator
        self.apply_settings = False

    def open_app(self):
        if os.path.splitext(os.path.basename(self.sub_settings[1]))[1] == '.lnk':
            os.startfile(self.sub_settings[1])
        elif self.sub_settings[1]:
            psutil.Popen(self.sub_settings[1])

    def close_app(self):
        if self.sub_settings[1]:
            try:
                for process in psutil.process_iter():
                    temp1 = os.path.splitext(process.name())[0]
                    temp2 = os.path.splitext(os.path.basename(self.sub_settings[1]))[0]
                    if temp1 == temp2:
                        process.kill()
            except psutil.NoSuchProcess:
                print('nasty error')

    def sim_key(self):
        if self.sub_settings[3]:
            if self.sub_settings[3] == config_keypress_options[0]:
                self.keyboard.press(Key.alt)
                self.keyboard.release(Key.alt)
            elif self.sub_settings[3] == config_keypress_options[1]:
                self.keyboard.press(Key.backspace)
                self.keyboard.release(Key.backspace)
            elif self.sub_settings[3] == config_keypress_options[2]:
                self.keyboard.press(Key.caps_lock)
                self.keyboard.release(Key.caps_lock)
            elif self.sub_settings[3] == config_keypress_options[3]:
                self.keyboard.press(Key.cmd)
                self.keyboard.release(Key.cmd)
            elif self.sub_settings[3] == config_keypress_options[4]:
                self.keyboard.press(Key.ctrl)
                self.keyboard.release(Key.ctrl)
            elif self.sub_settings[3] == config_keypress_options[5]:
                self.keyboard.press(Key.delete)
                self.keyboard.release(Key.delete)
            elif self.sub_settings[3] == config_keypress_options[6]:
                self.keyboard.press(Key.enter)
                self.keyboard.release(Key.enter)
            elif self.sub_settings[3] == config_keypress_options[7]:
                self.keyboard.press(Key.esc)
                self.keyboard.release(Key.esc)
            elif self.sub_settings[3] == config_keypress_options[8]:
                self.keyboard.press(Key.num_lock)
                self.keyboard.release(Key.num_lock)
            elif self.sub_settings[3] == config_keypress_options[9]:
                self.keyboard.press(Key.pause)
                self.keyboard.release(Key.pause)
            elif self.sub_settings[3] == config_keypress_options[10]:
                self.keyboard.press(Key.print_screen)
                self.keyboard.release(Key.print_screen)
            elif self.sub_settings[3] == config_keypress_options[11]:
                # Toggle keypad leds
                self.leds_on[0] = not self.leds_on[0]
                self.apply_settings = True
            elif self.sub_settings[3] == config_keypress_options[12]:
                self.keyboard.press(Key.cmd)
                self.keyboard.press(Key.tab)
                self.keyboard.release(Key.tab)
                self.keyboard.release(Key.cmd)

    def update_apply_settings(self):
        self.apply_settings = False

    def update_settings(self, sub_settings):
        self.sub_settings = sub_settings

    def state_machine(self):
        if self.sub_settings[0] == True:  # this button should open/close a program
            if self.sub_settings[2] == True:  # this button should open a program
                self.open_app()
            elif self.sub_settings[2] == False:  # this button should close a program
                self.close_app()
            else:
                return  # the config file is incorrect so do notting
        elif self.sub_settings[0] == False:  # this button should simulate a keypress of a keyboard
            self.sim_key()
        else:
            return  # the config file is incorrect so do notting


def main():
    l = Logger(Filename_Logger)
    c = ConfigFileHandler(Filename_Config_keypress, l, config_key_sections_check, config_key_items_check,
                          config_key_items_data)  # key configuration
    d = ConfigFileHandler(Filename_Config_debugging, l, config_debugging_sections_check, config_debugging_items_check,
                          config_debugging_items_data)  # debugging configuration
    buttons = list()
    for i in range(16):
        buttons.append(Button(i, c.settings[i], l))  # initialize button objects
    counter = 2
    while True:
        if counter >= update_settings_counter:
            print('Enter a number between 0 and 15')
            button_num = int(input())  # simulate button press event
            c.check_config_file()  # check the config file for correctness
            c.update_settings()  # the config file is correct so update the settings
            buttons[button_num].state_machine()  # open/close/simulate keypress depending on the settings
            counter = 0
        counter = counter + 1
        time.sleep(sleep_time)


if __name__ == '__main__':
    main()
