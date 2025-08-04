#!/bin/bash

# API Builder Setup Script - Based on AI Dev Team Migration
# Sets up tmux environment for all API builder agents

set -e

echo "🚀 Starting API Builder Orchestrator Setup"
echo "=================================================="

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Configuration
ORCHESTRATOR_SESSION="api_builder"
WORKSPACE_DIR="$PWD/api_builder/workspace"
SCRIPTS_DIR="$PWD"
PROMPTS_DIR="$PWD/api_builder/prompts"

# Check prerequisites
echo -e "${YELLOW}Checking prerequisites...${NC}"

if ! command -v tmux &> /dev/null; then
    echo -e "${RED}❌ tmux is not installed. Please install tmux first.${NC}"
    echo "Run: brew install tmux"
    exit 1
fi

if ! command -v claude &> /dev/null; then
    echo -e "${RED}❌ Claude CLI is not installed. Please install Claude CLI first.${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Prerequisites checked${NC}"

# Kill existing session if it exists
tmux kill-session -t $ORCHESTRATOR_SESSION 2>/dev/null || true

# Create the orchestrator session
echo -e "${YELLOW}Creating tmux API builder session...${NC}"
tmux new-session -d -s $ORCHESTRATOR_SESSION -n "orchestrator" -c "$SCRIPTS_DIR"

# Create windows for each agent
echo -e "${YELLOW}Creating agent windows...${NC}"

# Array of agents with their configurations
declare -a agents=(
    "lead:Lead Developer:$WORKSPACE_DIR"
    "fastapi:FastAPI Developer:$WORKSPACE_DIR/api"
    "mcp:MCP Server Dev:$WORKSPACE_DIR/mcp_server"
    "make:Make Builder:$WORKSPACE_DIR"
    "docs:Documentation:$WORKSPACE_DIR/docs"
    "tester:E2E Tester:$WORKSPACE_DIR/tests"
    "jupyter:Jupyter Dev:$WORKSPACE_DIR/notebooks"
)

# Create window for each agent
window_num=1
for agent_config in "${agents[@]}"; do
    IFS=':' read -r window_name agent_name work_dir <<< "$agent_config"
    
    echo "  Creating window for $agent_name..."
    
    # Create window with correct directory
    tmux new-window -t $ORCHESTRATOR_SESSION:$window_num -n "$window_name" -c "$WORKSPACE_DIR"
    
    # Create agent-specific subdirectory if needed
    if [ "$work_dir" != "$WORKSPACE_DIR" ]; then
        tmux send-keys -t $ORCHESTRATOR_SESSION:$window_num "mkdir -p $work_dir" Enter
        tmux send-keys -t $ORCHESTRATOR_SESSION:$window_num "cd $work_dir" Enter
    fi
    
    # Add initialization message
    tmux send-keys -t $ORCHESTRATOR_SESSION:$window_num "clear" Enter
    tmux send-keys -t $ORCHESTRATOR_SESSION:$window_num "echo '═══════════════════════════════════════════════════════'" Enter
    tmux send-keys -t $ORCHESTRATOR_SESSION:$window_num "echo '🤖 $agent_name Agent'" Enter
    tmux send-keys -t $ORCHESTRATOR_SESSION:$window_num "echo 'Session: $ORCHESTRATOR_SESSION:$window_num'" Enter
    tmux send-keys -t $ORCHESTRATOR_SESSION:$window_num "echo 'Working Directory: $work_dir'" Enter
    tmux send-keys -t $ORCHESTRATOR_SESSION:$window_num "echo '═══════════════════════════════════════════════════════'" Enter
    tmux send-keys -t $ORCHESTRATOR_SESSION:$window_num "echo ''" Enter
    tmux send-keys -t $ORCHESTRATOR_SESSION:$window_num "echo 'Ready for Claude initialization...'" Enter
    tmux send-keys -t $ORCHESTRATOR_SESSION:$window_num "echo 'Run: claude'" Enter
    tmux send-keys -t $ORCHESTRATOR_SESSION:$window_num "echo 'Then paste the agent prompt from: $PROMPTS_DIR/prompt_${window_name}.md'" Enter
    
    ((window_num++))
