# 🚀 Tmux Orchestrator - Quick Start Guide

Get up and running with Tmux Orchestrator in 5 minutes!

## Prerequisites Check

```bash
# Verify requirements
make check-deps  # Checks all dependencies automatically
```

## 1️⃣ One-Command Setup & Launch

```bash
# Complete setup and launch API Builder
make quick-start

# That's it! This command:
# ✅ Checks dependencies
# ✅ Creates directories
# ✅ Fixes paths
# ✅ Launches the intelligent API Builder
```

## Alternative Manual Setup

```bash
# Step-by-step setup
make setup       # Initialize everything
make api-launch  # Launch API Builder
make api-attach  # Attach to session
```

## 2️⃣ Basic Agent Setup (2 minutes)

```bash
# Start your first agent
tmux new-session -s my-agent
claude
# Type: "You are a development agent. Your job is to help with coding tasks."
# Detach: Press Ctrl+B, then D
```

## 3️⃣ Orchestrator Setup (3 minutes)

```bash
# Step 1: Start orchestrator session
tmux new-session -s orchestrator

# Step 2: Start Claude (in tmux)
claude

# Step 3: Brief the orchestrator (paste this message):
```
You are the Orchestrator. Your role:
- Monitor and coordinate multiple Claude agents
- Deploy project managers and developers as needed
- Schedule check-ins every 30 minutes using: ./schedule_with_note.sh 30 "Orchestrator check" "orchestrator:0"
- Use ./send-claude-message.sh to communicate with agents

Start by checking existing tmux sessions with: tmux list-sessions
```

# Step 4: Detach and let it run
# Press Ctrl+B, then D

## 📝 Essential Commands (Now with Make!)

### Communicate with Agents
```bash
# Send message using make
make message TARGET=orchestrator:0 MSG="Status update please"

# Or use the script directly
./send-claude-message.sh orchestrator:0 "Status update please"
```

### Monitor Agents
```bash
# Monitor all API Builder agents
make api-monitor

# Check specific agent
make agent-logs AGENT=1

# List all sessions
make tmux-list

# Check workspace status
make workspace-status
```

### Schedule Check-ins
```bash
# Schedule using make
make schedule MINUTES=30 NOTE="Check progress" TARGET=orchestrator:0

# Or use the script directly
./schedule_with_note.sh 30 "Check progress" "orchestrator:0"
```

## 🎯 Common Tasks

### Create a New Project Agent
```bash
PROJECT="my-project"
tmux new-session -d -s $PROJECT
tmux send-keys -t $PROJECT:0 "claude" Enter
sleep 5
./send-claude-message.sh $PROJECT:0 "You manage the $PROJECT codebase. Check for issues and start working."
```

### Deploy a Project Manager
```bash
# In orchestrator session, tell Claude:
./send-claude-message.sh orchestrator:0 "Create a project manager for the frontend project in a new tmux session called 'frontend-pm'"
```

### Check All Agent Status
```bash
python3 tmux_utils.py | jq '.sessions[].name'
```

## ⚡ Quick Wins

1. **Test messaging**: `./send-claude-message.sh test:0 "Hello"`
2. **Test scheduling**: `./schedule_with_note.sh 1 "Test" "test:0"`
3. **View Python utility**: `python3 -c "from tmux_utils import TmuxOrchestrator; print('Ready!')"`

## 🔧 Troubleshooting

| Problem | Solution |
|---------|----------|
| "command not found" | Run: `chmod +x *.sh` |
| "no such session" | Create it: `tmux new-session -s session-name` |
| Path errors | Scripts now use current directory |
| Can't detach | Press Ctrl+B, then D (not Cmd) |

## 📚 Next Steps

1. Read the full [README.md](README.md) for detailed documentation
2. Check [LEARNINGS.md](LEARNINGS.md) for best practices
3. Review [CLAUDE.md](CLAUDE.md) for agent instructions
4. Join multiple sessions: `tmux attach -t session-name`

## 💡 Pro Tips

- Always use `./send-claude-message.sh` for agent communication
- Schedule regular check-ins with `./schedule_with_note.sh`
- Commit work every 30 minutes (remind agents!)
- Use descriptive session names
- Monitor agent windows for errors

---

**Ready to orchestrate!** 🎭 Your agents can now work autonomously 24/7.