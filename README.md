# SpotifyRecordTimer

## Install a cronjob with something like this:

*/5 * * * * [ $(( $(date +%s) / 60 % 25 )) -eq 0 ] && python <path to repo>/SpotifyRecordTimer/spotify_record_timer.py
