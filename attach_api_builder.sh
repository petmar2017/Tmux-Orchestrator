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
