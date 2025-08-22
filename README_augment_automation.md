# Augment Agent Automation System

## Overview
This system enables Augment to use your 22 specialized research agents from `.augment/agents` for automated research workflows. The agents are designed for comprehensive academic research support from ideation to publication.

## Quick Start

### 1. Install Dependencies
```bash
pip install pyyaml
```

### 2. Test the System
```bash
# List all available agents
python augment_agent_integration.py --list-agents

# Use a specific agent
python augment_agent_integration.py --use-agent research-ideator --query "Generate ideas for sparse time series forecasting"

# Auto-select agent based on query
python augment_agent_integration.py --auto-select "I need help with statistical analysis"
```

### 3. Run Your Research Workflow
```bash
# Complete sparse forecasting research workflow
python sparse_forecasting_workflow.py full

# Run specific phase
python sparse_forecasting_workflow.py phase 1

# Quick agent query
python sparse_forecasting_workflow.py quick statistical-analyst "How do I validate theoretical bounds empirically?"
```

## Your Research Agents

### 📋 Research Planning (4 agents)
- **research-ideator** - Generate innovative research ideas and directions
- **gap-analyzer** - Systematically identify research gaps through literature analysis  
- **hypothesis-generator** - Formulate testable hypotheses and theoretical predictions
- **proposal-writer** - Craft compelling research proposals and grant applications

### 📚 Literature Review (4 agents)
- **paper-finder** - Search and discover relevant academic literature
- **citation-analyzer** - Analyze citation patterns and research impact networks
- **literature-synthesizer** - Synthesize findings from multiple papers
- **reference-manager** - Organize and format citations with precision

### 🔬 Experimental Design (3 agents)
- **methodology-designer** - Design robust research methodologies
- **experiment-planner** - Create detailed experimental procedures and protocols
- **statistical-consultant** - Provide statistical guidance and analysis planning

### 💻 Research Development (1 agent)
- **research-coder** - Develop reproducible research software and analysis tools

### 📊 Data Analysis (4 agents)
- **statistical-analyst** - Conduct advanced statistical analyses and modeling
- **data-visualizer** - Create publication-quality figures and visualizations
- **ml-researcher** - Apply machine learning methods to research problems
- **results-interpreter** - Interpret complex results and draw meaningful conclusions

### ✍️ Paper Writing (4 agents)
- **academic-writer** - Craft clear, compelling academic manuscripts
- **figure-creator** - Design scientific figures and publication graphics
- **citation-formatter** - Format citations and ensure bibliographic accuracy
- **research-documenter** - Create comprehensive research documentation

### 🤝 Research Operations (3 agents)
- **research-project-manager** - Manage complex research projects and timelines
- **ethics-advisor** - Provide research ethics guidance and compliance support
- **collaboration-coordinator** - Facilitate research collaboration and team coordination

## How It Works

### Agent Structure
Each agent has:
- **Name**: Unique identifier (e.g., `research-ideator`)
- **Description**: When and how to use the agent
- **Tools**: Available tools (WebSearch, Read, Write, etc.)
- **System Prompt**: Detailed instructions and expertise

### Integration Process
1. **Agent Selection**: System finds relevant agent based on your query
2. **Prompt Generation**: Creates specialized prompt for Augment
3. **Tool Mapping**: Maps Claude Code tools to Augment equivalents
4. **Context Preservation**: Maintains research context across agents

## Usage Examples

### For Your Sparse Forecasting Research

#### Generate Research Ideas
```bash
python augment_agent_integration.py --use-agent research-ideator --query "I want to establish information-theoretic bounds for sparse time series forecasting. What novel theoretical directions should I explore?"
```

#### Literature Review
```bash
python augment_agent_integration.py --use-agent literature-synthesizer --query "Synthesize recent work on information theory in time series analysis and identify gaps for sparse forecasting bounds"
```

#### Statistical Analysis Planning
```bash
python augment_agent_integration.py --use-agent statistical-analyst --query "How should I validate theoretical bounds for sparse forecasting? What statistical tests and metrics should I use?"
```

#### Academic Writing
```bash
python augment_agent_integration.py --use-agent academic-writer --query "Help me structure a TKDE paper on information-theoretic bounds for sparse time series forecasting"
```

### Multi-Agent Workflows

#### Complete Research Pipeline
```bash
# Phase 1: Ideation
python sparse_forecasting_workflow.py phase 1

# Phase 2: Literature Review  
python sparse_forecasting_workflow.py phase 2

# Phase 3: Methodology Design
python sparse_forecasting_workflow.py phase 3

# Phase 4: Implementation Planning
python sparse_forecasting_workflow.py phase 4

# Phase 5: Writing Preparation
python sparse_forecasting_workflow.py phase 5
```

## Integration with Augment

### Method 1: Copy-Paste Prompts
1. Run the agent integration script
2. Copy the generated prompt
3. Paste into Augment
4. Ensure specified tools are available

### Method 2: Direct Integration (Advanced)
Modify Augment to automatically:
1. Detect agent requests in user queries
2. Load and execute appropriate agents
3. Chain multiple agents for complex workflows

## Customization

### Adding New Agents
1. Create new `.md` file in `.augment/agents/`
2. Follow the YAML frontmatter format:
```markdown
---
name: your-agent-name
description: When to use this agent
tools: Read, Write, WebSearch
---

Your detailed system prompt here...
```

### Modifying Existing Agents
1. Edit the agent file in `.augment/agents/`
2. Modify system prompt or tools as needed
3. Reload with `python augment_agent_integration.py --list-agents`

### Creating Custom Workflows
1. Copy `sparse_forecasting_workflow.py`
2. Modify for your specific research domain
3. Add new phases or agent combinations

## Best Practices

### For Research Efficiency
- **Start with ideation agents** for new projects
- **Chain related agents** for comprehensive analysis
- **Use context** to maintain coherence across agents
- **Validate outputs** with domain expertise

### For TKDE Publication
- **Use methodology-designer** for rigorous experimental design
- **Apply statistical-consultant** for proper analysis planning
- **Leverage academic-writer** for manuscript structure
- **Employ figure-creator** for publication-quality visuals

### For Reproducibility
- **Document agent usage** in your research notes
- **Version control** agent configurations
- **Share workflows** with collaborators
- **Maintain research context** across sessions

## Troubleshooting

### Common Issues
1. **Agent not found**: Check spelling and use `--list-agents`
2. **No relevant agents**: Try different keywords or use specific agent names
3. **Tool conflicts**: Ensure Augment has access to specified tools
4. **Context loss**: Provide explicit context in queries

### Getting Help
- Use `--agent-help <agent-name>` for specific agent information
- Check agent descriptions for usage examples
- Review the system prompt for detailed instructions

## Next Steps

1. **Test the system** with your current research
2. **Customize workflows** for your specific needs
3. **Integrate with Augment** using your preferred method
4. **Share and iterate** with your research team

This automation system transforms your research workflow by providing specialized AI assistance at every stage, from initial ideation to final publication. Each agent brings deep expertise to accelerate and enhance your academic research process.
