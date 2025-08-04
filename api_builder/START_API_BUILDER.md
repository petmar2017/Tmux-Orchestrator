# 🚀 API Builder - Quick Start Guide

A native Tmux Orchestrator implementation for building complete API systems with 7 specialized AI agents.

## What This Builds

The API Builder orchestrates agents to create:
- **FastAPI Backend** with authentication and CRUD operations
- **MCP Server** for Claude Desktop integration
- **Complete Test Suite** with pytest
- **Documentation** (README, API docs, guides)
- **Build Automation** via Makefile
- **Interactive Notebooks** for API testing

## Prerequisites

```bash
# Check requirements
tmux -V          # Need tmux installed
claude --version # Need Claude CLI
python3 --version # Need Python 3.8+
```

## 🎯 Quick Start (2 minutes)

### Step 1: Run Setup Script

```bash
cd /Users/petermager/Downloads/code/Tmux-Orchestrator
./api_builder/setup_api_builder.sh
```

This creates:
- Tmux session "api_builder" with 8 windows (0-7)
- Workspace directories for each agent
- Helper scripts for attachment

### Step 2: Attach to Session

```bash
./attach_api_builder.sh
```

You'll see:
- Window 0: Orchestrator (you start here)
- Window 1-7: Agent windows (ready for Claude)

### Step 3: Start the Orchestrator

In Window 0, start Claude:
```bash
claude
```

Then paste the orchestrator prompt:
```bash
cat api_builder/prompts/prompt_orchestrator.md
# Copy and paste the content into Claude
```

### Step 4: Let the Orchestrator Initialize Agents

The orchestrator will:
1. Send initialization messages to each agent window
2. Distribute initial tasks
3. Monitor progress
4. Schedule regular check-ins

## 🤖 Agent Roles

| Window | Agent | Responsibility |
|--------|-------|----------------|
| 0 | Orchestrator | High-level coordination |
| 1 | Lead Developer | Team management, git, architecture |
| 2 | FastAPI Dev | REST APIs, database models |
| 3 | MCP Server Dev | Claude tools, MCP protocol |
| 4 | Make Builder | Build automation, Makefile |
| 5 | Documentation | README, guides, API docs |
| 6 | E2E Tester | pytest, test coverage |
| 7 | Jupyter Dev | Interactive notebooks |

## 📝 Manual Agent Setup (If Needed)

If you want to manually start agents:

### For Each Agent Window (1-7):

1. **Switch to window**: `Ctrl+B` then `[number]`

2. **Start Claude**: 
   ```bash
   claude
   ```

3. **Paste agent prompt**:
   ```bash
   # For Lead Developer (Window 1)
   cat api_builder/prompts/prompt_lead.md
   
   # For FastAPI (Window 2)
   cat api_builder/prompts/prompt_fastapi.md
   
   # And so on...
   ```

## 🔧 Communication Between Agents

Agents communicate using:

```bash
# Send message to any agent
./send-claude-message.sh api_builder:[window] "Your message"

# Examples:
./send-claude-message.sh api_builder:1 "Status update please"
./send-claude-message.sh api_builder:2 "Create user authentication endpoints"
```

## 📊 Monitoring Progress

### From Orchestrator (Window 0)
```bash
# Check any agent's output
tmux capture-pane -t api_builder:1 -p | tail -30

# Check all windows
for i in {1..7}; do
  echo "=== Window $i ==="
  tmux capture-pane -t api_builder:$i -p | tail -5
done
```

### Check Git Commits
```bash
cd api_builder/workspace
git log --oneline -10
```

## ⏰ Scheduling

Agents self-schedule check-ins:
```bash
# Schedule a check-in
./schedule_with_note.sh 30 "Review API endpoints" "api_builder:2"
```

## 📁 Project Structure

```
api_builder/
├── workspace/          # Where code is built
│   ├── api/           # FastAPI code
│   ├── mcp_server/    # MCP server
│   ├── tests/         # Test suites
│   ├── notebooks/     # Jupyter notebooks
│   ├── docs/          # Documentation
│   └── scripts/       # Utility scripts
├── prompts/           # Agent prompts
├── tasks/             # Task definitions
└── setup_api_builder.sh
```

## 🎯 Expected Timeline

- **Hour 1**: Project setup, git init, basic structure
- **Hour 2-3**: Core API with auth and database
- **Hour 4-5**: MCP server and tools
- **Hour 6**: Tests and documentation
- **Ongoing**: Agents work autonomously with 30-min commits

## 🚨 Troubleshooting

| Issue | Solution |
|-------|----------|
| Agent not responding | Check window with `tmux capture-pane`, restart Claude if needed |
| Can't send messages | Verify session exists: `tmux list-sessions` |
| Git not initialized | Tell Lead Developer to run `git init` |
| Tasks not distributed | Check orchestrator is running in Window 0 |

## 🎉 Success Indicators

- All agents acknowledging tasks
- Regular git commits (every 30 min)
- API endpoints responding
- Tests passing
- Documentation growing
- Agents communicating status updates

## 💡 Tips

1. **Let agents work autonomously** - Don't micromanage
2. **Monitor git commits** - Ensures progress is saved
3. **Use orchestrator for big decisions** - Agents handle details
4. **Check Window 0 regularly** - Orchestrator provides overview
5. **Trust the process** - Agents will self-organize

## Next Steps

After setup:
1. Watch the orchestrator coordinate the team
2. Monitor git commits appearing every 30 minutes
3. Check the API being built in `workspace/api/`
4. Review documentation in `workspace/docs/`
5. Let the system run - agents work 24/7!

---

**Ready!** Your API Builder team is now operational. The orchestrator will coordinate everything automatically. 🚀