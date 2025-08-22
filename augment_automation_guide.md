# Making Augment Support Claude Code Agent Automation

## Overview
Your `.augment/agents` directory contains 22 specialized research agents designed for Claude Code automation. These agents use YAML frontmatter configuration and can be adapted to work with Augment's system.

## Current Agent Structure Analysis

### Agent Format
Each agent follows this structure:
```markdown
---
name: agent-name
description: When to use this agent with examples
color: purple
tools: WebSearch, WebFetch, Read, Write, MultiEdit
---

[Detailed system prompt and instructions]
```

### Available Research Agents
Your collection includes:

**Research Planning (4 agents):**
- `research-ideator` - Generate innovative research ideas
- `gap-analyzer` - Identify research gaps  
- `hypothesis-generator` - Formulate testable hypotheses
- `proposal-writer` - Craft research proposals

**Literature Review (4 agents):**
- `paper-finder` - Search academic literature
- `citation-analyzer` - Analyze citation patterns
- `literature-synthesizer` - Synthesize findings
- `reference-manager` - Organize citations

**Experimental Design (3 agents):**
- `methodology-designer` - Design research methodologies
- `experiment-planner` - Create experimental procedures
- `statistical-consultant` - Statistical guidance

**Research Development (1 agent):**
- `research-coder` - Develop research software

**Data Analysis (4 agents):**
- `statistical-analyst` - Advanced statistical analysis
- `data-visualizer` - Create publication-quality figures
- `ml-researcher` - Apply ML to research problems
- `results-interpreter` - Interpret complex results

**Paper Writing (4 agents):**
- `academic-writer` - Craft academic manuscripts
- `figure-creator` - Design scientific figures
- `citation-formatter` - Format citations
- `research-documenter` - Create research documentation

**Research Operations (3 agents):**
- `research-project-manager` - Manage research projects
- `ethics-advisor` - Research ethics guidance
- `collaboration-coordinator` - Facilitate collaboration

## Making Augment Support This Automation

### Option 1: Direct Integration (Recommended)

#### Step 1: Create Augment Agent Loader
Create a system that reads and interprets the Claude Code agent format:

```python
# augment_agent_loader.py
import os
import yaml
import re
from pathlib import Path

class AugmentAgentLoader:
    def __init__(self, agents_dir=".augment/agents"):
        self.agents_dir = Path(agents_dir)
        self.agents = {}
        self.load_agents()
    
    def load_agents(self):
        """Load all agents from the agents directory"""
        for agent_file in self.agents_dir.rglob("*.md"):
            agent = self.parse_agent_file(agent_file)
            if agent:
                self.agents[agent['name']] = agent
    
    def parse_agent_file(self, file_path):
        """Parse a Claude Code agent file"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Split frontmatter and content
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                frontmatter = yaml.safe_load(parts[1])
                system_prompt = parts[2].strip()
                
                return {
                    'name': frontmatter.get('name'),
                    'description': frontmatter.get('description'),
                    'color': frontmatter.get('color'),
                    'tools': frontmatter.get('tools', []),
                    'system_prompt': system_prompt,
                    'file_path': file_path
                }
        return None
    
    def get_agent(self, name):
        """Get a specific agent by name"""
        return self.agents.get(name)
    
    def list_agents(self):
        """List all available agents"""
        return list(self.agents.keys())
    
    def find_relevant_agent(self, user_query):
        """Find the most relevant agent for a user query"""
        # Simple keyword matching - can be enhanced with embeddings
        query_lower = user_query.lower()
        
        for name, agent in self.agents.items():
            description = agent['description'].lower()
            if any(keyword in description for keyword in query_lower.split()):
                return agent
        
        return None
```

#### Step 2: Create Augment Agent Executor
```python
# augment_agent_executor.py
from augment_agent_loader import AugmentAgentLoader

class AugmentAgentExecutor:
    def __init__(self):
        self.loader = AugmentAgentLoader()
        self.active_agent = None
    
    def execute_agent(self, agent_name, user_query, context=None):
        """Execute a specific agent with user query"""
        agent = self.loader.get_agent(agent_name)
        if not agent:
            return f"Agent '{agent_name}' not found"
        
        # Set active agent
        self.active_agent = agent
        
        # Construct prompt with agent's system prompt
        full_prompt = f"""
{agent['system_prompt']}

User Query: {user_query}

Context: {context or 'No additional context provided'}

Please respond according to your role as {agent['name']}.
"""
        
        return self.send_to_augment(full_prompt, agent)
    
    def auto_select_agent(self, user_query):
        """Automatically select and execute the most relevant agent"""
        agent = self.loader.find_relevant_agent(user_query)
        if agent:
            return self.execute_agent(agent['name'], user_query)
        else:
            return "No suitable agent found for this query"
    
    def send_to_augment(self, prompt, agent):
        """Send the constructed prompt to Augment"""
        # This would integrate with Augment's API/system
        # For now, return the constructed prompt
        return {
            'agent': agent['name'],
            'prompt': prompt,
            'tools': agent['tools']
        }
```

