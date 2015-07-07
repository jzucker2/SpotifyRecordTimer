# SpotifyRecordTimer

## Install Shpotify
Best way to install is with Homebrew:
`brew install shpotify`

## Notifications
Install terminal-notifier if you'd like desktop notifications as well
`brew install terminal-notifier`

## Install a cronjob with something like this:

```bash
TERM=xterm-256color
SHELL=/bin/sh
PATH=/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/opt/X11/bin:/usr/local/git/bin
*/1 * * * * python <path to repo>/SpotifyRecordTimer/spotify_record_timer.py
```
