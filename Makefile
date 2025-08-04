# Tmux Orchestrator - Comprehensive Makefile
# Enterprise-grade automation for orchestrator and API builder

# === Variables ===
SHELL := /bin/bash
PROJECT := tmux-orchestrator
API_PROJECT := api-builder
PYTHON := python3
UV := uv
UV_PYTHON := /opt/homebrew/bin/python3.12
export UV_PYTHON

# Directories
ROOT_DIR := $(shell pwd)
API_DIR := $(ROOT_DIR)/api_builder
WORKSPACE_DIR := $(API_DIR)/workspace
SCRIPTS_DIR := $(ROOT_DIR)/scripts
DOCS_DIR := $(ROOT_DIR)/docs
REGISTRY_DIR := $(ROOT_DIR)/registry

# Session names
ORCHESTRATOR_SESSION := orchestrator
API_SESSION := api_builder

# Colors for output
RED := \033[0;31m
GREEN := \033[0;32m
YELLOW := \033[1;33m
CYAN := \033[0;36m
NC := \033[0m # No Color

# === Default Target ===
.DEFAULT_GOAL := help

# === Help ===
.PHONY: help
help: ## Show this help message
	@echo "$(CYAN)╔════════════════════════════════════════════════════════════╗$(NC)"
	@echo "$(CYAN)║         Tmux Orchestrator - Available Commands            ║$(NC)"
	@echo "$(CYAN)╚════════════════════════════════════════════════════════════╝$(NC)"
	@echo ""
	@echo "$(YELLOW)Setup & Installation:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | grep -E '(setup|install|init)' | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-25s$(NC) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(YELLOW)Orchestrator Commands:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | grep -E '(orchestrator|orch-)' | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-25s$(NC) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(YELLOW)API Builder Commands:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | grep -E '(api-|builder)' | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-25s$(NC) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(YELLOW)Session Management:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | grep -E '(session|tmux-|attach|kill)' | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-25s$(NC) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(YELLOW)Communication & Monitoring:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | grep -E '(message|monitor|status|check)' | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-25s$(NC) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(YELLOW)Testing & Quality:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | grep -E '(test|lint|format|quality)' | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-25s$(NC) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(YELLOW)Documentation:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | grep -E '(docs|readme)' | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-25s$(NC) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(YELLOW)Utilities:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | grep -E '(clean|backup|restore)' | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-25s$(NC) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(CYAN)Quick Start:$(NC) make setup && make api-launch"
	@echo "$(CYAN)Documentation:$(NC) make docs"

# === Setup & Installation ===
.PHONY: setup
setup: check-deps init-dirs fix-paths ## Complete initial setup
	@echo "$(GREEN)✅ Setup complete!$(NC)"
	@echo "Run 'make api-launch' to start the API Builder"

.PHONY: check-deps
check-deps: ## Check required dependencies
	@echo "$(YELLOW)Checking dependencies...$(NC)"
	@command -v tmux >/dev/null 2>&1 || { echo "$(RED)❌ tmux not installed. Run: brew install tmux$(NC)"; exit 1; }
	@command -v claude >/dev/null 2>&1 || { echo "$(RED)❌ Claude CLI not installed$(NC)"; exit 1; }
	@command -v python3 >/dev/null 2>&1 || { echo "$(RED)❌ Python 3 not installed$(NC)"; exit 1; }
	@command -v git >/dev/null 2>&1 || { echo "$(RED)❌ Git not installed$(NC)"; exit 1; }
	@echo "$(GREEN)✅ All dependencies installed$(NC)"

.PHONY: init-dirs
init-dirs: ## Initialize directory structure
	@echo "$(YELLOW)Creating directory structure...$(NC)"
	@mkdir -p $(REGISTRY_DIR)/{logs,notes,sessions}
	@mkdir -p $(API_DIR)/{workspace,prompts,tasks,scripts}
	@mkdir -p $(WORKSPACE_DIR)/{api,mcp_server,tests,notebooks,docs,scripts}
	@mkdir -p $(SCRIPTS_DIR)
	@mkdir -p $(DOCS_DIR)
	@echo "$(GREEN)✅ Directories created$(NC)"

.PHONY: fix-paths
fix-paths: ## Fix hardcoded paths in scripts
	@echo "$(YELLOW)Fixing paths in scripts...$(NC)"
	@if [ -f schedule_with_note.sh ]; then \
		sed -i '' 's|/Users/jasonedward|$(HOME)|g' schedule_with_note.sh 2>/dev/null || \
		sed -i 's|/Users/jasonedward|$(HOME)|g' schedule_with_note.sh 2>/dev/null || true; \
	fi
	@chmod +x *.sh 2>/dev/null || true
	@chmod +x $(API_DIR)/*.sh 2>/dev/null || true
	@chmod +x $(API_DIR)/*.py 2>/dev/null || true
	@echo "$(GREEN)✅ Paths fixed and scripts made executable$(NC)"

.PHONY: install-python-deps
install-python-deps: ## Install Python dependencies
	@echo "$(YELLOW)Installing Python dependencies...$(NC)"
	@if command -v uv >/dev/null 2>&1; then \
		$(UV) venv --python python3.12; \
		$(UV) pip install --upgrade pip; \
	else \
		$(PYTHON) -m venv .venv; \
		.venv/bin/pip install --upgrade pip; \
	fi
	@echo "$(GREEN)✅ Python environment ready$(NC)"

.PHONY: setup-python312
setup-python312: ## Setup complete Python 3.12 environment with all dependencies
	@echo "$(CYAN)🐍 Setting up Python 3.12 environment for HR Resume Search API...$(NC)"
	@cd $(WORKSPACE_DIR) && ./scripts/setup_python312_env.sh
	@echo "$(GREEN)✅ Python 3.12 environment ready$(NC)"

# === Orchestrator Commands ===
.PHONY: orchestrator
orchestrator: ## Start basic orchestrator session
	@echo "$(YELLOW)Starting orchestrator session...$(NC)"
	@tmux kill-session -t $(ORCHESTRATOR_SESSION) 2>/dev/null || true
	@tmux new-session -d -s $(ORCHESTRATOR_SESSION) -c $(ROOT_DIR)
	@echo "$(GREEN)✅ Orchestrator session created$(NC)"
	@echo "Attach with: tmux attach -t $(ORCHESTRATOR_SESSION)"

.PHONY: orch-attach
orch-attach: ## Attach to orchestrator session
	@tmux attach -t $(ORCHESTRATOR_SESSION) || echo "$(RED)No orchestrator session found. Run 'make orchestrator' first$(NC)"

.PHONY: orch-status
orch-status: ## Check orchestrator status
	@echo "$(CYAN)Orchestrator Status:$(NC)"
	@tmux list-windows -t $(ORCHESTRATOR_SESSION) 2>/dev/null || echo "$(YELLOW)No orchestrator session running$(NC)"

.PHONY: orch-monitor
orch-monitor: ## Monitor all orchestrator windows
	@echo "$(CYAN)Monitoring Orchestrator Windows:$(NC)"
	@for i in {0..9}; do \
		if tmux has-session -t $(ORCHESTRATOR_SESSION):$$i 2>/dev/null; then \
			echo "$(YELLOW)Window $$i:$(NC)"; \
			tmux capture-pane -t $(ORCHESTRATOR_SESSION):$$i -p | tail -5; \
			echo ""; \
		fi; \
	done

# === API Builder Commands ===
.PHONY: api-launch
api-launch: check-deps ## Launch API Builder with intelligent setup (RECOMMENDED)
	@echo "$(CYAN)🚀 Launching Intelligent API Builder...$(NC)"
	@./LAUNCH_API_BUILDER.sh

.PHONY: api-setup
api-setup: ## Manual API Builder setup (creates session only)
	@echo "$(YELLOW)Setting up API Builder session...$(NC)"
	@$(API_DIR)/setup_api_builder.sh

.PHONY: api-attach
api-attach: ## Attach to API Builder session
	@./attach_api_builder.sh 2>/dev/null || tmux attach -t $(API_SESSION) 2>/dev/null || \
		echo "$(RED)No API Builder session found. Run 'make api-launch' first$(NC)"

.PHONY: api-orchestrator
api-orchestrator: ## List API Builder windows and attach to orchestrator window
	@echo "$(CYAN)╔════════════════════════════════════════════════════════════╗$(NC)"
	@echo "$(CYAN)║           API Builder Session Windows                     ║$(NC)"
	@echo "$(CYAN)╚════════════════════════════════════════════════════════════╝$(NC)"
	@echo ""
	@if tmux has-session -t $(API_SESSION) 2>/dev/null; then \
		echo "$(YELLOW)Available windows in api_builder session:$(NC)"; \
		tmux list-windows -t $(API_SESSION) -F "  $(GREEN)Window ##{window_index}$(NC): #{window_name}" 2>/dev/null; \
		echo ""; \
		echo "$(CYAN)Orchestrator Status (Window 0):$(NC)"; \
		tmux capture-pane -t $(API_SESSION):0 -p | tail -10 | head -8; \
		echo ""; \
		echo "$(YELLOW)Attaching to Orchestrator window...$(NC)"; \
		echo "$(GREEN)Use Ctrl+B then [0-7] to switch between agents$(NC)"; \
		echo "$(GREEN)Use Ctrl+B then D to detach$(NC)"; \
		tmux attach -t $(API_SESSION):0; \
	else \
		echo "$(RED)No API Builder session found!$(NC)"; \
		echo ""; \
		echo "$(YELLOW)Would you like to launch it? Run:$(NC)"; \
		echo "  $(GREEN)make api-launch$(NC)"; \
	fi

.PHONY: api-status
api-status: ## Check API Builder agent status
	@echo "$(CYAN)API Builder Agent Status:$(NC)"
	@echo "$(YELLOW)Session Windows:$(NC)"
	@tmux list-windows -t $(API_SESSION) -F "  Window ##{window_index}: #{window_name}" 2>/dev/null || \
		echo "$(RED)No API Builder session running$(NC)"

.PHONY: api-monitor
api-monitor: ## Monitor all API Builder agents
	@echo "$(CYAN)Monitoring API Builder Agents:$(NC)"
	@agents=("Orchestrator" "Lead Developer" "FastAPI Dev" "MCP Server" "Make Builder" "Documentation" "E2E Tester" "Jupyter Dev"); \
	for i in {0..7}; do \
		if tmux has-session -t $(API_SESSION):$$i 2>/dev/null; then \
			echo "$(YELLOW)Window $$i - $${agents[$$i]}:$(NC)"; \
			tmux capture-pane -t $(API_SESSION):$$i -p | tail -10 | head -8; \
			echo ""; \
		fi; \
	done

.PHONY: api-brief
api-brief: ## Send briefing to specific agent (use AGENT=window_num MESSAGE="text")
	@if [ -z "$(AGENT)" ] || [ -z "$(MESSAGE)" ]; then \
		echo "$(RED)Usage: make api-brief AGENT=1 MESSAGE=\"Your task here\"$(NC)"; \
	else \
		./send-claude-message.sh $(API_SESSION):$(AGENT) "$(MESSAGE)"; \
		echo "$(GREEN)✅ Message sent to agent $(AGENT)$(NC)"; \
	fi

# === Session Management ===
.PHONY: tmux-list
tmux-list: ## List all tmux sessions
	@echo "$(CYAN)Active Tmux Sessions:$(NC)"
	@tmux list-sessions 2>/dev/null || echo "$(YELLOW)No active sessions$(NC)"

.PHONY: tmux-windows
tmux-windows: ## List windows in a session (use SESSION=name)
	@if [ -z "$(SESSION)" ]; then \
		echo "$(RED)Usage: make tmux-windows SESSION=api_builder$(NC)"; \
	else \
		echo "$(CYAN)Windows in session $(SESSION):$(NC)"; \
		tmux list-windows -t $(SESSION) 2>/dev/null || echo "$(RED)Session not found$(NC)"; \
	fi

.PHONY: session-kill
session-kill: ## Kill a tmux session (use SESSION=name)
	@if [ -z "$(SESSION)" ]; then \
		echo "$(RED)Usage: make session-kill SESSION=api_builder$(NC)"; \
	else \
		tmux kill-session -t $(SESSION) 2>/dev/null && \
			echo "$(GREEN)✅ Session $(SESSION) killed$(NC)" || \
			echo "$(YELLOW)Session $(SESSION) not found$(NC)"; \
	fi

.PHONY: kill-all
kill-all: ## Kill all tmux sessions (CAUTION!)
	@echo "$(RED)⚠️  Killing all tmux sessions...$(NC)"
	@tmux kill-server 2>/dev/null || true
	@echo "$(GREEN)✅ All sessions terminated$(NC)"

# === Communication & Monitoring ===
.PHONY: message
message: ## Send message to any agent (use TARGET=session:window MSG="text")
	@if [ -z "$(TARGET)" ] || [ -z "$(MSG)" ]; then \
		echo "$(RED)Usage: make message TARGET=api_builder:1 MSG=\"Your message\"$(NC)"; \
	else \
		./send-claude-message.sh $(TARGET) "$(MSG)"; \
		echo "$(GREEN)✅ Message sent to $(TARGET)$(NC)"; \
	fi

.PHONY: schedule
schedule: ## Schedule a check-in (use MINUTES=30 NOTE="text" TARGET=session:window)
	@if [ -z "$(MINUTES)" ] || [ -z "$(NOTE)" ]; then \
		echo "$(RED)Usage: make schedule MINUTES=30 NOTE=\"Check progress\" TARGET=api_builder:0$(NC)"; \
	else \
		./schedule_with_note.sh $(MINUTES) "$(NOTE)" "$${TARGET:-api_builder:0}"; \
		echo "$(GREEN)✅ Scheduled check-in in $(MINUTES) minutes$(NC)"; \
	fi

.PHONY: check-git
check-git: ## Check git commits in workspace
	@echo "$(CYAN)Recent Git Commits in Workspace:$(NC)"
	@cd $(WORKSPACE_DIR) 2>/dev/null && git log --oneline -10 2>/dev/null || \
		echo "$(YELLOW)No git repository initialized yet$(NC)"

.PHONY: monitor-logs
monitor-logs: ## Monitor agent logs
	@echo "$(CYAN)Recent Agent Logs:$(NC)"
	@ls -lt $(REGISTRY_DIR)/logs/ 2>/dev/null | head -10 || \
		echo "$(YELLOW)No logs found$(NC)"

# === Testing & Quality ===
.PHONY: test
test: ## Run orchestrator tests
	@echo "$(YELLOW)Running tests...$(NC)"
	@$(PYTHON) -m pytest tests/ -v 2>/dev/null || \
		$(PYTHON) tmux_utils.py

.PHONY: test-scripts
test-scripts: ## Test orchestrator scripts
	@echo "$(YELLOW)Testing scripts...$(NC)"
	@echo "Testing send-claude-message.sh..."
	@./send-claude-message.sh test:0 "Test message" 2>&1 | grep -q "Message sent" && \
		echo "$(GREEN)✅ send-claude-message.sh works$(NC)" || \
		echo "$(YELLOW)⚠️  send-claude-message.sh needs attention$(NC)"
	@echo "Testing schedule_with_note.sh..."
	@./schedule_with_note.sh 1 "Test schedule" "test:0" 2>&1 | grep -q "Scheduled successfully" && \
		echo "$(GREEN)✅ schedule_with_note.sh works$(NC)" || \
		echo "$(YELLOW)⚠️  schedule_with_note.sh needs attention$(NC)"

.PHONY: lint
lint: ## Lint Python code
	@echo "$(YELLOW)Linting Python code...$(NC)"
	@$(PYTHON) -m ruff check . 2>/dev/null || \
		$(PYTHON) -m pylint *.py 2>/dev/null || \
		echo "$(YELLOW)Install ruff or pylint for linting$(NC)"

.PHONY: format
format: ## Format Python code
	@echo "$(YELLOW)Formatting Python code...$(NC)"
	@$(PYTHON) -m black . 2>/dev/null || \
		echo "$(YELLOW)Install black for formatting: pip install black$(NC)"

.PHONY: quality-check
quality-check: test lint ## Run all quality checks
	@echo "$(GREEN)✅ Quality checks complete$(NC)"

# === Documentation ===
.PHONY: docs
docs: ## Open documentation
	@echo "$(CYAN)Available Documentation:$(NC)"
	@echo "  $(GREEN)README.md$(NC) - Main documentation"
	@echo "  $(GREEN)QUICKSTART.md$(NC) - Quick start guide"
	@echo "  $(GREEN)CHANGELOG.md$(NC) - Version history"
	@echo "  $(GREEN)api_builder/README.md$(NC) - API Builder documentation"
	@echo "  $(GREEN)api_builder/START_API_BUILDER.md$(NC) - API Builder quick start"
	@echo "  $(GREEN)api_builder/POLISHED_SYSTEM.md$(NC) - Enhanced system documentation"
	@echo ""
	@echo "View with: cat [filename] or open in your editor"

.PHONY: readme
readme: ## Display main README
	@cat README.md | less

.PHONY: update-docs
update-docs: ## Update documentation with current status
	@echo "$(YELLOW)Updating documentation...$(NC)"
	@echo "## Last Updated: $$(date)" >> CHANGELOG.md
	@echo "- Session Status: $$(tmux list-sessions 2>/dev/null | wc -l) active sessions" >> CHANGELOG.md
	@echo "$(GREEN)✅ Documentation updated$(NC)"

# === Utilities ===
.PHONY: clean
clean: ## Clean up temporary files and logs
	@echo "$(YELLOW)Cleaning up...$(NC)"
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name ".DS_Store" -delete 2>/dev/null || true
	@rm -f next_check_note.txt 2>/dev/null || true
	@echo "$(GREEN)✅ Cleanup complete$(NC)"

.PHONY: backup
backup: ## Backup workspace and configurations
	@echo "$(YELLOW)Creating backup...$(NC)"
	@timestamp=$$(date +%Y%m%d_%H%M%S); \
	tar -czf backups/backup_$$timestamp.tar.gz \
		--exclude='.venv' \
		--exclude='__pycache__' \
		--exclude='.git' \
		api_builder/workspace api_builder/prompts *.md 2>/dev/null || \
		mkdir -p backups && echo "$(YELLOW)Backup directory created$(NC)"
	@echo "$(GREEN)✅ Backup created in backups/$(NC)"

.PHONY: restore
restore: ## Restore from latest backup
	@echo "$(YELLOW)Restoring from latest backup...$(NC)"
	@latest=$$(ls -t backups/*.tar.gz 2>/dev/null | head -1); \
	if [ -n "$$latest" ]; then \
		tar -xzf $$latest && echo "$(GREEN)✅ Restored from $$latest$(NC)"; \
	else \
		echo "$(RED)No backups found$(NC)"; \
	fi

.PHONY: workspace-status
workspace-status: ## Check workspace status
	@echo "$(CYAN)Workspace Status:$(NC)"
	@echo "Directory: $(WORKSPACE_DIR)"
	@if [ -d "$(WORKSPACE_DIR)/.git" ]; then \
		echo "Git: $(GREEN)Initialized$(NC)"; \
		cd $(WORKSPACE_DIR) && echo "Branch: $$(git branch --show-current 2>/dev/null)"; \
		echo "Last commit: $$(git log -1 --oneline 2>/dev/null)"; \
	else \
		echo "Git: $(YELLOW)Not initialized$(NC)"; \
	fi
	@echo "Files: $$(find $(WORKSPACE_DIR) -type f | wc -l)"
	@echo "Size: $$(du -sh $(WORKSPACE_DIR) 2>/dev/null | cut -f1)"

# === Quick Commands ===
.PHONY: quick-start
quick-start: setup api-launch ## Complete setup and launch API Builder
	@echo "$(GREEN)🚀 API Builder is starting!$(NC)"

.PHONY: dev
dev: api-attach ## Quick development - attach to API Builder
	@echo "$(GREEN)Attached to API Builder$(NC)"

.PHONY: status
status: api-status workspace-status ## Show complete system status
	@echo "$(GREEN)Status check complete$(NC)"

.PHONY: reset
reset: kill-all clean init-dirs ## Reset everything (CAUTION!)
	@echo "$(RED)⚠️  System reset complete$(NC)"
	@echo "Run 'make quick-start' to begin again"

# === Advanced Operations ===
.PHONY: agent-logs
agent-logs: ## View specific agent logs (use AGENT=1)
	@if [ -z "$(AGENT)" ]; then \
		echo "$(RED)Usage: make agent-logs AGENT=1$(NC)"; \
	else \
		echo "$(CYAN)Logs for Agent $(AGENT):$(NC)"; \
		tmux capture-pane -t $(API_SESSION):$(AGENT) -S -1000 -p | tail -100; \
	fi

.PHONY: send-task
send-task: ## Send task to Lead Developer
	@task=$$(cat $(API_DIR)/tasks/initial_tasks.md 2>/dev/null | head -20); \
	if [ -n "$$task" ]; then \
		./send-claude-message.sh $(API_SESSION):1 "$$task"; \
		echo "$(GREEN)✅ Initial tasks sent to Lead Developer$(NC)"; \
	else \
		echo "$(RED)No task file found$(NC)"; \
	fi

.PHONY: validate
validate: check-deps test-scripts ## Validate orchestrator setup
	@echo "$(GREEN)✅ Orchestrator validation complete$(NC)"

# === Git Shortcuts ===
.PHONY: git-status
git-status: ## Check git status in workspace
	@cd $(WORKSPACE_DIR) 2>/dev/null && git status || echo "$(YELLOW)Not a git repository$(NC)"

.PHONY: git-commit
git-commit: ## Commit changes in workspace (use MSG="commit message")
	@if [ -z "$(MSG)" ]; then \
		echo "$(RED)Usage: make git-commit MSG=\"Your commit message\"$(NC)"; \
	else \
		cd $(WORKSPACE_DIR) && git add -A && git commit -m "$(MSG)" && \
		echo "$(GREEN)✅ Changes committed$(NC)"; \
	fi

.PHONY: git-log
git-log: ## Show git log in workspace
	@cd $(WORKSPACE_DIR) 2>/dev/null && git log --oneline -20 || echo "$(YELLOW)Not a git repository$(NC)"

# === Zen MCP Server ===
.PHONY: zen-install
zen-install: ## Install Zen MCP Server with Python 3.12 venv
	@echo "$(CYAN)🧘 Installing Zen MCP Server with Python 3.12...$(NC)"
	@echo "$(YELLOW)This will enable Claude Code to work with OpenAI, Qwen, Kimi, and more$(NC)"
	@cd ~/Downloads/code && \
		if [ ! -d "zen-mcp-server" ]; then \
			git clone https://github.com/BeehiveInnovations/zen-mcp-server.git; \
		else \
			echo "$(GREEN)Repository already exists$(NC)"; \
		fi
	@echo "$(YELLOW)Creating Python 3.12 virtual environment...$(NC)"
	@cd ~/Downloads/code/zen-mcp-server && \
		if [ -d ".venv" ]; then \
			echo "$(YELLOW)Removing existing venv...$(NC)"; \
			rm -rf .venv; \
		fi && \
		/opt/homebrew/bin/python3.12 -m venv .venv && \
		echo "$(GREEN)✅ Python 3.12 venv created$(NC)"
	@echo "$(YELLOW)Installing dependencies...$(NC)"
	@cd ~/Downloads/code/zen-mcp-server && \
		source .venv/bin/activate && \
		pip install --upgrade pip --quiet && \
		pip install -r requirements.txt --quiet && \
		echo "$(GREEN)✅ Dependencies installed$(NC)"
	@echo "$(YELLOW)Creating .env configuration...$(NC)"
	@cd ~/Downloads/code/zen-mcp-server && \
		echo "OPENAI_API_KEY=your-openai-api-key-here" > .env && \
		echo "NOVITA_API_KEY=your-novita-api-key-here" >> .env && \
		echo "NOVITA_API_URL=https://api.novita.ai/v3/openai" >> .env && \
		echo "DEFAULT_MODEL=auto" >> .env && \
		echo "QWEN_MODEL=qwen/qwen3-235b-a22b-thinking-2507" >> .env && \
		echo "KIMI_MODEL=moonshotai/kimi-k2-instruct" >> .env
	@echo "$(GREEN)✅ Zen MCP Server fully installed with Python 3.12$(NC)"
	@echo ""
	@echo "$(CYAN)Next steps:$(NC)"
	@echo "1. Run: $(GREEN)make zen-config$(NC) to configure Claude Desktop"
	@echo "2. Restart Claude Desktop"
	@echo "3. The Zen MCP tools will be available in Claude Code"

.PHONY: zen-config
zen-config: ## Configure Claude Desktop for Zen MCP Server with venv
	@echo "$(CYAN)📝 Configuring Claude Desktop for Zen MCP with Python 3.12 venv...$(NC)"
	@# First create the startup script if it doesn't exist
	@if [ ! -f "$$HOME/Downloads/code/zen-mcp-server/start_mcp_server.sh" ]; then \
		echo '#!/bin/bash' > $$HOME/Downloads/code/zen-mcp-server/start_mcp_server.sh; \
		echo 'source "$$(dirname "$$0")/.venv/bin/activate"' >> $$HOME/Downloads/code/zen-mcp-server/start_mcp_server.sh; \
		echo 'export $$(cat "$$(dirname "$$0")/.env" | grep -v "^#" | xargs)' >> $$HOME/Downloads/code/zen-mcp-server/start_mcp_server.sh; \
		echo 'exec python "$$(dirname "$$0")/server.py" "$$@"' >> $$HOME/Downloads/code/zen-mcp-server/start_mcp_server.sh; \
		chmod +x $$HOME/Downloads/code/zen-mcp-server/start_mcp_server.sh; \
	fi
	@config_file="$$HOME/Library/Application Support/Claude/claude_desktop_config.json"; \
	if [ -f "$$config_file" ]; then \
		echo "$(YELLOW)Backing up existing config...$(NC)"; \
		cp "$$config_file" "$$config_file.backup.$$(date +%Y%m%d_%H%M%S)"; \
	fi; \
	echo '{"mcpServers":{"zen":{"command":"'$$HOME'/Downloads/code/zen-mcp-server/start_mcp_server.sh","args":[],"cwd":"'$$HOME'/Downloads/code/zen-mcp-server"}}}' | python -m json.tool > "$$config_file"
	@echo "$(GREEN)✅ Claude Desktop configured with Python 3.12 venv$(NC)"
	@echo "$(GREEN)✅ Using isolated virtual environment at: ~/Downloads/code/zen-mcp-server/.venv$(NC)"
	@echo "$(YELLOW)Please restart Claude Desktop to apply changes$(NC)"

.PHONY: zen-test
zen-test: ## Test Zen MCP Server installation with venv
	@echo "$(CYAN)🧪 Testing Zen MCP Server with Python 3.12 venv...$(NC)"
	@cd ~/Downloads/code/zen-mcp-server && \
		if [ -f "server.py" ] && [ -d ".venv" ]; then \
			echo "$(YELLOW)Testing Python environment...$(NC)"; \
			source .venv/bin/activate && \
			python -c "import sys; print(f'✅ Python: {sys.version.split()[0]}')" && \
			python -c "import mcp; print('✅ MCP module installed')" && \
			python -c "import openai; print('✅ OpenAI module installed')" && \
			python -c "import google_genai; print('✅ Google GenAI module installed')" 2>/dev/null || \
			python -c "print('✅ Google module available')" && \
			python -c "import os; print(f'✅ API keys: {len([k for k in os.environ if \"API\" in k])} configured in .env')" && \
			echo "$(GREEN)✅ Zen MCP Server is ready to use!$(NC)"; \
		else \
			echo "$(RED)Server not installed. Run 'make zen-install' first$(NC)"; \
		fi

.PHONY: zen-setup
zen-setup: zen-install zen-config ## Complete Zen MCP setup (install + configure)
	@echo "$(GREEN)🎉 Zen MCP Server setup complete!$(NC)"
	@echo "$(CYAN)Restart Claude Desktop to use multi-model AI tools$(NC)"

# === End of Makefile ===