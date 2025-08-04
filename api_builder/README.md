# 🚀 Intelligent API Builder - Tmux Orchestrator

An intelligent, interactive launcher that creates a complete API development team with 8 specialized AI agents, all working autonomously in tmux.

## ✨ Key Features

### 🎯 Intelligent Project Setup
- **Interactive Requirements Gathering**: Asks about your project needs
- **Customized Agent Prompts**: Each agent gets project-specific instructions
- **Auto-Launch**: Starts Claude in all windows with tailored prompts
- **No Manual Configuration**: Everything is automated

### 🤖 What Gets Built
Based on your requirements, the team will build:
- FastAPI backend with your chosen database
- Authentication system (JWT, OAuth2, etc.)
- MCP server for Claude Desktop tools
- Complete test suite with pytest
- API documentation
- Makefile for automation
- Jupyter notebooks for testing

## 🚀 Quick Start (30 seconds!)

### One Command Launch:
```bash
cd /Users/petermager/Downloads/code/Tmux-Orchestrator
./LAUNCH_API_BUILDER.sh
```

That's it! The launcher will:
1. Ask you about your project (name, API type, database, features)
2. Create a tmux session with 8 windows
3. Launch Claude in each window
4. Send customized prompts to each agent
5. Start the autonomous development process

### What You'll Be Asked:
- Project name and description
- API type (REST, GraphQL, WebSocket, Hybrid)
- Database choice (PostgreSQL, MongoDB, SQLite, MySQL)
- Authentication method (JWT, OAuth2, API Keys, etc.)
- Features to include (user management, file uploads, etc.)
- MCP tools for Claude Desktop
- Testing strategy and coverage targets

## 📁 Project Structure

```
api_builder/
├── launch_api_builder.py    # Intelligent launcher script
├── auto_brief_agent.sh      # Auto-briefing utility
├── setup_api_builder.sh     # Manual setup (if needed)
├── workspace/               # Where your API gets built
│   ├── api/                # FastAPI backend
│   ├── mcp_server/         # MCP server for Claude
│   ├── tests/              # Test suites
│   ├── notebooks/          # Jupyter notebooks
│   ├── docs/               # Documentation
│   └── project_config.json # Your project configuration
├── prompts/                # Agent prompt templates
│   ├── prompt_orchestrator.md
│   ├── prompt_lead.md
│   ├── prompt_fastapi.md
│   ├── prompt_mcp.md
│   └── ...
└── tasks/                  # Task definitions
    └── initial_tasks.md
```

## 🎭 The Agent Team

| Window | Agent | Role |
|--------|-------|------|
| 0 | **Orchestrator** | High-level coordination, monitors all agents |
| 1 | **Lead Developer** | Team management, architecture, git workflow |
| 2 | **FastAPI Developer** | Builds REST/GraphQL/WebSocket APIs |
| 3 | **MCP Server Dev** | Creates Claude Desktop tools |
| 4 | **Make Builder** | Build automation and deployment |
| 5 | **Documentation** | README, API docs, guides |
| 6 | **E2E Tester** | pytest, coverage, integration tests |
| 7 | **Jupyter Dev** | Interactive notebooks for API testing |

## 🔧 How It Works

### 1. Interactive Configuration
The launcher asks about your project requirements:
```
Project name: my-awesome-api
API Type: REST
Database: PostgreSQL
Authentication: JWT
Features: User Management, Rate Limiting, Caching
```

### 2. Automatic Agent Briefing
Each agent receives a customized prompt with:
- Their specific role and responsibilities
- Your project requirements
- Immediate tasks to start
- Communication protocols

### 3. Autonomous Development
Agents then:
- Start building immediately
- Coordinate through tmux messages
- Commit code every 30 minutes
- Self-schedule check-ins
- Work 24/7 autonomously

## 📊 Monitoring Your Team

### Attach to the Session
```bash
tmux attach -t api_builder
```

