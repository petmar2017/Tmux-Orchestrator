#!/bin/bash

# Gemini API Builder - Quick Start Guide

# A native Tmux Orchestrator implementation for building complete API systems with 7 specialized AI agents powered by Gemini.

echo "🚀 Gemini API Builder - Quick Start Guide"
echo "=================================================="
echo "This script will guide you through setting up and running the API builder with Gemini."

# Prerequisites Check
echo "Checking prerequisites..."
if ! command -v tmux &> /dev/null;
then
    echo "Error: tmux is not installed. Please install it first."
    exit 1
fi
if ! command -v gemini &> /dev/null;
then
    echo "Error: gemini is not installed. Please install it first."
    exit 1
fi
echo "Prerequisites met."

# Step 1: Run Setup Script
echo -e "\nStep 1: Running Setup Script..."
cd /Users/petermager/Downloads/code/Tmux-Orchestrator
./api_builder/setup_api_builder.sh

if [ $? -ne 0 ]; then
    echo "Error: setup_api_builder.sh failed to execute."
    exit 1
fi
echo "Setup script completed successfully."

# Step 2: Attach to Session
echo -e "\nStep 2: Attach to Session"
echo "To attach to the tmux session, run the following command:"
echo "./attach_api_builder.sh"
echo "You'll see:"
echo "- Window 0: Orchestrator (you start here)"
echo "- Window 1-7: Agent windows (ready for Gemini)"

# Step 3: Start the Orchestrator
echo -e "\nStep 3: Start the Orchestrator"
echo "In Window 0, start Gemini:"
echo "gemini"
echo "Then paste the orchestrator prompt:"
echo "cat api_builder/prompts/prompt_orchestrator.md"

# Step 4: Let the Orchestrator Initialize Agents
echo -e "\nStep 4: Let the Orchestrator Initialize Agents"
echo "The orchestrator will:"
echo "1. Send initialization messages to each agent window"
echo "2. Distribute initial tasks"
echo "3. Monitor progress"
echo "4. Schedule regular check-ins"

# Agent Roles
echo -e "\n🤖 Agent Roles"
echo "| Window | Agent          | Responsibility                 |"
echo "|--------|----------------|--------------------------------|"
echo "| 0      | Orchestrator   | High-level coordination        |"
echo "| 1      | Lead Developer | Team management, git, architecture |"
echo "| 2      | FastAPI Dev    | REST APIs, database models     |"
echo "| 3      | MCP Server Dev | Claude tools, MCP protocol     |"
echo "| 4      | Make Builder   | Build automation, Makefile     |"
echo "| 5      | Documentation  | README, guides, API docs       |"
echo "| 6      | E2E Tester     | pytest, test coverage          |"
echo "| 7      | Jupyter Dev    | Interactive notebooks          |"

# Manual Agent Setup (If Needed)
echo -e "\n📝 Manual Agent Setup (If Needed)"
echo "If you want to manually start agents:"
echo "For Each Agent Window (1-7):"
echo "1. Switch to window: Ctrl+B then [number]"
echo "2. Start Gemini: gemini"
echo "3. Paste agent prompt:"
echo "   # For Lead Developer (Window 1)"
echo "   cat api_builder/prompts/prompt_lead.md"
echo "   # For FastAPI (Window 2)"
echo "   cat api_builder/prompts/prompt_fastapi.md"
echo "   # And so on..."

# Communication Between Agents
echo -e "\n🔧 Communication Between Agents"
echo "Agents communicate using:"
echo "# Send message to any agent"
echo "./send-gemini-message.sh api_builder:[window] \"Your message\""
echo "# Examples:"
echo "./send-gemini-message.sh api_builder:1 \"Status update please\""
echo "./send-gemini-message.sh api_builder:2 \"Create user authentication endpoints\""

