import os
import json
from dataclasses import dataclass

class DbLocked(Exception):
    def __init__(self, file_name):
        message = f'XP database {file_name} is locked. ' + \
            'If you are sure that another process is not running, ' + \
            'Manually delete the file and start the program again'
        super().__init__(message)

@dataclass
class XpSettings:
    base_char_score = 1
    capital_multiplier = 1.2
    censorship_multiplier = 2
    image_score_per_byte = 1_000_000 / 100
    base_level_size = 1000
    level_size_exponent = 1.2
    xp_gain_exponent = 2 ** (1/10)

def calculate_xp_gain(message: str, image_count: int, current_level: int, settings: XpSettings):
    value = len(message)
    value *= current_level ** settings.xp_gain_exponent
    return value

class XpManager:
    def __init__(self, leaderboard_file_name: str, xp_settings: XpSettings):
        self.leaderboard_file_name = leaderboard_file_name
        self.lock_file_name = leaderboard_file_name + '.lck'
        self.xp_settings = xp_settings

        self.check_lock_file()

        self.load_leaderboard()

    def check_lock_file(self):
        if os.path.exists(self.lock_file_name):
            raise DbLocked()
        
        with open(self.lock_file_name, 'w+') as lock_file:
            lock_file.write('locked')
        
    def load_leaderboard(self):
        self.leaderboard = {}
        with open(self.leaderboard_file_name, 'r') as f:
            self.leaderboard = json.load(f)
    
    def save_leaderboard(self):
        with open(self.leaderboard_file_name, 'w+') as f:
            json.save(f)