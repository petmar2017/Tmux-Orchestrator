#!/bin/bash

# Auto-brief a Claude agent with a prompt file
# Usage: ./auto_brief_agent.sh <session:window> <prompt_file> <agent_name>

SESSION_WINDOW=$1
PROMPT_FILE=$2
AGENT_NAME=${3:-"Agent"}

if [ -z "$SESSION_WINDOW" ] || [ -z "$PROMPT_FILE" ]; then
    echo "Usage: $0 <session:window> <prompt_file> [agent_name]"
    echo "Example: $0 api_builder:1 prompts/prompt_lead.md 'Lead Developer'"
    exit 1
fi

if [ ! -f "$PROMPT_FILE" ]; then
    echo "Error: Prompt file not found: $PROMPT_FILE"
    exit 1
fi

echo "🤖 Auto-briefing $AGENT_NAME at $SESSION_WINDOW..."

# Clear the window
tmux send-keys -t "$SESSION_WINDOW" C-c 2>/dev/null || true
sleep 0.5
tmux send-keys -t "$SESSION_WINDOW" "clear" Enter
sleep 0.5

# Start Claude
echo "  Starting Claude..."
tmux send-keys -t "$SESSION_WINDOW" "claude" Enter
sleep 5  # Wait for Claude to fully initialize

# Read the prompt file and send it in chunks
echo "  Sending prompt..."

# Method 1: Try using send-claude-message.sh if available
if [ -f "./send-claude-message.sh" ]; then
    # Read file content
    PROMPT_CONTENT=$(cat "$PROMPT_FILE")
    
    # Send the prompt using the reliable message script
    ./send-claude-message.sh "$SESSION_WINDOW" "$PROMPT_CONTENT"
    
    echo "  ✅ Prompt sent via send-claude-message.sh"
else
    # Method 2: Direct sending (backup method)
    # Send the prompt line by line with small delays
    while IFS= read -r line; do
        if [ ! -z "$line" ]; then
            tmux send-keys -t "$SESSION_WINDOW" "$line"
            tmux send-keys -t "$SESSION_WINDOW" Enter
            sleep 0.1
        fi
    done < "$PROMPT_FILE"
    
    # Send final Enter to submit
    sleep 1
    tmux send-keys -t "$SESSION_WINDOW" Enter
    
    echo "  ✅ Prompt sent directly"
fi

echo "✅ $AGENT_NAME briefed successfully!"