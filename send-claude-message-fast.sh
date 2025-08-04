#!/bin/bash

# Fast version of send-claude-message.sh
# Removes the 0.5s sleep for faster operation
# Usage: send-claude-message-fast.sh <session:window> <message>

if [ $# -lt 2 ]; then
    echo "Usage: $0 <session:window> <message>"
    echo "Example: $0 api_builder:3 'Hello Claude!'"
    exit 1
fi

WINDOW="$1"
shift  # Remove first argument, rest is the message
MESSAGE="$*"

# Send the message and Enter in rapid succession
tmux send-keys -t "$WINDOW" "$MESSAGE" Enter

echo "Message sent to $WINDOW"