done

# Set up orchestrator in window 0
echo -e "${YELLOW}Setting up orchestrator window...${NC}"
tmux send-keys -t $ORCHESTRATOR_SESSION:0 "clear" Enter
tmux send-keys -t $ORCHESTRATOR_SESSION:0 "echo '═══════════════════════════════════════════════════════'" Enter
tmux send-keys -t $ORCHESTRATOR_SESSION:0 "echo '🎯 API Builder Orchestrator'" Enter
tmux send-keys -t $ORCHESTRATOR_SESSION:0 "echo 'Session: $ORCHESTRATOR_SESSION:0'" Enter
tmux send-keys -t $ORCHESTRATOR_SESSION:0 "echo '═══════════════════════════════════════════════════════'" Enter
tmux send-keys -t $ORCHESTRATOR_SESSION:0 "echo ''" Enter
tmux send-keys -t $ORCHESTRATOR_SESSION:0 "echo 'Use this window to monitor all agents'" Enter
tmux send-keys -t $ORCHESTRATOR_SESSION:0 "echo 'Start Claude here to act as the orchestrator'" Enter

echo -e "${GREEN}✅ Tmux API builder session created${NC}"

# Create helper script for quick access
cat > attach_api_builder.sh << 'EOF'
#!/bin/bash
# Quick attach to API builder session

SESSION="api_builder"

if tmux has-session -t $SESSION 2>/dev/null; then
    echo "Attaching to $SESSION..."
    echo ""
    echo "Tmux Commands:"
    echo "  Ctrl+B then D     - Detach from session"
    echo "  Ctrl+B then [0-7] - Switch to window"
    echo "  Ctrl+B then c     - Create new window"
    echo "  Ctrl+B then ,     - Rename current window"
    echo ""
    echo "Windows:"
    echo "  0: Orchestrator"
    echo "  1: Lead Developer"
    echo "  2: FastAPI Developer"
    echo "  3: MCP Server Developer"
    echo "  4: Make Command Builder"
    echo "  5: Documentation Developer"
    echo "  6: E2E Tester"
    echo "  7: Jupyter Developer"
    echo ""
    tmux attach -t $SESSION
else
    echo "Session $SESSION not found. Run setup_api_builder.sh first."
fi
EOF

chmod +x attach_api_builder.sh

# Display status
echo ""
echo -e "${GREEN}═══════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}✅ API Builder Environment Ready!${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════════════${NC}"
echo ""
echo "Next steps:"
echo "1. Attach to the API builder session:"
echo -e "   ${YELLOW}./attach_api_builder.sh${NC}"
echo ""
echo "2. Navigate to each window (Ctrl+B then 0-7)"
echo ""
echo "3. Start Claude in each window by typing: claude"
echo ""
echo "4. Paste the appropriate agent prompt from:"
echo "   ${PROMPTS_DIR}/prompt_[agent_name].md"
echo ""
echo "5. Agents will begin working on API development tasks"
echo ""
echo -e "${YELLOW}Window Layout:${NC}"
echo "  Window 0: Orchestrator (monitoring)"
echo "  Window 1: Lead Developer"
echo "  Window 2: FastAPI Developer"
echo "  Window 3: MCP Server Developer"
echo "  Window 4: Make Command Builder"
echo "  Window 5: Documentation Developer"
echo "  Window 6: E2E Tester"
echo "  Window 7: Jupyter Developer"
echo ""
echo -e "${YELLOW}Communication:${NC}"
echo "  Use: ./send-claude-message.sh api_builder:[window] \"message\""
echo "  Schedule: ./schedule_with_note.sh [minutes] \"note\" api_builder:[window]"