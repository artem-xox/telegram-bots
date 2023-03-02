#!/bin/sh
/usr/bin/sleep 60s

/usr/bin/bash -c 'cd /home/artem/server/telegram-bots/dalle && make docker-run' &
/usr/bin/bash -c 'cd /home/artem/server/telegram-bots/codex && make docker-run' &
/usr/bin/bash -c 'cd /home/artem/server/telegram-bots/chat && make docker-run'