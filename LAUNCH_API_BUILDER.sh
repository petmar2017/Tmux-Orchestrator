#!/bin/bash

# Intelligent API Builder Launcher
# Gathers requirements and auto-launches all agents with Claude

set -e

echo "🚀 Intelligent API Builder Launcher"
echo "===================================="
echo ""

# Check prerequisites
if ! command -v tmux &> /dev/null; then
    echo "❌ tmux is not installed. Please install tmux first."
    echo "   Run: brew install tmux"
    exit 1
fi

if ! command -v claude &> /dev/null; then
    echo "❌ Claude CLI is not installed. Please install Claude CLI first."
    exit 1
fi

if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

echo "✅ Prerequisites checked"
echo ""

# Run the intelligent launcher
cd "$(dirname "$0")"
python3 api_builder/launch_api_builder.py

# Note: The Python script will handle everything including:
# 1. Gathering project requirements interactively
# 2. Creating customized prompts for each agent
# 3. Setting up the tmux session
# 4. Auto-launching Claude in each window
# 5. Sending the customized prompts to each Claude instance