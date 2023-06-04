import os
import jsonpickle
from dataclasses import dataclass
from datetime import datetime
import functools
import enum

from better_profanity import profanity
profanity.load_censor_words()
import discord

from common import run_bot
from abstract_bot import Bot

# A note on levels:
# A user's level is the highest level

class DbLocked(Exception):
    def __init__(self, file_name):
        message = f'XP database {file_name} is locked. ' + \
            'If you are sure that another process is not running, ' + \
            'Manually delete the file and start the program again'
        super().__init__(message)

@dataclass
class XpSettings:
    base_char_score = 1
    message_length_exponent = 1/3
    message_length_break_even_point = 100 # The point at which base_char_score * len(message) == (base_char_score * len(message)) ^ message_length_exponent
    capital_multiplier = 2
    profanity_multiplier = 3
    multiplier_char_exponent = 1/2
    multiplier_char_break_even_point = 4
    attachment_score_per_byte = 100 / 1_000_000
    image_multiplier = 2
    image_multiplier_duration = 60
    base_level_size = 1000
    level_size_exponent = 1.232
    xp_gain_exponent = 1.184
    score_square_words = ['square', 'squared', 'quadratic', 'parabola'] # score is squared if you say this word

# Info about what boosts were applied during the scoring of a message
class XpGainFlags(enum.Flag):
    NONE = 0
    PROFANITY = enum.auto()
    CAPITALS = enum.auto()
    IMAGE_BOOST = enum.auto()
    SQUARED = enum.auto()

@dataclass
class UserXp:
    xp: int
    image_send_timestamps: list[float]
    squared_message_count = 0

    def clear_old_image_timestamps(self, current_time: float, settings: XpSettings):
        self.image_send_timestamps = [t for t in self.image_send_timestamps if
            t + settings.image_multiplier_duration >= current_time]
    
    def calc_level(self, settings: XpSettings):
        target = self.xp / settings.base_level_size
        multiplier = 1
        level = 0
        last_delta = 1
        while multiplier < target:
            level += 1
            multiplier += last_delta
            last_delta *= settings.level_size_exponent
        return level

def apply_exponent_with_break_even_point(value: float, exponent: float, break_even_point: float) -> float:
    return value ** exponent * (break_even_point / break_even_point ** exponent)

def apply_char_based_multiplier(existing_value: float, multiplier: float, num_matching_chars: int, message_length: int) -> float:
    if message_length == 0:
        return existing_value
    return existing_value + existing_value * (num_matching_chars / message_length * (multiplier - 1))

def calculate_xp_gain(message: str, attachment_bytes: int, xp: UserXp, current_time: float, s: XpSettings) -> (int, XpGainFlags):
    flags = XpGainFlags.NONE

    length = len(message)

    if any([x in message for x in s.score_square_words]):
        length *= length
        flags |= XpGainFlags.SQUARED

    value = length * s.base_char_score
    value = apply_exponent_with_break_even_point(value, s.message_length_exponent, s.message_length_break_even_point)

    profanity_count = calculate_str_delta(message, profanity.censor(message))
    profanity_count = apply_exponent_with_break_even_point(profanity_count, s.multiplier_char_exponent, s.multiplier_char_break_even_point)
    if profanity_count:
        flags |= XpGainFlags.PROFANITY
    value = apply_char_based_multiplier(value, s.profanity_multiplier * s.base_char_score, profanity_count, length)

    capital_count = [c.isupper() for c in message].count(True)
    capital_count = apply_exponent_with_break_even_point(capital_count, s.multiplier_char_exponent, s.multiplier_char_break_even_point)
    if profanity_count:
        flags |= XpGainFlags.CAPITALS
    value = apply_char_based_multiplier(value, s.capital_multiplier * s.base_char_score, capital_count, length)
    
    value += attachment_bytes * s.attachment_score_per_byte

    value *= s.xp_gain_exponent ** xp.calc_level(s)
    value *= s.image_multiplier ** len(xp.image_send_timestamps)
    if len(xp.image_send_timestamps):
        flags |= XpGainFlags.IMAGE_BOOST

    return (int(value), flags)

def calculate_level_size(level: int, settings: XpSettings) -> float:
    multiplier = 1
    last_delta = 1
    for i in range(level):
        multiplier += last_delta
        last_delta *= settings.level_size_exponent
    return settings.base_level_size * multiplier

