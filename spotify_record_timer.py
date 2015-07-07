#!/usr/bin/env python

import subprocess
import json
import time
import os

# this must be a round number
MINUTES_UNTIL_PAUSE = 25
SPOTIFY_PATH = 'spotify'
NOTIFIER_PATH = 'terminal-notifier'
PUSH_ICON = 'push_icon.png'
SPOTIFY_BUNDLE_ID = 'com.spotify.client'

class PushNotifier(object):
	"""docstring for PushNotifier"""
	def __init__(self):
		super(PushNotifier, self).__init__()
	def is_notifier_installed(self):
		result = subprocess.Popen(['which', NOTIFIER_PATH], stdin=subprocess.PIPE, stdout=subprocess.PIPE).communicate()
		if len(result[0]) > 0:
			return True
		else:
			return False
	def get_push_message(self):
		return 'Stand up!'
	def get_push_sound(self):
		return 'default'
	def get_push_group(self):
		return 'SpotifyRecordPlayer'
	def get_push_title(self):
		return 'Spotify Record Player'
	def get_push_app_icon(self):
		current_directory = os.path.dirname(os.path.realpath(__file__))
		return os.path.join(current_directory, PUSH_ICON)
	def get_push_sender(self):
		return SPOTIFY_BUNDLE_ID
	def send_desktop_notification(self):
		result = subprocess.Popen([NOTIFIER_PATH, '-group', self.get_push_group(), '-sound', self.get_push_sound(), '-title', self.get_push_title(), '-message', self.get_push_message(), '-appIcon', self.get_push_app_icon(), '-sender', self.get_push_sender()], stdin=subprocess.PIPE, stdout=subprocess.PIPE).communicate()
		return result


class SpotifyHandler(object):
	"""docstring for SpotifyHandler"""
	def __init__(self):
		super(SpotifyHandler, self).__init__()
	def poll_spotify(self):
		result = subprocess.Popen([SPOTIFY_PATH, 'status'], stdin=subprocess.PIPE, stdout=subprocess.PIPE).communicate()
		return result[0]

	def is_spotify_playing(self):
		result = self.poll_spotify()
		if 'Spotify is currently playing.' in result:
			return True
		elif 'Spotify is currently paused.' in result:
			return False
		else:
			raise Exception()
	def is_command_line_installed(self):
		result = subprocess.Popen(['which', SPOTIFY_PATH], stdin=subprocess.PIPE, stdout=subprocess.PIPE).communicate()
		if len(result[0]) > 0:
			return True
		else:
			return False

	def pause_spotify(self):
		result = subprocess.Popen([SPOTIFY_PATH, 'pause'], stdin=subprocess.PIPE, stdout=subprocess.PIPE).communicate()
		return result[0]

	def play_spotify(self):
		result = subprocess.Popen([SPOTIFY_PATH, 'play'], stdin=subprocess.PIPE, stdout=subprocess.PIPE).communicate()
		return result[0]

	def toggle_spotify_playing(self, should_play):
		if should_play:
			return self.play_spotify()
		else:
			return self.pause_spotify()

class TimeChecker(object):
	"""docstring for TimeChecker"""
	def get_number_of_checks_file(self):
		current_directory = os.path.dirname(os.path.realpath(__file__))
		return os.path.join(current_directory, 'number_of_checks.json')
	def create_number_of_checks_file_if_needed(self):
		if not os.path.exists(self.get_number_of_checks_file()):
			with open(self.get_number_of_checks_file(), 'w') as checks_file:
				checks = {'checks' : 0, 'last_updated' : self.current_time}
				json.dump(checks, checks_file)
	def get_number_of_checks(self):
		with open(self.get_number_of_checks_file()) as checks_file:
			data = json.load(checks_file)
			self.checks = data
	def __init__(self):
		super(TimeChecker, self).__init__()
		self.current_time = time.time()
		self.create_number_of_checks_file_if_needed()
		self.get_number_of_checks()
	def update_number_of_checks(self):
		current_number_of_checks = self.checks['checks']
		updated_number_of_checks = current_number_of_checks
		if current_number_of_checks >= (MINUTES_UNTIL_PAUSE - 1):
			updated_number_of_checks = 0
		else:
			updated_number_of_checks += 1
		with open(self.get_number_of_checks_file(), 'w') as checks_file:
			checks = {'checks' : updated_number_of_checks, 'last_updated' : self.current_time}
			json.dump(checks, checks_file)
	def reset_number_of_checks(self):
		with open(self.get_number_of_checks_file(), 'w') as checks_file:
			checks = {'checks' : 0, 'last_updated' : self.current_time}
			json.dump(checks, checks_file)
	def should_pause(self):
		current_number_of_checks = self.checks['checks']
		last_check_time = self.checks['last_updated']
		if self.current_time - last_check_time >= (MINUTES_UNTIL_PAUSE * 60):
			return True
		elif current_number_of_checks == (MINUTES_UNTIL_PAUSE - 1):
			return True
		else:
			return False

def main():
	spotify = SpotifyHandler()
	if not spotify.is_command_line_installed():
		print 'Spotify is not installed or in crontab PATH'
		print 'Install with "brew install shpotify"'
		return
	checker = TimeChecker()
	# don't check or update number of checks if spotify is not playing
	if not spotify.is_spotify_playing():
		checker.reset_number_of_checks()
		return
	if checker.should_pause():
		if spotify.is_spotify_playing():
			spotify.toggle_spotify_playing(False)
			notifier = PushNotifier()
			# only run if notifier is installed and found in path
			if notifier.is_notifier_installed():
				notifier.send_desktop_notification()
			# if we toggle off, make sure to reset number of checks!
			checker.reset_number_of_checks()
	# don't forget to update number of checks afterwards
	checker.update_number_of_checks()



if __name__ == '__main__':
	main()