# Monitoring Progress
echo -e "\n📊 Monitoring Progress"
echo "From Orchestrator (Window 0)"
echo "# Check any agent's output"
echo "tmux capture-pane -t api_builder:1 -p | tail -30"
echo "# Check all windows"
echo "for i in {1..7}; do"
echo "  echo \"=== Window $i ===\""
echo "  tmux capture-pane -t api_builder:$i -p | tail -5"
echo "done"
echo "Check Git Commits"
echo "cd api_builder/workspace"
echo "git log --oneline -10"

# Scheduling
echo -e "\n⏰ Scheduling"
echo "Agents self-schedule check-ins:"
echo "# Schedule a check-in"
echo "./schedule_with_note.sh 30 \"Review API endpoints\" \"api_builder:2\""

# Project Structure
echo -e "\n📁 Project Structure"
echo "api_builder/"
echo "├── workspace/          # Where code is built"
echo "│   ├── api/           # FastAPI code"
echo "│   ├── mcp_server/    # MCP server"
echo "│   ├── tests/         # Test suites"
echo "│   ├── notebooks/     # Jupyter notebooks"
echo "│   ├── docs/          # Documentation"
echo "│   └── scripts/       # Utility scripts"
echo "├── prompts/           # Agent prompts"
echo "├── tasks/             # Task definitions"
echo "└── setup_api_builder.sh"

# Expected Timeline
echo -e "\n🎯 Expected Timeline"
echo "- Hour 1: Project setup, git init, basic structure"
echo "- Hour 2-3: Core API with auth and database"
echo "- Hour 4-5: MCP server and tools"
echo "- Hour 6: Tests and documentation"
echo "- Ongoing: Agents work autonomously with 30-min commits"

# Troubleshooting
echo -e "\n🚨 Troubleshooting"
echo "| Issue                  | Solution                                           |"
echo "|------------------------|----------------------------------------------------|"
echo "| Agent not responding   | Check window with 'tmux capture-pane', restart Gemini if needed |"
echo "| Can't send messages    | Verify session exists: 'tmux list-sessions'        |"
echo "| Git not initialized    | Tell Lead Developer to run 'git init'              |"
echo "| Tasks not distributed  | Check orchestrator is running in Window 0          |"

# Success Indicators
echo -e "\n🎉 Success Indicators"
echo "- All agents acknowledging tasks"
echo "- Regular git commits (every 30 min)"
echo "- API endpoints responding"
echo "- Tests passing"
echo "- Documentation growing"
echo "- Agents communicating status updates"

# Tips
echo -e "\n💡 Tips"
echo "1. Let agents work autonomously - Don't micromanage"
echo "2. Monitor git commits - Ensures progress is saved"
echo "3. Use orchestrator for big decisions - Agents handle details"
echo "4. Check Window 0 regularly - Orchestrator provides overview"
echo "5. Trust the process - Agents will self-organize"

# Next Steps
echo -e "\nNext Steps"
echo "After setup:"
echo "1. Watch the orchestrator coordinate the team"
echo "2. Monitor git commits appearing every 30 minutes"
echo "3. Check the API being built in 'workspace/api/'"
echo "4. Review documentation in 'workspace/docs/'"
echo "5. Let the system run - agents work 24/7!"

echo -e "\n**Ready!** Your API Builder team is now operational. The orchestrator will coordinate everything automatically. 🚀"

# Create a Gemini-specific message sender
cat > send-gemini-message.sh << 'EOF'
#!/bin/bash

# Send message to Gemini agent in tmux window
# Usage: send-gemini-message.sh <session:window> <message>

if [ $# -lt 2 ]; then
    echo "Usage: $0 <session:window> <message>"
    echo "Example: $0 agentic-seek:3 'Hello Gemini!'"
    exit 1
fi

WINDOW="$1"
shift  # Remove first argument, rest is the message
MESSAGE="$*"

# Send the message
tmux send-keys -t "$WINDOW" "$MESSAGE"

# Wait 0.5 seconds for UI to register
sleep 0.5

# Send Enter to submit
tmux send-keys -t "$WINDOW" Enter

echo "Message sent to $WINDOW: $MESSAGE"
EOF

chmod +x send-gemini-message.sh

echo -e "\nCreated 'send-gemini-message.sh' for agent communication."