### Navigate Between Agents
- `Ctrl+B` then `0-7` - Switch to specific agent
- `Ctrl+B` then `n` - Next window
- `Ctrl+B` then `p` - Previous window
- `Ctrl+B` then `d` - Detach (agents keep working)

### Check Agent Status
```bash
# From outside tmux
tmux capture-pane -t api_builder:1 -p | tail -30  # Check Lead Developer

# Check all agents
for i in {0..7}; do
    echo "=== Window $i ==="
    tmux capture-pane -t api_builder:$i -p | tail -5
done
```

### Monitor Git Progress
```bash
cd api_builder/workspace
git log --oneline -10  # See recent commits
```

## 🛠️ Advanced Usage

### Manual Agent Briefing
If you need to manually brief an agent:
```bash
./api_builder/auto_brief_agent.sh api_builder:2 prompts/custom_prompt.md "FastAPI Dev"
```

### Send Messages to Agents
```bash
./send-claude-message.sh api_builder:1 "Please prioritize authentication"
```

### Schedule Check-ins
```bash
./schedule_with_note.sh 30 "Review API endpoints" "api_builder:2"
```

### Custom Project Configuration
Edit `workspace/project_config.json` to modify project settings.

## 🚨 Troubleshooting

| Issue | Solution |
|-------|----------|
| Claude not starting | Check Claude CLI is installed: `claude --version` |
| Session already exists | Kill it: `tmux kill-session -t api_builder` |
| Agent not responding | Restart Claude in that window: `Ctrl+C` then type `claude` |
| Can't attach to session | Check it exists: `tmux list-sessions` |

## 🎯 Example Projects

### 1. E-commerce API
```
API Type: REST
Database: PostgreSQL
Auth: JWT
Features: User Management, File Uploads, Email Notifications
MCP Tools: Database Query, Order Management
```

### 2. Real-time Chat API
```
API Type: Hybrid (REST + WebSocket)
Database: MongoDB
Auth: JWT
Features: User Management, Rate Limiting, Caching
MCP Tools: Message Search, User Analytics
```

### 3. Analytics Dashboard API
```
API Type: GraphQL
Database: PostgreSQL
Auth: API Keys
Features: Rate Limiting, Caching, API Documentation
MCP Tools: Data Query, Report Generation
```

## 💡 Tips for Success

1. **Let It Run**: Agents work best when not interrupted
2. **Trust the Process**: Agents self-organize and coordinate
3. **Monitor Git**: Check commits every 30 minutes
4. **Review Window 0**: Orchestrator provides overall status
5. **Be Patient**: Complex features take time to implement properly

## 📈 Expected Timeline

- **Minutes 0-5**: Setup and agent initialization
- **Minutes 5-30**: Basic project structure and git setup
- **Hour 1**: Core API endpoints working
- **Hour 2-3**: Authentication and database models
- **Hour 4-5**: MCP server and Claude tools
- **Hour 6+**: Tests, documentation, and polish

## 🔄 Updating Configuration

To change project settings after launch:
1. Edit `workspace/project_config.json`
2. Tell the Lead Developer about changes:
   ```bash
   ./send-claude-message.sh api_builder:1 "Project config updated. Please review project_config.json"
   ```

## 🎉 Success Metrics

You'll know it's working when you see:
- ✅ Regular git commits (every 30 min)
- ✅ API endpoints responding (check `workspace/api/`)
- ✅ Tests passing (check `workspace/tests/`)
- ✅ Documentation growing (check `workspace/docs/`)
- ✅ Agents reporting status to Lead Developer
- ✅ MCP server tools working

## 🚦 Next Steps

After launching:
1. Let the agents work for 30 minutes
2. Check the orchestrator (Window 0) for overall status
3. Review the code being generated in `workspace/`
4. Test the API endpoints as they're created
5. Watch the magic happen!

---

**Ready to build your API?** Run `./LAUNCH_API_BUILDER.sh` and answer a few questions. Your AI development team will handle the rest! 🚀