def calculate_str_delta(a: str, b: str) -> int:
    return [i != j for i, j in zip(a, b)].count(True)

def get_user_tag(user: discord.User):
    return str(user.id)

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
            user = UserXp(0, [])
            self.leaderboard[username] = user
            return user
    
    def apply_xp_from_message(self, message: str, attachment_bytes: int, image_count: int, username: str):
        user = self.get_user(username)
        user.clear_old_image_timestamps(datetime.utcnow().timestamp(), self.xp_settings)
        user.image_send_timestamps += [datetime.utcnow().timestamp()] * image_count
        score, flags = calculate_xp_gain(message, attachment_bytes, user, datetime.utcnow().timestamp(), self.xp_settings)
        user.xp = int(user.xp) + score
        if XpGainFlags.SQUARED in flags:
            user.squared_message_count += 1
    
    def cleanup(self):
        if os.path.exists(self.lock_file_name):
            os.remove(self.lock_file_name)

class DumbXp(Bot):
    '''Intentionally stupid XP bot'''
    START_PREFIX = '/xpstart'
    RANK_PREFIX = '/xprank'
    LEADERBOARD_PREFIX = '/xpleaderboard'
    LEADERBOARD_AMOUNT = 10
    SAVE_INTERVAL = 10
    SQUARED_BOOST_OVERUSE_AMOUNT = 3

    def __init__(self, token: str, xp_settings: XpSettings = None):
        super().__init__(token)
        xp_settings = xp_settings or XpSettings()

        self.enabled_servers = []
        self.message_counter = 0

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
        old_level = user.calc_level(self.xp_manager.xp_settings)
        self.xp_manager.apply_xp_from_message(message.content, attachment_bytes, image_count, get_user_tag(message.author))
        if user.squared_message_count >= self.SQUARED_BOOST_OVERUSE_AMOUNT:
            await self.send_stop_squaring_message(message)
            user.squared_message_count = 0
        if user.calc_level(self.xp_manager.xp_settings) != old_level:
            await self.send_level_up_message(message)

        self.message_counter += 1
        if self.message_counter % self.SAVE_INTERVAL == 0:
            self.message_counter = 0
            self.xp_manager.save_leaderboard()
    
    async def send_rank_message(self, message: discord.Message):
        if len(message.mentions) == 0:
            await message.reply(f'Please specify a user to rank by mentioning them, eg {self.RANK_PREFIX} @ThatCoolCoder')
            return

        discord_user = message.mentions[0]
        user = self.xp_manager.get_user(get_user_tag(discord_user))
        level = user.calc_level(self.xp_manager.xp_settings)
        level_size = calculate_level_size(level + 1, self.xp_manager.xp_settings)
        await message.channel.send(f'Ranking info for {message.mentions[0].mention}: {round(user.xp)} xp / {round(level_size)} [level {level}]')
    
    async def send_leaderboard_message(self, message: discord.Message):
        users = [(k, v) for k, v in self.xp_manager.leaderboard.items()]
        users.sort(reverse=True, key=lambda u: u[1].xp)
        if len(users) > self.LEADERBOARD_AMOUNT:
            users = users[:self.LEADERBOARD_AMOUNT]

        leaderboard_lines = []
        for idx, user_info in enumerate(users):
            user_name, user_xp = user_info
            leaderboard_lines.append(f'{idx + 1}) <@{user_name}> {round(user_xp.xp)} xp [level {user_xp.calc_level(self.xp_manager.xp_settings)}]')

        await message.channel.send(f'Leaderboard:\n' + '\n'.join(leaderboard_lines))
    
    async def send_level_up_message(self, message: discord.Message):
        user = self.xp_manager.get_user(get_user_tag(message.author))
        await message.channel.send(f'Congrats to {message.author.mention} for reaching level {user.calc_level(self.xp_manager.xp_settings)}!')
    
    async def send_stop_squaring_message(self, message: discord.Message):
        await message.reply('Stop trying to game the system')
    
    def cleanup(self):
        self.xp_manager.cleanup()
        self.xp_manager.save_leaderboard()

if __name__ == '__main__':
    run_bot(DumbXp)