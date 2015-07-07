#!/usr/bin/env python

import subprocess

def poll_spotify():
	return subprocess.check_output(['spotify', 'status'])

def is_spotify_playing():
	result = poll_spotify()
	if 'Spotify is currently playing.' in result:
		return True
	elif 'Spotify is currently paused.' in result:
		return False
	else:
		raise Exception()

def pause_spotify():
	return subprocess.call(['spotify', 'pause'])

def play_spotify():
	return subprocess.call(['spotify', 'play'])

def toggle_spotify_playing(should_play):
	if should_play:
		return play_spotify()
	else:
		return pause_spotify()

def main():
	if is_spotify_playing():
		toggle_spotify_playing(False)


if __name__ == '__main__':
	main()