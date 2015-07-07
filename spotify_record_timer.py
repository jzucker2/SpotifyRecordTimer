#!/usr/bin/env python

import subprocess
import json
import time
import os

MINUTES_UNTIL_PAUSE = 25

class SpotifyHandler(object):
	"""docstring for SpotifyHandler"""
	def __init__(self):
		super(SpotifyHandler, self).__init__()
	def poll_spotify(self):
		return subprocess.check_output(['spotify', 'status'])

	def is_spotify_playing(self):
		result = self.poll_spotify()
		if 'Spotify is currently playing.' in result:
			return True
		elif 'Spotify is currently paused.' in result:
			return False
		else:
			raise Exception()

	def pause_spotify(self):
		return subprocess.call(['spotify', 'pause'])

	def play_spotify(self):
		return subprocess.call(['spotify', 'play'])

	def toggle_spotify_playing(self, should_play):
		if should_play:
			return self.play_spotify()
		else:
			return self.pause_spotify()

class TimeChecker(object):
	"""docstring for TimeChecker"""
	def __init__(self):
		super(TimeChecker, self).__init__()
		self.current_time = time.time()
	def get_number_of_checks_file(self):
		current_directory = os.path.dirname(os.path.realpath(__file__))
		return os.path.join(current_directory, 'number_of_checks.json')
	def get_number_of_checks(self):
		with open(self.get_number_of_checks_file()) as checks_file:
			data = json.load(checks_file)
			self.checks = data
	def update_number_of_checks(self):
		current_number_of_checks = self.checks['checks']
		updated_number_of_checks = current_number_of_checks
		if current_number_of_checks >= 24:
			updated_number_of_checks = 0
		else:
			updated_number_of_checks += 1
		with open(self.get_number_of_checks_file(), 'w') as checks_file:
			checks = {'checks' : updated_number_of_checks, 'last_updated' : self.current_time}
			json.dump(checks, checks_file)
	def should_pause(self):
		current_number_of_checks = self.checks['checks']
		last_check_time = self.checks['last_updated']
		if self.current_time - last_check_time > (25*60):
			return True
		elif current_number_of_checks = 24:
			return True
		else:
			return False

def main():
	checker = TimeChecker()
	checker.get_number_of_checks()
	if checker.should_pause():
		spotify = SpotifyHandler()
		if spotify.is_spotify_playing():
			spotify.toggle_spotify_playing(False)
	# don't forget to update number of checks afterwards
	checker.update_number_of_checks()


if __name__ == '__main__':
	main()