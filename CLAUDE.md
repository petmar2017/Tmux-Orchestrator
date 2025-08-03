# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Core Architecture

The Tmux Orchestrator is a multi-agent coordination system that enables Claude instances to work autonomously across tmux sessions. The architecture uses a hierarchical model where an Orchestrator manages Project Managers, who in turn coordinate Developers, QA Engineers, and other specialized agents.

### Key Components

- **Orchestrator**: High-level oversight, architectural decisions, cross-project coordination
- **Project Managers**: Quality enforcement, task assignment, team coordination  
- **Specialized Agents**: Developers, QA, DevOps, Code Reviewers - focused implementation
- **Communication Layer**: `send-claude-message.sh` for reliable agent messaging
- **Scheduling System**: `schedule_with_note.sh` for autonomous check-ins

## Essential Commands

### Starting Projects
```bash
# Create new tmux session for a project
PROJECT_NAME="project-name"
PROJECT_PATH="/Users/petermager/Coding/$PROJECT_NAME"
tmux new-session -d -s $PROJECT_NAME -c "$PROJECT_PATH"
tmux rename-window -t $PROJECT_NAME:0 "Claude-Agent"
tmux new-window -t $PROJECT_NAME -n "Shell" -c "$PROJECT_PATH"
tmux new-window -t $PROJECT_NAME -n "Dev-Server" -c "$PROJECT_PATH"

# Start Claude agent
tmux send-keys -t $PROJECT_NAME:0 "claude" Enter
sleep 5

# Brief the agent using the messaging script
./send-claude-message.sh $PROJECT_NAME:0 "Your briefing message here"
```

### Agent Communication
```bash
# Always use the messaging script - handles timing automatically
./send-claude-message.sh session:window "Your message"

# Examples:
./send-claude-message.sh frontend:0 "What's your status?"
./send-claude-message.sh backend:1 "Please review the API endpoints"
```

### Self-Scheduling
```bash
# Schedule check-ins with specific notes
./schedule_with_note.sh 30 "Review auth implementation" "current-window:0"

# Get current window for self-scheduling
CURRENT_WINDOW=$(tmux display-message -p "#{session_name}:#{window_index}")
./schedule_with_note.sh 15 "PM oversight check" "$CURRENT_WINDOW"
```

### Monitoring
```bash
# Check window content
tmux capture-pane -t session:window -p | tail -50

# List all windows in session
tmux list-windows -t session -F "#{window_index}: #{window_name}"

# Check current location
tmux display-message -p "#{session_name}:#{window_index}"
```

## Critical Protocols

### Git Safety (MANDATORY)
- **Commit every 30 minutes**: `git add -A && git commit -m "Progress: [description]"`
- **Feature branches**: Always work in feature branches, never directly on main
- **Meaningful commits**: Describe what was done, not generic "updates"
- **Tag stable versions**: `git tag stable-[feature]-$(date +%Y%m%d-%H%M%S)`

### Window Management
- **Always specify directory**: `tmux new-window -t session -n "name" -c "/path"`
- **Verify before commands**: Check pwd and environment before running commands
- **Capture output**: Always verify command success with `tmux capture-pane`

### Agent Lifecycle
1. **Creation**: Start Claude, brief with specific responsibilities
2. **Communication**: Use hub-and-spoke model through PMs
3. **Monitoring**: Regular status checks and progress verification
4. **Termination**: Capture logs, document handoff, close properly

## Project-Specific Patterns

### Python Utilities
- `tmux_utils.py`: Core tmux interaction library with TmuxOrchestrator class
  - Safety checks on all operations
  - Window content capture and monitoring
  - Session/window discovery methods

### Shell Scripts
- `send-claude-message.sh`: Handles critical 0.5s timing for Claude messages
- `schedule_with_note.sh`: Creates detached scheduling processes with notes
  - Accepts target window as third parameter
  - Creates note file at `/Users/jasonedward/Coding/Tmux orchestrator/next_check_note.txt`

## Common Issues & Solutions

### Scheduling Failures
- Always verify current window: `tmux display-message -p "#{session_name}:#{window_index}"`
- Test scheduling with explicit target: `./schedule_with_note.sh 1 "test" "session:window"`

### Communication Failures  
- Never use manual `tmux send-keys` for messages - always use `send-claude-message.sh`
- Wait 5+ seconds after sending message before checking response

### Directory Issues
- New windows inherit tmux startup directory, not current window's directory
- Always use `-c` flag when creating windows
- Verify with `pwd` before running commands

## Quality Standards

### Project Manager Enforcement
- No code without tests
- Comprehensive error handling required
- Documentation must be updated with code
- Performance must be acceptable
- Security best practices mandatory

### Communication Discipline
- Structured templates for all messages
- No chat - work-related only
- Escalate blockers within 10 minutes
- One topic per message

## Testing & Development

### Running Tests
The project currently doesn't have automated tests. When implementing:
- Use pytest for Python components
- Add tests for tmux interaction utilities
- Test scheduling and messaging scripts

### Development Workflow
1. Check project type: `test -f package.json || test -f requirements.txt`
2. Activate environments: `source venv/bin/activate` for Python
3. Start dev servers in dedicated windows
4. Monitor logs in separate windows
5. Commit progress every 30 minutes

## Key Learnings

From LEARNINGS.md:
- **Web research after 10 min**: If stuck, immediately suggest web search
- **Read exact errors**: Don't assume - check actual error messages
- **Cross-window monitoring**: Check server/log windows for context
- **Claude plan mode**: Activate with `tmux send-keys -t session:window S-Tab S-Tab`
- **Documentation enforcement**: PMs must ensure learnings are documented

## Directory Structure
```
~/Coding/Tmux orchestrator/
├── send-claude-message.sh      # Agent communication
├── schedule_with_note.sh        # Self-scheduling
├── tmux_utils.py               # Tmux interaction utilities
├── next_check_note.txt         # Scheduling notes
├── registry/
│   ├── logs/                   # Agent conversation logs
│   ├── sessions.json           # Active session tracking
│   └── notes/                  # Orchestrator summaries
└── LEARNINGS.md                # Accumulated knowledge
```