#### Step 3: Integration with Your Research Workflow
```python
# research_workflow_integration.py
from augment_agent_executor import AugmentAgentExecutor

class ResearchWorkflowManager:
    def __init__(self):
        self.executor = AugmentAgentExecutor()
    
    def handle_research_query(self, query):
        """Main entry point for research queries"""
        
        # Determine if this is a specific agent request
        if "use the" in query.lower() and "agent" in query.lower():
            agent_name = self.extract_agent_name(query)
            if agent_name:
                return self.executor.execute_agent(agent_name, query)
        
        # Auto-select based on query content
        return self.executor.auto_select_agent(query)
    
    def extract_agent_name(self, query):
        """Extract agent name from user query"""
        import re
        pattern = r"use the (\w+(?:-\w+)*) agent"
        match = re.search(pattern, query.lower())
        return match.group(1) if match else None
    
    def chain_agents(self, workflow_steps):
        """Execute multiple agents in sequence"""
        results = []
        context = ""
        
        for step in workflow_steps:
            result = self.executor.execute_agent(
                step['agent'], 
                step['query'], 
                context
            )
            results.append(result)
            context += f"\nPrevious step result: {result}"
        
        return results

# Example usage
workflow = ResearchWorkflowManager()

# Single agent execution
result = workflow.handle_research_query(
    "Use the research-ideator agent to generate ideas for sparse time series forecasting"
)

# Multi-agent workflow
workflow_steps = [
    {'agent': 'research-ideator', 'query': 'Generate research ideas for AI in healthcare'},
    {'agent': 'gap-analyzer', 'query': 'Analyze gaps in the generated ideas'},
    {'agent': 'hypothesis-generator', 'query': 'Create testable hypotheses from the gaps'}
]
results = workflow.chain_agents(workflow_steps)
```

### Option 2: Augment Plugin/Extension

Create an Augment plugin that recognizes and executes Claude Code agents:

```python
# augment_claude_code_plugin.py
class AugmentClaudeCodePlugin:
    def __init__(self):
        self.name = "Claude Code Agents"
        self.version = "1.0.0"
        self.agents_loader = AugmentAgentLoader()
    
    def register_commands(self):
        """Register plugin commands with Augment"""
        return {
            '/agents': self.list_agents_command,
            '/use-agent': self.use_agent_command,
            '/agent-help': self.agent_help_command
        }
    
    def list_agents_command(self, args):
        """List all available agents"""
        agents = self.agents_loader.list_agents()
        return f"Available agents: {', '.join(agents)}"
    
    def use_agent_command(self, args):
        """Use a specific agent"""
        if len(args) < 2:
            return "Usage: /use-agent <agent-name> <query>"
        
        agent_name = args[0]
        query = ' '.join(args[1:])
        
        executor = AugmentAgentExecutor()
        return executor.execute_agent(agent_name, query)
    
    def agent_help_command(self, args):
        """Get help for a specific agent"""
        if not args:
            return "Usage: /agent-help <agent-name>"
        
        agent = self.agents_loader.get_agent(args[0])
        if agent:
            return f"Agent: {agent['name']}\nDescription: {agent['description']}"
        else:
            return f"Agent '{args[0]}' not found"
```

### Option 3: Configuration-Based Approach

Create an Augment configuration file that maps your research workflow:

```yaml
# .augment/config.yml
agents:
  research_workflow:
    enabled: true
    agent_directory: ".augment/agents"
    auto_selection: true
    
  triggers:
    - pattern: "research ideas"
      agent: "research-ideator"
    - pattern: "literature review"
      agent: "literature-synthesizer"
    - pattern: "statistical analysis"
      agent: "statistical-analyst"
    - pattern: "write paper"
      agent: "academic-writer"
  
  workflows:
    complete_research:
      steps:
        - agent: "research-ideator"
          trigger: "generate ideas"
        - agent: "gap-analyzer"
          trigger: "analyze gaps"
        - agent: "methodology-designer"
          trigger: "design methodology"
        - agent: "statistical-analyst"
          trigger: "analyze data"
        - agent: "academic-writer"
          trigger: "write paper"
```

## Implementation Steps

### Phase 1: Basic Integration (Week 1)
1. **Create agent loader** - Parse existing agent files
2. **Build executor** - Execute agents with proper context
3. **Test with key agents** - Start with research-ideator, statistical-analyst

### Phase 2: Enhanced Features (Week 2)
1. **Auto-selection** - Intelligent agent selection based on query
2. **Context preservation** - Maintain context between agent calls
3. **Tool integration** - Map Claude Code tools to Augment equivalents

### Phase 3: Advanced Workflows (Week 3)
1. **Agent chaining** - Multi-agent workflows
2. **State management** - Track workflow progress
3. **Result aggregation** - Combine outputs from multiple agents

### Phase 4: User Interface (Week 4)
1. **Command interface** - `/agents`, `/use-agent` commands
2. **Visual feedback** - Show which agent is active
3. **Progress tracking** - Display workflow progress

## Benefits of This Approach

### For Your Research
- **Specialized expertise** - Each agent optimized for specific tasks
- **Consistent quality** - Standardized approaches across research phases
- **Workflow automation** - Chain agents for complete research pipelines
- **Context preservation** - Maintain research context across sessions

### For Augment Integration
- **Backward compatibility** - Works with existing Claude Code agents
- **Extensibility** - Easy to add new agents or modify existing ones
- **Flexibility** - Support both manual and automatic agent selection
- **Scalability** - Can handle complex multi-agent workflows

## Next Steps

1. **Choose integration approach** - I recommend Option 1 (Direct Integration)
2. **Start with core agents** - Focus on research-ideator, statistical-analyst, academic-writer
3. **Test with your sparse forecasting research** - Use the agents for your current project
4. **Iterate and improve** - Refine based on actual usage patterns

Would you like me to help you implement any of these approaches or create specific integration code for your research workflow?
