#!/bin/bash

SESSION="beavy"

tmux -2 new-session -d -s $SESSION
tmux new-window -t $SESSION:1 -n
tmux split-window -v
tmux select-pane -t 1
tmux split-window -h
tmux send-keys "python install.py && python manager.py db upgrade heads && flask --app=main --debug run"  C-m
tmux select-pane -t 1
tmux send-keys "npm install && npm run hot-dev-server" C-m
tmux select-pane -t 0
tmux -2 attach-session -t $SESSION
