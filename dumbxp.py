import os
import jsonpickle
from dataclasses import dataclass
from datetime import datetime
import functools

from better_profanity import profanity
profanity.load_censor_words()
profanity.add_censor_words(['flag'])
import discord

from common import run_bot
from abstract_bot import Bot

class DbLocked(Exception):
    def __init__(self, file_name):
        message = f'XP database {file_name} is locked. ' + \
            'If you are sure that another process is not running, ' + \
            'Manually delete the file and start the program again'
        super().__init__(message)

@dataclass
class XpSettings:
    base_char_score = 1
    capital_multiplier = 2
    profanity_multiplier = 5
    attachment_score_per_byte = 100 / 1_000_000
    image_multiplier = 2
    image_multiplier_duration = 60
    base_level_size = 1000
    level_size_exponent = 1.2
    xp_gain_exponent = 2 ** (1/10)

@dataclass
class UserXp:
    xp: float
    level: int
    image_send_timestamps: list[float]

    def clear_old_image_timestamps(self, current_time: float, settings: XpSettings):
        self.image_send_timestamps = [t for t in self.image_send_timestamps if
            t + settings.image_multiplier_duration >= current_time]
    
    def update_level(self, settings: XpSettings):
        while self.xp > calculate_level_size(self.level + 1, settings):
            self.level += 1

def calculate_xp_gain(message: str, attachment_bytes: int, xp: UserXp, current_time: float, s: XpSettings) -> float:

    def apply_char_based_multiplier(existing_value: float, multiplier: float, num_matching_chars: int) -> float:
        return existing_value + num_matching_chars * (multiplier - 1)

    value = len(message) * s.base_char_score
    value = apply_char_based_multiplier(value, s.profanity_multiplier * s.base_char_score,
        calculate_str_delta(message, profanity.censor(message)))
    value = apply_char_based_multiplier(value, s.capital_multiplier * s.base_char_score,
        [c.isupper() for c in message].count(True))
    
    value += attachment_bytes * s.attachment_score_per_byte

    value *= s.xp_gain_exponent ** xp.level
    value *= s.image_multiplier ** len(xp.image_send_timestamps)


    return value

def calculate_level_size(level: int, settings: XpSettings) -> float:
    multiplier = 1
    for i in range(level):
        multiplier += settings.level_size_exponent * i
    return settings.base_level_size * multiplier

def calculate_str_delta(a: str, b: str) -> int:
    return [i != j for i, j in zip(a, b)].count(True)

def get_user_tag(user: discord.User):
    return user.id

class XpManager:
    def __init__(self, leaderboard_file_name: str, xp_settings: XpSettings):
        self.leaderboard_file_name = leaderboard_file_name
        self.lock_file_name = leaderboard_file_name + '.lck'
        self.xp_settings = xp_settings

        self.check_lock_file()

        self.load_leaderboard()

    def check_lock_file(self):
        if os.path.exists(self.lock_file_name):
            raise DbLocked(self.lock_file_name)
        
        with open(self.lock_file_name, 'w+') as lock_file:
            lock_file.write('locked')
        
    def load_leaderboard(self):
        self.leaderboard = {}
        try:
            with open(self.leaderboard_file_name, 'r') as f:
                self.leaderboard = jsonpickle.decode(f.read())
        except:
            pass
    
    def save_leaderboard(self):
        with open(self.leaderboard_file_name, 'w+') as f:
            f.write(jsonpickle.encode(self.leaderboard))
    
    def get_user(self, username: str) -> UserXp:
        try:
            return self.leaderboard[username]
        except KeyError:
            user = UserXp(0, 0, [])
            self.leaderboard[username] = user
            return user
    
    def apply_xp_from_message(self, message: str, attachment_bytes: int, image_count: int, username: str):
        user = self.get_user(username)
        user.clear_old_image_timestamps(datetime.utcnow().timestamp(), self.xp_settings)
        user.image_send_timestamps += [datetime.utcnow().timestamp()] * image_count
        user.xp += calculate_xp_gain(message, attachment_bytes, user, datetime.utcnow().timestamp(), self.xp_settings)
        user.update_level(self.xp_settings)
    
    def cleanup(self):
        if os.path.exists(self.lock_file_name):
            os.remove(self.lock_file_name)

class DumbXp(Bot):
    '''Intentionally stupid XP bot'''
    START_PREFIX = '/startxp'
    RANK_PREFIX = '/rank'
    LEADERBOARD_PREFIX = '/leaderboard'
    LEADERBOARD_AMOUNT = 10

    def __init__(self, token: str, xp_settings: XpSettings = None):
        super().__init__(token)
        xp_settings = xp_settings or XpSettings()

        self.enabled_servers = []

        self.xp_manager = XpManager('leaderboard.json', xp_settings)
    
    async def on_message(self, message: discord.Message):
        if message.content.startswith(self.START_PREFIX):
            self.enabled_servers.append(message.guild.id)
            await message.reply('Started!')
            return

        if message.guild.id not in self.enabled_servers:
            return

        # Don't reply to self
        if message.author == self.user:
            return
        if message.content.startswith(self.RANK_PREFIX):
            await self.send_rank_message(message)
            return
        if message.content.startswith(self.LEADERBOARD_PREFIX):
            await self.send_leaderboard_message(message)
            return
        
        attachment_bytes = sum([a.size for a in message.attachments])
        image_count = [t.content_type.startswith('image/') for t in message.attachments].count(True)

        user = self.xp_manager.get_user(get_user_tag(message.author))
        old_level = user.level
        self.xp_manager.apply_xp_from_message(message.content, attachment_bytes, image_count, get_user_tag(message.author))
        if user.level != old_level:
            await self.send_level_up_message(message)
    
    async def send_rank_message(self, message: discord.Message):
        if len(message.mentions) == 0:
            await message.reply(f'Please specify a user to rank by mentioning them, eg {self.RANK_PREFIX} @ThatCoolCoder')
            return

        discord_user = message.mentions[0]
        user = self.xp_manager.get_user(get_user_tag(discord_user))
        level_size = calculate_level_size(user.level, self.xp_manager.xp_settings)
        await message.channel.send(f'Ranking info for {message.mentions[0].mention}: {round(user.xp)} xp / {round(level_size)} [level {user.level}]')
    
    async def send_leaderboard_message(self, message: discord.Message):
        users = [(k, v) for k, v in self.xp_manager.leaderboard.items()]
        users.sort(reverse=True, key=lambda u: u[1].xp)
        if len(users) > self.LEADERBOARD_AMOUNT:
            users = users[:self.LEADERBOARD_AMOUNT]
        
        leaderboard_lines = []
        for idx, user_info in enumerate(users):
            user_name, user_xp = user_info
            leaderboard_lines.append(f'{idx + 1}) <@{user_name}> {user_xp.xp} [level {user_xp.level}]')

        await message.channel.send(f'Leaderboard:\n' + '\n'.join(leaderboard_lines))
    
    async def send_level_up_message(self, message: discord.Message):
        user = self.xp_manager.get_user(get_user_tag(message.author))
        await message.channel.send(f'Congrats to {message.author.mention} for reaching level {user.level}!')
    
    def cleanup(self):
        self.xp_manager.cleanup()
        self.xp_manager.save_leaderboard()

if __name__ == '__main__':
    run_bot(DumbXp)