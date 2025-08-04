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
        
        # Agent configurations
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
        """Launch Claude in a specific window with a customized prompt"""
        
        print(f"  🚀 Launching {agent_name} (window {window_num})...", end="", flush=True)
        
        # First, ensure we're in the right directory
        subprocess.run(["tmux", "send-keys", "-t", f"{self.session_name}:{window_num}", 
                       f"cd {self.workspace_dir}", "Enter"])
        time.sleep(0.3)  # Reduced wait
        
        # Clear the screen
        subprocess.run(["tmux", "send-keys", "-t", f"{self.session_name}:{window_num}", 
                       "clear", "Enter"])
        time.sleep(0.2)  # Reduced wait
        
        # Start Claude
        subprocess.run(["tmux", "send-keys", "-t", f"{self.session_name}:{window_num}", 
                       "claude", "Enter"])
        time.sleep(2)  # Reduced wait for Claude to start
        
        # Send prompt line by line to avoid tmux interpreting newlines as flags
        lines = prompt_content.split('\n')
        
        # Send each line separately
        for i, line in enumerate(lines):
            # For lines starting with -, we need to use -- to stop flag parsing
            if line.startswith('-'):
                # Use -- to indicate end of flags, everything after is literal
                cmd = ["tmux", "send-keys", "-t", f"{self.session_name}:{window_num}", "--", line]
            else:
                # Regular lines can use -l flag
                cmd = ["tmux", "send-keys", "-t", f"{self.session_name}:{window_num}", "-l", line]
            
            subprocess.run(cmd)
            
            # Send C-m (newline) after each line except the last
            if i < len(lines) - 1:
                cmd_newline = ["tmux", "send-keys", "-t", f"{self.session_name}:{window_num}", "C-m"]
                subprocess.run(cmd_newline)
        
        # Wait for all lines to register in tmux buffer
        time.sleep(0.5)
        
        # CRITICAL: Send final Enter to submit the complete prompt to Claude
        subprocess.run(["tmux", "send-keys", "-t", 
                      f"{self.session_name}:{window_num}", 
                      "Enter"])
        
        print(f" ✅ Ready!")
        
    def launch_all_agents(self):
        """Launch Claude in all windows with customized prompts"""
        print(f"\n{self.YELLOW}🤖 Launching agents with customized prompts...{self.NC}")
        
        # Read the agent standards
        standards_path = self.prompts_dir / "AGENT_STANDARDS.md"
        if standards_path.exists():
            with open(standards_path, 'r') as f:
                agent_standards = f.read()
        else:
            agent_standards = ""
        
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
        
        # Check if user wants to create GitHub repo
        create_repo = self.get_user_input("\nCreate GitHub repository? (y/n)", "y")
        repo_name = ""
        if create_repo.lower() == 'y':
            repo_name = self.get_user_input("Repository name", self.project_config['name'].replace(' ', '-').lower())
            self.project_config['github_repo'] = repo_name
        
        print(f"\n{self.CYAN}Starting agent initialization...{self.NC}")
        print(f"{self.YELLOW}This will take approximately 3-4 minutes for all 9 agents.{self.NC}\n")
        
        agent_count = len(agents)
        for idx, (window_num, prompt_file, agent_name) in enumerate(agents, 1):
            print(f"\n{self.MAGENTA}[Agent {idx}/{agent_count}]{self.NC}")
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
            time.sleep(2)  # Small delay between launches
            
        print(f"\n{self.GREEN}✅ All agents launched successfully!{self.NC}")
        
    def display_final_instructions(self):
        """Display instructions for the user"""
        print(f"\n{self.CYAN}{'='*70}")
        print(f"🎉 API Builder Team is Ready!")
        print(f"{'='*70}{self.NC}\n")
        
        print(f"{self.GREEN}All 9 agents have been launched with customized prompts based on:{self.NC}")
        print(f"  • Project: {self.project_config['name']}")
        print(f"  • API Type: {self.project_config['api_type']}")
        print(f"  • Database: {self.project_config['database']}")
        print(f"  • Features: {', '.join(self.project_config['features'])}")
        
        print(f"\n{self.YELLOW}To monitor your team:{self.NC}")
        print(f"  1. Attach to session: {self.CYAN}tmux attach -t {self.session_name}{self.NC}")
        print(f"  2. Switch windows: {self.CYAN}Ctrl+B then [0-8]{self.NC}")
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
        print("  8: DevOps Engineer (deployment & infrastructure)")
        
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