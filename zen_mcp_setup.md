# Zen MCP Server Installation Guide for Claude Code

## Overview
Zen MCP Server enables Claude Code to work with multiple AI models (OpenAI, Gemini, Qwen, Kimi, etc.) as a unified team.

## Prerequisites
- Python 3.12 (recommended) or 3.10+
- Git
- Claude Desktop application
- API keys (you have provided these)

## Step 1: Clone the Repository
```bash
cd ~/Downloads/code/
git clone https://github.com/BeehiveInnovations/zen-mcp-server.git
cd zen-mcp-server
```

## Step 2: Create Environment Configuration
Create a `.env` file in the zen-mcp-server directory:

```bash
cat > .env << 'EOF'
# OpenAI Configuration
OPENAI_API_KEY=your-openai-api-key-here

# Novita.ai Configuration for Qwen3 and Kimi
NOVITA_API_KEY=your-novita-api-key-here
NOVITA_API_URL=https://api.novita.ai/v3/openai

# Model Configuration
DEFAULT_MODEL=auto
QWEN_MODEL=qwen/qwen3-235b-a22b-thinking-2507
KIMI_MODEL=moonshotai/kimi-k2-instruct

# Optional: Set specific model as default
# DEFAULT_MODEL=openai/gpt-4o
EOF
```

## Step 3: Configure Claude Desktop

### Option A: Direct Configuration
Edit your Claude Desktop configuration file:

**macOS:**
```bash
nano ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

**Windows (WSL):**
```bash
nano "$APPDATA/Claude/claude_desktop_config.json"
```

**Linux:**
```bash
nano ~/.config/Claude/claude_desktop_config.json
```

Add this configuration:
```json
{
  "mcpServers": {
    "zen": {
      "command": "python",
      "args": [
        "-m",
        "zen_mcp_server"
      ],
      "cwd": "/Users/petermager/Downloads/code/zen-mcp-server",
      "env": {
        "PYTHONPATH": "/Users/petermager/Downloads/code/zen-mcp-server",
        "OPENAI_API_KEY": "your-openai-api-key-here",
        "NOVITA_API_KEY": "your-novita-api-key-here",
        "NOVITA_API_URL": "https://api.novita.ai/v3/openai",
        "DEFAULT_MODEL": "auto"
      }
    }
  }
}
```

### Option B: Using UVX (Recommended)
```json
{
  "mcpServers": {
    "zen": {
      "command": "sh",
      "args": [
        "-c",
        "exec $(which uvx || echo uvx) --from git+https://github.com/BeehiveInnovations/zen-mcp-server.git zen-mcp-server"
      ],
      "env": {
        "PATH": "/usr/local/bin:/usr/bin:/bin:/opt/homebrew/bin:~/.local/bin",
        "OPENAI_API_KEY": "your-openai-api-key-here",
        "NOVITA_API_KEY": "your-novita-api-key-here"
      }
    }
  }
}
```

## Step 4: Install Dependencies
```bash
cd ~/Downloads/code/zen-mcp-server

# Option 1: Using UV (recommended)
uv venv --python python3.12
source .venv/bin/activate
uv pip install -r requirements.txt

# Option 2: Using regular pip
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Step 5: Test the Server
```bash
# Run the server directly to test
./run-server.sh

# Or manually:
python -m zen_mcp_server
```

## Step 6: Restart Claude Desktop
1. Quit Claude Desktop completely
2. Restart Claude Desktop
3. The Zen MCP server should now be available

## Available Tools in Claude Code
Once installed, you'll have access to these tools:
- `chat` - Multi-model AI collaboration
- `thinkdeep` - Advanced reasoning across models
- `codereview` - Multi-model code review
- `debug` - AI-powered debugging
- `explain` - Concept explanation
- `generate` - Content generation
- And many more...

## Using Custom Models via Novita.ai

### For Qwen3:
```python
# In your .env or config
CUSTOM_MODEL_URL=https://api.novita.ai/v3/openai
CUSTOM_MODEL_API_KEY=sk_riPQdrbT7CEOuVjXRGbBQXiQpE2pQkqw5o8y7dsUYGU
CUSTOM_MODEL_NAME=qwen/qwen3-235b-a22b-thinking-2507
```

### For Kimi:
```python
# In your .env or config
CUSTOM_MODEL_URL=https://api.novita.ai/v3/openai
CUSTOM_MODEL_API_KEY=sk_riPQdrbT7CEOuVjXRGbBQXiQpE2pQkqw5o8y7dsUYGU
CUSTOM_MODEL_NAME=moonshotai/kimi-k2-instruct
```

## Troubleshooting

### If the server doesn't appear in Claude:
1. Check the configuration file path is correct
2. Ensure JSON syntax is valid (no trailing commas)
3. Verify Python path: `which python3.12`
4. Check logs: `tail -f ~/.claude/logs/mcp.log` (if available)

### If models don't respond:
1. Verify API keys are correct
2. Check API rate limits
3. Test API keys directly:
```bash
# Test OpenAI
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer YOUR_API_KEY"

# Test Novita.ai
curl https://api.novita.ai/v3/openai/models \
  -H "Authorization: Bearer YOUR_API_KEY"
```

## Security Note
⚠️ **IMPORTANT**: The API keys in this file should be stored securely:
1. Never commit API keys to version control
2. Use environment variables or secure vaults in production
3. Rotate keys regularly
4. Monitor usage for unauthorized access

## Next Steps
1. Complete the installation
2. Restart Claude Desktop
3. Test the integration with a simple command
4. Explore the multi-model capabilities

## Support
- GitHub Issues: https://github.com/BeehiveInnovations/zen-mcp-server/issues
- Documentation: Check the `docs/` folder in the repository