#!/usr/bin/env python3
"""
Intelligent API Builder Launcher
Gathers project requirements and auto-launches all agents with customized prompts
"""

import os
import sys
import json
import time
import subprocess
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path

class APIBuilderLauncher:
    """Intelligent launcher for API Builder with automated agent initialization"""
    
    def __init__(self):
        self.session_name = "api_builder"
        self.base_dir = Path(__file__).parent
        self.workspace_dir = self.base_dir / "workspace"
        self.prompts_dir = self.base_dir / "prompts"
        self.project_config = {}
        
        # Colors for terminal output
        self.GREEN = '\033[0;32m'
        self.YELLOW = '\033[1;33m'
        self.CYAN = '\033[0;36m'
        self.RED = '\033[0;31m'
        self.MAGENTA = '\033[0;35m'
        self.NC = '\033[0m'  # No Color
        
    def print_header(self):
        """Print welcome header"""
        print(f"\n{self.CYAN}{'='*70}")
        print(f"{self.CYAN}🚀 Intelligent API Builder Launcher")
        print(f"{self.CYAN}{'='*70}{self.NC}\n")
        print(f"{self.GREEN}I'll help you set up your API project with specialized AI agents.")
        print(f"{self.GREEN}First, let me gather some information about your project.\n{self.NC}")
        
    def get_user_input(self, prompt: str, default: str = "") -> str:
        """Get user input with colored prompt"""
        if default:
            print(f"{self.CYAN}{prompt} [{default}]: {self.NC}", end="")
        else:
            print(f"{self.CYAN}{prompt}: {self.NC}", end="")
        
        user_input = input().strip()
        return user_input if user_input else default
        
    def gather_project_requirements(self):
        """Interactively gather project requirements from user"""
        print(f"{self.YELLOW}📋 Project Configuration{self.NC}")
        print("-" * 50)
        
        # Basic information
        self.project_config['name'] = self.get_user_input("Project name", "my-api")
        self.project_config['description'] = self.get_user_input("Brief description")
        
        # API Type
        print(f"\n{self.YELLOW}API Type:{self.NC}")
        print("1. REST API")
        print("2. GraphQL API")
        print("3. WebSocket API")
        print("4. Hybrid (REST + WebSocket)")
        api_type = self.get_user_input("Choose API type (1-4)", "1")
        api_types = ["REST", "GraphQL", "WebSocket", "Hybrid"]
        self.project_config['api_type'] = api_types[int(api_type)-1 if api_type.isdigit() else 0]
        
        # Database
        print(f"\n{self.YELLOW}Database:{self.NC}")
        print("1. PostgreSQL")
        print("2. MongoDB")
        print("3. SQLite")
        print("4. MySQL")
        print("5. No database")
        db_choice = self.get_user_input("Choose database (1-5)", "1")
        databases = ["PostgreSQL", "MongoDB", "SQLite", "MySQL", "None"]
        self.project_config['database'] = databases[int(db_choice)-1 if db_choice.isdigit() else 0]
        
        # Authentication
        print(f"\n{self.YELLOW}Authentication:{self.NC}")
        print("1. JWT")
        print("2. OAuth2")
        print("3. API Keys")
        print("4. Session-based")
        print("5. No authentication")
        auth_choice = self.get_user_input("Choose authentication (1-5)", "1")
        auth_types = ["JWT", "OAuth2", "API Keys", "Session", "None"]
        self.project_config['authentication'] = auth_types[int(auth_choice)-1 if auth_choice.isdigit() else 0]
        
        # Features
        print(f"\n{self.YELLOW}Features to include:{self.NC}")
        features = []
        if self.get_user_input("Include user management? (y/n)", "y").lower() == 'y':
            features.append("User Management")
        if self.get_user_input("Include file uploads? (y/n)", "n").lower() == 'y':
            features.append("File Uploads")
        if self.get_user_input("Include email notifications? (y/n)", "n").lower() == 'y':
            features.append("Email Notifications")
        if self.get_user_input("Include rate limiting? (y/n)", "y").lower() == 'y':
            features.append("Rate Limiting")
        if self.get_user_input("Include caching? (y/n)", "y").lower() == 'y':
            features.append("Caching")
        if self.get_user_input("Include API documentation? (y/n)", "y").lower() == 'y':
            features.append("API Documentation")
        
        self.project_config['features'] = features
        
        # MCP Tools
        print(f"\n{self.YELLOW}MCP (Model Context Protocol) Tools:{self.NC}")
        print("What Claude Desktop tools should the MCP server provide?")
        mcp_tools = []
        if self.get_user_input("Database query tool? (y/n)", "y").lower() == 'y':
            mcp_tools.append("Database Query")
        if self.get_user_input("API testing tool? (y/n)", "y").lower() == 'y':
            mcp_tools.append("API Testing")
        if self.get_user_input("Code generation tool? (y/n)", "y").lower() == 'y':
            mcp_tools.append("Code Generation")
        custom_tool = self.get_user_input("Any custom tool? (describe or press enter)")
        if custom_tool:
            mcp_tools.append(custom_tool)
        
        self.project_config['mcp_tools'] = mcp_tools
        
        # Testing strategy
        print(f"\n{self.YELLOW}Testing Strategy:{self.NC}")
        self.project_config['test_coverage_target'] = self.get_user_input("Target test coverage (%)", "80")
        self.project_config['test_types'] = []
        if self.get_user_input("Include unit tests? (y/n)", "y").lower() == 'y':
            self.project_config['test_types'].append("unit")
        if self.get_user_input("Include integration tests? (y/n)", "y").lower() == 'y':
            self.project_config['test_types'].append("integration")
        if self.get_user_input("Include E2E tests? (y/n)", "y").lower() == 'y':
            self.project_config['test_types'].append("e2e")
            
        # Summary
        self.display_configuration_summary()
        
    def display_configuration_summary(self):
        """Display the gathered configuration"""
        print(f"\n{self.CYAN}{'='*70}")
        print(f"📊 Project Configuration Summary")
        print(f"{'='*70}{self.NC}\n")
        
        print(f"{self.GREEN}Project:{self.NC} {self.project_config['name']}")
        print(f"{self.GREEN}Description:{self.NC} {self.project_config['description']}")
        print(f"{self.GREEN}API Type:{self.NC} {self.project_config['api_type']}")
        print(f"{self.GREEN}Database:{self.NC} {self.project_config['database']}")
        print(f"{self.GREEN}Authentication:{self.NC} {self.project_config['authentication']}")
        print(f"{self.GREEN}Features:{self.NC} {', '.join(self.project_config['features'])}")
        print(f"{self.GREEN}MCP Tools:{self.NC} {', '.join(self.project_config['mcp_tools'])}")
        print(f"{self.GREEN}Test Coverage:{self.NC} {self.project_config['test_coverage_target']}%")
        print(f"{self.GREEN}Test Types:{self.NC} {', '.join(self.project_config['test_types'])}")
        
        confirm = self.get_user_input("\nProceed with this configuration? (y/n)", "y")
        if confirm.lower() != 'y':
            print(f"{self.YELLOW}Configuration cancelled. Please run again.{self.NC}")
            sys.exit(0)
            
    def generate_customized_prompts(self):
        """Generate customized prompts for each agent based on project config"""
        print(f"\n{self.YELLOW}🔧 Generating customized agent prompts...{self.NC}")
        
        # Create custom prompt context
        context = f"""
Project: {self.project_config['name']}
Description: {self.project_config['description']}
API Type: {self.project_config['api_type']}
Database: {self.project_config['database']}
Authentication: {self.project_config['authentication']}
Features: {', '.join(self.project_config['features'])}
MCP Tools: {', '.join(self.project_config['mcp_tools'])}
Test Coverage Target: {self.project_config['test_coverage_target']}%
"""
        
        # Store context for all agents
        self.project_config['context'] = context
        
        # Save configuration
        config_file = self.workspace_dir / "project_config.json"
        config_file.parent.mkdir(parents=True, exist_ok=True)
        with open(config_file, 'w') as f:
            json.dump(self.project_config, f, indent=2)
        
        print(f"{self.GREEN}✅ Configuration saved to project_config.json{self.NC}")
        
    def kill_existing_session(self):
        """Kill existing tmux session if it exists"""
        subprocess.run(["tmux", "kill-session", "-t", self.session_name], 
                      stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
        
    def create_tmux_session(self):
        """Create the tmux session with all windows"""
        print(f"\n{self.YELLOW}🚀 Creating tmux session...{self.NC}")
        
        # Kill existing session
        self.kill_existing_session()
        
        # Create new session
        subprocess.run(["tmux", "new-session", "-d", "-s", self.session_name, 
                       "-n", "orchestrator", "-c", str(self.workspace_dir)])
        
        # Agent configurations (including DevOps)
        agents = [
            ("lead", "Lead Developer"),
            ("fastapi", "FastAPI Developer"),
            ("mcp", "MCP Server Dev"),
            ("make", "Make Builder"),
            ("docs", "Documentation"),
            ("tester", "E2E Tester"),
            ("jupyter", "Jupyter Dev"),
            ("devops", "DevOps Engineer")
        ]
        
        # Create windows for each agent
        for i, (name, title) in enumerate(agents, 1):
            subprocess.run(["tmux", "new-window", "-t", f"{self.session_name}:{i}", 
                          "-n", name, "-c", str(self.workspace_dir)])
            print(f"  Created window {i}: {title}")
            
        print(f"{self.GREEN}✅ Tmux session created{self.NC}")
        
    def launch_claude_in_window(self, window_num: int, agent_name: str, prompt_content: str):
        """Launch Claude in a specific window with optimized fast prompt sending"""
        
        print(f"  🚀 Starting {agent_name}...", end="", flush=True)
        
        # Step 1: Setup directory and clear screen (combined for speed)
        setup_commands = [
            f"cd {self.workspace_dir}",
            "clear"
        ]
        
        for cmd in setup_commands:
            subprocess.run(["tmux", "send-keys", "-t", f"{self.session_name}:{window_num}", 
                           cmd, "Enter"])
            time.sleep(0.2)  # Reduced wait time
        
        print(f" initializing...", end="", flush=True)
        
        # Step 2: Start Claude
        subprocess.run(["tmux", "send-keys", "-t", f"{self.session_name}:{window_num}", 
                       "claude", "Enter"])
        time.sleep(1.5)  # Reduced Claude startup wait
        
        print(f" briefing...", end="", flush=True)
        
        # Step 3: Send entire prompt at once (MUCH faster than chunking!)
        # This is the key optimization - send the whole prompt in one go
        try:
            # Check if we have the fast message script
            script_dir = Path(__file__).parent.parent
            fast_script_path = script_dir / "send-claude-message-fast.sh"
            regular_script_path = script_dir / "send-claude-message.sh"
            
            # Create fast script if it doesn't exist
            if not fast_script_path.exists():
                self.create_fast_send_script()
            
            # Use the fast script for sending the entire prompt
            if fast_script_path.exists():
                os.chmod(str(fast_script_path), 0o755)
                # Send entire prompt as one message
                result = subprocess.run(["bash", str(fast_script_path), 
                                       f"{self.session_name}:{window_num}", 
                                       prompt_content],
                                       capture_output=True,
                                       text=True,
                                       timeout=5)
                
                if result.returncode != 0:
                    raise Exception(f"Fast send failed: {result.stderr}")
                    
            else:
                # Fallback to chunked sending if fast script not available
                self.send_prompt_chunked(window_num, prompt_content)
                
        except Exception as e:
            print(f" {self.YELLOW}(using fallback){self.NC}", end="", flush=True)
            # Fallback to chunked sending
            self.send_prompt_chunked(window_num, prompt_content)
        
        print(f" {self.GREEN}✅ Ready!{self.NC}")
    
    def send_prompt_chunked(self, window_num: int, prompt_content: str):
        """Fallback chunked sending if fast method fails - optimized to only sleep once at the end"""
        lines = prompt_content.split('\n')
        chunk_size = 100  # Larger chunks since we're not sleeping between them
        
        # Send all chunks WITHOUT Enter (just the text)
        for i in range(0, len(lines), chunk_size):
            chunk = '\n'.join(lines[i:i+chunk_size])
            if chunk.strip():
                # Send just the text, no Enter
                subprocess.run(["tmux", "send-keys", "-t", 
                              f"{self.session_name}:{window_num}", 
                              chunk])
        
        # Single sleep at the end to let all chunks register
        time.sleep(0.5)
        
        # Send ONE Enter at the very end to execute everything
        subprocess.run(["tmux", "send-keys", "-t", 
                       f"{self.session_name}:{window_num}", "Enter"])
    
    def create_fast_send_script(self):
        """Create an optimized send script that doesn't use sleep"""
        fast_script = self.base_dir.parent / "send-claude-message-fast.sh"
        
        script_content = '''#!/bin/bash

# Fast version of send-claude-message.sh
# Removes the 0.5s sleep for faster operation
# Usage: send-claude-message-fast.sh <session:window> <message>

if [ $# -lt 2 ]; then
    echo "Usage: $0 <session:window> <message>"
    echo "Example: $0 api_builder:3 'Hello Claude!'"
    exit 1
fi

WINDOW="$1"
shift  # Remove first argument, rest is the message
MESSAGE="$*"

# Send the message and Enter in rapid succession
tmux send-keys -t "$WINDOW" "$MESSAGE" Enter

echo "Message sent to $WINDOW"
'''
        
        with open(fast_script, 'w') as f:
            f.write(script_content)
        
        os.chmod(str(fast_script), 0o755)
        return fast_script
        
    def launch_all_agents(self):
        """Launch Claude in all windows with customized prompts"""
        print(f"\n{self.YELLOW}🤖 Launching agents with customized prompts...{self.NC}")
        print(f"{self.CYAN}This process takes 3-5 minutes as we start Claude in each window.{self.NC}")
        print(f"{self.CYAN}Each agent needs time to initialize and receive their briefing.{self.NC}\n")
        
        # Read the agent standards
        print(f"📚 Loading agent standards...", end="", flush=True)
        standards_path = self.prompts_dir / "AGENT_STANDARDS.md"
        if standards_path.exists():
            with open(standards_path, 'r') as f:
                agent_standards = f.read()
            print(f" {self.GREEN}✓{self.NC}")
        else:
            agent_standards = ""
            print(f" {self.YELLOW}(not found, using defaults){self.NC}")
        
        # Read base prompts and customize them
        agents = [
            (0, "orchestrator", "Orchestrator"),
            (1, "lead", "Lead Developer"),
            (2, "fastapi", "FastAPI Developer"),
            (3, "mcp", "MCP Server Developer"),
            (4, "make", "Make Command Builder"),
            (5, "docs", "Documentation Developer"),
            (6, "tester", "E2E Tester"),
            (7, "jupyter", "Jupyter Developer"),
            (8, "devops", "DevOps Engineer")
        ]
        
        print(f"\n{self.YELLOW}Starting agent initialization sequence...{self.NC}")
        
        # Check if user wants to create GitHub repo
        print(f"\n{self.CYAN}📦 Repository Setup{self.NC}")
        print("-" * 50)
        create_repo = self.get_user_input("Create GitHub repository? (y/n)", "y")
        repo_name = ""
        if create_repo.lower() == 'y':
            repo_name = self.get_user_input("Repository name", self.project_config['name'].replace(' ', '-').lower())
            self.project_config['github_repo'] = repo_name
            
            print(f"\n{self.YELLOW}Checking repository status...{self.NC}", end="", flush=True)
            
            # Check if repo already exists locally
            repo_path = self.workspace_dir / repo_name
            if repo_path.exists():
                print(f"\n{self.YELLOW}⚠️  Repository '{repo_name}' already exists at {repo_path}{self.NC}")
                use_existing = self.get_user_input("Use existing repository? (y/n)", "y")
                if use_existing.lower() != 'y':
                    print(f"{self.RED}Please choose a different name or remove the existing repository{self.NC}")
                    sys.exit(1)
                self.project_config['use_existing_repo'] = True
                print(f"{self.GREEN}✓ Using existing repository{self.NC}")
            else:
                self.project_config['use_existing_repo'] = False
                print(f" {self.GREEN}✓ Ready to create new repository{self.NC}")
        
        total_agents = len(agents)
        print(f"\n{self.CYAN}═══════════════════════════════════════════════════════════════{self.NC}")
        print(f"{self.CYAN}🤖 Agent Deployment Phase{self.NC}")
        print(f"{self.CYAN}═══════════════════════════════════════════════════════════════{self.NC}")
        print(f"\n{self.YELLOW}Launching {total_agents} specialized AI agents...{self.NC}")
        print(f"{self.YELLOW}Each agent takes 20-30 seconds to initialize and receive briefing.{self.NC}\n")
        
        start_time = time.time()
        
        for idx, (window_num, prompt_file, agent_name) in enumerate(agents, 1):
            print(f"\n{self.MAGENTA}[Agent {idx}/{total_agents}]{self.NC} {agent_name}")
            print(f"{'─' * 60}")
            
            # Read base prompt
            prompt_path = self.prompts_dir / f"prompt_{prompt_file}.md"
            enhanced_prompt_path = self.prompts_dir / f"enhanced_prompt_{prompt_file}.md"
            
            # Use enhanced prompt if available
            if enhanced_prompt_path.exists():
                with open(enhanced_prompt_path, 'r') as f:
                    base_prompt = f.read()
            elif prompt_path.exists():
                with open(prompt_path, 'r') as f:
                    base_prompt = f.read()
            else:
                base_prompt = f"You are the {agent_name} agent."
            
            # Customize prompt with project context and standards
            customized_prompt = f"""
{base_prompt}

## 🎯 MANDATORY AGENT STANDARDS

{agent_standards}

## PROJECT SPECIFIC CONTEXT

{self.project_config['context']}

## YOUR IMMEDIATE TASKS

Based on the project configuration above, your specific focus areas are:
- API Type: Build {self.project_config['api_type']} API
- Database: Use {self.project_config['database']} for data persistence
- Auth: Implement {self.project_config['authentication']} authentication
- Features: {', '.join(self.project_config['features'])}
- Test Coverage Target: {self.project_config['test_coverage_target']}%
- MCP Tools: {', '.join(self.project_config['mcp_tools'])}

## GITHUB REPOSITORY
{'Repository Name: ' + repo_name if repo_name else 'No GitHub repository requested'}

## CRITICAL REMINDERS
1. FIRST: Read AGENT_STANDARDS.md completely
2. Use Python 3.12 ONLY (not 3.13)
3. All configuration in .env file
4. Commit every 30 minutes
5. Update documentation continuously
6. All operations via Makefile
7. No mock functions - use TODOs
8. Test everything (target: {self.project_config['test_coverage_target']}% coverage)

Please acknowledge that you understand your role, the project requirements, and the mandatory standards.
"""
            
            # Launch Claude with customized prompt
            self.launch_claude_in_window(window_num, agent_name, customized_prompt)
            
            # Show progress and time remaining
            remaining = total_agents - idx
            if remaining > 0:
                est_time = remaining * 25  # Estimate 25 seconds per agent
                minutes = est_time // 60
                seconds = est_time % 60
                if minutes > 0:
                    time_str = f"{minutes}m {seconds}s"
                else:
                    time_str = f"{seconds}s"
                print(f"\n  {self.CYAN}⏱️  Estimated time remaining: {time_str} ({remaining} agents left){self.NC}")
            
            time.sleep(1)  # Small delay between launches
        
        # Calculate total time taken
        total_time = int(time.time() - start_time)
        minutes = total_time // 60
        seconds = total_time % 60
        
        print(f"\n{self.CYAN}═══════════════════════════════════════════════════════════════{self.NC}")
        print(f"{self.GREEN}✅ All {total_agents} agents launched successfully!{self.NC}")
        print(f"{self.GREEN}⏱️  Total deployment time: {minutes}m {seconds}s{self.NC}")
        print(f"{self.CYAN}═══════════════════════════════════════════════════════════════{self.NC}")
        print(f"\n{self.GREEN}The team is now working autonomously on your {self.project_config['name']} project.{self.NC}")
        
    def display_final_instructions(self):
        """Display instructions for the user"""
        print(f"\n{self.CYAN}{'='*70}")
        print(f"🎉 API Builder Team is Ready!")
        print(f"{'='*70}{self.NC}\n")
        
        print(f"{self.GREEN}All 8 agents have been launched with customized prompts based on:{self.NC}")
        print(f"  • Project: {self.project_config['name']}")
        print(f"  • API Type: {self.project_config['api_type']}")
        print(f"  • Database: {self.project_config['database']}")
        print(f"  • Features: {', '.join(self.project_config['features'])}")
        
        print(f"\n{self.YELLOW}To monitor your team:{self.NC}")
        print(f"  1. Attach to session: {self.CYAN}tmux attach -t {self.session_name}{self.NC}")
        print(f"  2. Switch windows: {self.CYAN}Ctrl+B then [0-7]{self.NC}")
        print(f"  3. Detach: {self.CYAN}Ctrl+B then D{self.NC}")
        
        print(f"\n{self.YELLOW}Window Layout:{self.NC}")
        print("  0: Orchestrator (coordinating all agents)")
        print("  1: Lead Developer (managing team)")
        print("  2: FastAPI Developer (building API)")
        print("  3: MCP Server Developer (Claude tools)")
        print("  4: Make Command Builder (automation)")
        print("  5: Documentation Developer (docs)")
        print("  6: E2E Tester (testing)")
        print("  7: Jupyter Developer (notebooks)")
        
        print(f"\n{self.MAGENTA}The agents are now working autonomously on your project!{self.NC}")
        print(f"{self.MAGENTA}They will commit code every 30 minutes and coordinate tasks.{self.NC}")
        
    def run(self):
        """Main execution flow"""
        try:
            self.print_header()
            self.gather_project_requirements()
            self.generate_customized_prompts()
            self.create_tmux_session()
            self.launch_all_agents()
            self.display_final_instructions()
            
            # Ask if user wants to attach immediately
            attach = self.get_user_input("\nAttach to session now? (y/n)", "y")
            if attach.lower() == 'y':
                os.system(f"tmux attach -t {self.session_name}")
                
        except KeyboardInterrupt:
            print(f"\n{self.RED}Launcher cancelled by user{self.NC}")
            sys.exit(0)
        except Exception as e:
            print(f"\n{self.RED}Error: {str(e)}{self.NC}")
            sys.exit(1)

if __name__ == "__main__":
    launcher = APIBuilderLauncher()
    launcher.run()