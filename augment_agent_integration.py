#!/usr/bin/env python3
"""
Augment Agent Integration System
Enables Augment to use Claude Code research agents for automation

Usage:
    python augment_agent_integration.py --list-agents
    python augment_agent_integration.py --use-agent research-ideator "Generate ideas for sparse forecasting"
    python augment_agent_integration.py --auto-select "I need help with statistical analysis"
"""

import os
import sys
import yaml
import argparse
import re
from pathlib import Path
from typing import Dict, List, Optional, Any

class AugmentAgentSystem:
    """Main system for integrating Claude Code agents with Augment"""
    
    def __init__(self, agents_dir: str = "."):
        self.agents_dir = Path(agents_dir)
        self.agents: Dict[str, Dict[str, Any]] = {}
        self.load_agents()
    
    def load_agents(self) -> None:
        """Load all agents from the agents directory"""
        if not self.agents_dir.exists():
            print(f"Warning: Agents directory {self.agents_dir} not found")
            return
        
        for agent_file in self.agents_dir.rglob("*.md"):
            try:
                agent = self._parse_agent_file(agent_file)
                if agent:
                    self.agents[agent['name']] = agent
                    print(f"Loaded agent: {agent['name']}")
            except Exception as e:
                print(f"Error loading agent {agent_file}: {e}")
    
    def _parse_agent_file(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """Parse a Claude Code agent file"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Split frontmatter and content
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                try:
                    # Handle complex YAML with multiline descriptions
                    frontmatter_text = parts[1].strip()

                    # Try to parse YAML, if it fails, parse manually
                    try:
                        frontmatter = yaml.safe_load(frontmatter_text)
                    except yaml.YAMLError:
                        # Manual parsing for complex descriptions
                        frontmatter = self._parse_frontmatter_manually(frontmatter_text)

                    system_prompt = parts[2].strip()

                    # Parse tools if they're comma-separated
                    tools = frontmatter.get('tools', [])
                    if isinstance(tools, str):
                        tools = [tool.strip() for tool in tools.split(',')]

                    return {
                        'name': frontmatter.get('name'),
                        'description': frontmatter.get('description', ''),
                        'color': frontmatter.get('color', 'blue'),
                        'tools': tools,
                        'system_prompt': system_prompt,
                        'file_path': str(file_path),
                        'category': self._get_category_from_path(file_path)
                    }
                except Exception as e:
                    print(f"Error parsing {file_path}: {e}")
        return None

    def _parse_frontmatter_manually(self, frontmatter_text: str) -> Dict[str, Any]:
        """Manually parse frontmatter when YAML fails"""
        result = {}
        lines = frontmatter_text.split('\n')
        current_key = None
        current_value = []

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Check if this is a new key-value pair
            if ':' in line and not line.startswith(' '):
                # Save previous key-value pair
                if current_key:
                    result[current_key] = '\n'.join(current_value).strip()

                # Start new key-value pair
                key, value = line.split(':', 1)
                current_key = key.strip()
                current_value = [value.strip()] if value.strip() else []
            else:
                # This is a continuation of the current value
                if current_key:
                    current_value.append(line)

        # Save the last key-value pair
        if current_key:
            result[current_key] = '\n'.join(current_value).strip()

        return result
    
    def _get_category_from_path(self, file_path: Path) -> str:
        """Extract category from file path"""
        parts = file_path.parts
        for part in parts:
            if part in ['research-planning', 'literature-review', 'experimental-design', 
                       'research-development', 'data-analysis', 'paper-writing', 'research-operations']:
                return part.replace('-', ' ').title()
        return 'General'
    
    def list_agents(self) -> None:
        """List all available agents organized by category"""
        if not self.agents:
            print("No agents loaded")
            return
        
        # Group by category
        categories = {}
        for agent in self.agents.values():
            category = agent['category']
            if category not in categories:
                categories[category] = []
            categories[category].append(agent)
        
        print("🤖 Available Research Agents:")
        print("=" * 50)
        
        for category, agents in categories.items():
            print(f"\n📁 {category} ({len(agents)} agents):")
            for agent in agents:
                print(f"  • {agent['name']}")
                # Show first line of description
                desc_lines = agent['description'].split('\n')
                if desc_lines:
                    first_line = desc_lines[0].strip()
                    if first_line:
                        print(f"    {first_line[:80]}...")
    
    def get_agent(self, name: str) -> Optional[Dict[str, Any]]:
        """Get a specific agent by name"""
        return self.agents.get(name)
    
    def find_relevant_agents(self, query: str, limit: int = 3) -> List[Dict[str, Any]]:
        """Find the most relevant agents for a query"""
        query_lower = query.lower()
        scored_agents = []
        
        for agent in self.agents.values():
            score = 0
            description_lower = agent['description'].lower()
            
            # Score based on keyword matches
            query_words = query_lower.split()
            for word in query_words:
                if word in description_lower:
                    score += 1
                if word in agent['name'].lower():
                    score += 2
            
            # Boost score for specific research terms
            research_terms = {
                'literature': ['literature-synthesizer', 'paper-finder', 'citation-analyzer'],
                'statistical': ['statistical-analyst', 'statistical-consultant'],
                'analysis': ['statistical-analyst', 'data-visualizer', 'results-interpreter'],
                'writing': ['academic-writer', 'research-documenter'],
                'ideas': ['research-ideator', 'hypothesis-generator'],
                'experiment': ['experiment-planner', 'methodology-designer'],
                'data': ['data-visualizer', 'statistical-analyst', 'ml-researcher']
            }
            
            for term, relevant_agents in research_terms.items():
                if term in query_lower and agent['name'] in relevant_agents:
                    score += 5
            
            if score > 0:
                scored_agents.append((score, agent))
        
        # Sort by score and return top results
        scored_agents.sort(key=lambda x: x[0], reverse=True)
        return [agent for score, agent in scored_agents[:limit]]
    
    def execute_agent(self, agent_name: str, user_query: str, context: str = "") -> Dict[str, Any]:
        """Execute a specific agent with user query"""
        agent = self.get_agent(agent_name)
        if not agent:
            return {
                'success': False,
                'error': f"Agent '{agent_name}' not found",
                'available_agents': list(self.agents.keys())
            }
        
        # Construct the full prompt for Augment
        augment_prompt = self._build_augment_prompt(agent, user_query, context)
        
        return {
            'success': True,
            'agent': agent['name'],
            'category': agent['category'],
            'tools': agent['tools'],
            'prompt': augment_prompt,
            'instructions': self._get_execution_instructions(agent)
        }
    
    def _build_augment_prompt(self, agent: Dict[str, Any], user_query: str, context: str) -> str:
        """Build the complete prompt for Augment"""
        return f"""You are now acting as the {agent['name']} research agent.

{agent['system_prompt']}

Current Research Context:
{context if context else "No additional context provided"}

User Request:
{user_query}

Please respond according to your specialized role as {agent['name']}. Use the tools and approaches specified in your instructions above."""
    
    def _get_execution_instructions(self, agent: Dict[str, Any]) -> str:
        """Get execution instructions for the user"""
        return f"""
🤖 Executing Agent: {agent['name']}
📁 Category: {agent['category']}
🛠️  Available Tools: {', '.join(agent['tools']) if agent['tools'] else 'All tools'}

To use this agent effectively:
1. Copy the generated prompt to Augment
2. Ensure the specified tools are available
3. Follow up with clarifying questions if needed
4. Chain with other agents for complex workflows
"""

def main():
    parser = argparse.ArgumentParser(description='Augment Agent Integration System')
    parser.add_argument('--list-agents', action='store_true', help='List all available agents')
    parser.add_argument('--use-agent', type=str, help='Use a specific agent by name')
    parser.add_argument('--auto-select', type=str, help='Auto-select agent based on query')
    parser.add_argument('--query', type=str, help='Query to send to the agent')
    parser.add_argument('--context', type=str, default='', help='Additional context for the agent')
    parser.add_argument('--agents-dir', type=str, default='.', help='Path to agents directory')
    
    args = parser.parse_args()
    
    # Initialize the system
    system = AugmentAgentSystem(args.agents_dir)
    
    if args.list_agents:
        system.list_agents()
        return
    
    if args.use_agent:
        if not args.query:
            print("Error: --query is required when using --use-agent")
            return
        
        result = system.execute_agent(args.use_agent, args.query, args.context)
        
        if result['success']:
            print(result['instructions'])
            print("\n" + "="*60)
            print("PROMPT FOR AUGMENT:")
            print("="*60)
            print(result['prompt'])
        else:
            print(f"Error: {result['error']}")
            if 'available_agents' in result:
                print(f"Available agents: {', '.join(result['available_agents'])}")
        return
    
    if args.auto_select:
        relevant_agents = system.find_relevant_agents(args.auto_select)
        
        if not relevant_agents:
            print("No relevant agents found for your query")
            return
        
        print(f"🔍 Found {len(relevant_agents)} relevant agents for: '{args.auto_select}'")
        print("\nRecommended agents:")
        
        for i, agent in enumerate(relevant_agents, 1):
            print(f"\n{i}. {agent['name']} ({agent['category']})")
            desc_lines = agent['description'].split('\n')
            if desc_lines:
                print(f"   {desc_lines[0].strip()[:100]}...")
        
        # Auto-execute the top recommendation
        if relevant_agents:
            top_agent = relevant_agents[0]
            print(f"\n🚀 Auto-executing top recommendation: {top_agent['name']}")
            
            result = system.execute_agent(top_agent['name'], args.auto_select, args.context)
            if result['success']:
                print(result['instructions'])
                print("\n" + "="*60)
                print("PROMPT FOR AUGMENT:")
                print("="*60)
                print(result['prompt'])
        return
    
    # If no specific action, show help
    parser.print_help()

if __name__ == "__main__":
    main()
