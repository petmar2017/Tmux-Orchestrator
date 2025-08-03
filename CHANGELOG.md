# Changelog

All notable changes to the Tmux Orchestrator project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- QUICKSTART.md for rapid onboarding (5-minute setup)
- CHANGELOG.md for tracking project changes
- Registry directory structure for logs, notes, and session tracking
- Improved path handling for multiple user environments

### Changed
- Updated hardcoded paths from /Users/jasonedward to dynamic paths
- Modified schedule_with_note.sh to use project directory instead of hardcoded path
- Simplified scheduling command in schedule_with_note.sh (removed claude_control.py reference)
- Enhanced CLAUDE.md with clearer architecture overview and essential commands

### Fixed
- Path compatibility issues for different user environments
- Schedule script now correctly references local next_check_note.txt
- Directory creation for registry structure

### Security
- Removed hardcoded user paths that could expose system information

## [1.0.0] - 2025-08-02

### Added
- Initial release of Tmux Orchestrator
- Core orchestration system with hierarchical agent management
- send-claude-message.sh for reliable agent communication
- schedule_with_note.sh for autonomous agent scheduling
- tmux_utils.py Python utility for tmux interaction
- Comprehensive documentation (README.md, CLAUDE.md, LEARNINGS.md)
- Visual examples demonstrating orchestrator capabilities
- Git safety protocols with 30-minute commit requirements
- Hub-and-spoke communication model for agent coordination

### Features
- Multi-agent coordination across tmux sessions
- Self-scheduling capabilities for autonomous operation
- Project Manager and Developer agent roles
- Quality assurance protocols and verification checklists
- Cross-project intelligence sharing
- Window naming conventions for better organization
- Agent lifecycle management with proper logging

### Documentation
- Complete setup instructions for single and multi-project scenarios
- Troubleshooting guide for common issues
- Best practices and lessons learned
- Architecture diagrams and visual examples

## [0.9.0] - 2025-06-18

### Added
- Project Manager responsibilities and enforcement patterns
- Web research recommendations for stuck agents
- Claude plan mode discovery (Shift+Tab+Tab activation)
- Cross-window monitoring capabilities
- Documentation enforcement protocols

### Changed
- Improved PM intervention strategies
- Enhanced error message reading practices
- Better communication patterns with numbered questions

### Lessons Learned
- Importance of web research after 10 minutes of failed attempts
- Reading exact error messages before implementing solutions
- Timely positive feedback improves agent motivation
- Structured communication reduces ambiguity

## [0.8.0] - 2025-06-17

### Added
- Multi-agent coordination patterns
- Agent lifecycle management system
- Quality assurance principles for Project Managers
- Hub-and-spoke communication model
- Temporary vs permanent agent distinction

### Architecture
- Three-tier hierarchy (Orchestrator → Project Managers → Developers)
- Structured communication templates
- Agent logging directory structure

## Migration Guide

### From 1.0.0 to Current

1. **Update Paths**: Run the following to update paths:
   ```bash
   sed -i '' 's|/Users/jasonedward|/Users/petermager|g' *.sh
   ```

2. **Create Directories**: Ensure registry structure exists:
   ```bash
   mkdir -p registry/{logs,notes,sessions}
   ```

3. **Test Components**: Verify functionality:
   ```bash
   ./schedule_with_note.sh 1 "Migration test" "test:0"
   python3 tmux_utils.py
   ```

---

For detailed usage instructions, see [QUICKSTART.md](QUICKSTART.md) or [README.md](README.md).