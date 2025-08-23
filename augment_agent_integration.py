#!/usr/bin/env python3
"""
Augment Agent Integration System
Enables Augment to use Claude Code research agents for automation

Usage:
    python augment_agent_integration.py --list-agents
    python augment_agent_integration.py --use-agent research-ideator "Generate ideas for sparse forecasting"
    python augment_agent_integration.py --auto-select "I need help with statistical analysis"
    python augment_agent_integration.py --save-config agents_config.json
    python augment_agent_integration.py --export-prompts output_dir/
"""

import os
import sys
import yaml
import json
import argparse
import re
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

class AugmentAgentSystem:
    """Main system for integrating Claude Code agents with Augment"""

    def __init__(self, agents_dir: str = ".", output_dir: str = "output", verbose: bool = False):
        self.agents_dir = Path(agents_dir)
        self.output_dir = Path(output_dir)
        self.agents: Dict[str, Dict[str, Any]] = {}
        self.verbose = verbose

        # Create output directory if it doesn't exist
        self.output_dir.mkdir(exist_ok=True)

        # Setup logging
        self._setup_logging()

        self.load_agents()

    def _setup_logging(self) -> None:
        """Setup logging configuration"""
        log_level = logging.DEBUG if self.verbose else logging.INFO
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler(self.output_dir / 'agent_system.log')
            ]
        )
    
    def load_agents(self) -> None:
        """Load all agents from the agents directory"""
        if not self.agents_dir.exists():
            logging.warning(f"Agents directory {self.agents_dir} not found")
            return

        loaded_count = 0
        for agent_file in self.agents_dir.rglob("*.md"):
            try:
                agent = self._parse_agent_file(agent_file)
                if agent:
                    self.agents[agent['name']] = agent
                    logging.info(f"Loaded agent: {agent['name']}")
                    loaded_count += 1
            except Exception as e:
                logging.error(f"Error loading agent {agent_file}: {e}")

        logging.info(f"Successfully loaded {loaded_count} agents from {self.agents_dir}")

        # Save agents configuration to file
        self._save_agents_config()
    
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
                    logging.error(f"Error parsing {file_path}: {e}")
        return None

    def _save_agents_config(self) -> None:
        """Save agents configuration to JSON file"""
        config_file = self.output_dir / 'agents_config.json'

        # Create a simplified version for JSON serialization
        agents_config = {
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'agents_directory': str(self.agents_dir),
                'total_agents': len(self.agents)
            },
            'agents': {}
        }

        for name, agent in self.agents.items():
            agents_config['agents'][name] = {
                'name': agent['name'],
                'description': agent['description'],
                'category': agent['category'],
                'color': agent['color'],
                'tools': agent['tools'],
                'file_path': agent['file_path']
            }

        try:
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(agents_config, f, indent=2, ensure_ascii=False)
            logging.info(f"Saved agents configuration to {config_file}")
        except Exception as e:
            logging.error(f"Failed to save agents configuration: {e}")

    def export_agents_data(self, format_type: str = 'json') -> str:
        """Export agents data in various formats"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        if format_type.lower() == 'json':
            return self._export_json(timestamp)
        elif format_type.lower() == 'yaml':
            return self._export_yaml(timestamp)
        elif format_type.lower() == 'csv':
            return self._export_csv(timestamp)
        else:
            raise ValueError(f"Unsupported export format: {format_type}")

    def _export_json(self, timestamp: str) -> str:
        """Export agents data as JSON"""
        output_file = self.output_dir / f'agents_export_{timestamp}.json'

        export_data = {
            'export_info': {
                'timestamp': datetime.now().isoformat(),
                'format': 'json',
                'total_agents': len(self.agents)
            },
            'agents': self.agents
        }

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)

        logging.info(f"Exported agents data to {output_file}")
        return str(output_file)

    def _export_yaml(self, timestamp: str) -> str:
        """Export agents data as YAML"""
        output_file = self.output_dir / f'agents_export_{timestamp}.yaml'

        export_data = {
            'export_info': {
                'timestamp': datetime.now().isoformat(),
                'format': 'yaml',
                'total_agents': len(self.agents)
            },
            'agents': self.agents
        }

        with open(output_file, 'w', encoding='utf-8') as f:
            yaml.dump(export_data, f, default_flow_style=False, allow_unicode=True)

        logging.info(f"Exported agents data to {output_file}")
        return str(output_file)

    def _export_csv(self, timestamp: str) -> str:
        """Export agents data as CSV"""
        import csv

        output_file = self.output_dir / f'agents_export_{timestamp}.csv'

        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)

            # Write header
            writer.writerow(['Name', 'Category', 'Description', 'Tools', 'File Path'])

            # Write agent data
            for agent in self.agents.values():
                writer.writerow([
                    agent['name'],
                    agent['category'],
                    agent['description'].replace('\n', ' ').strip(),
                    ', '.join(agent['tools']) if agent['tools'] else '',
                    agent['file_path']
                ])

        logging.info(f"Exported agents data to {output_file}")
        return str(output_file)

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
    
    def list_agents(self, save_to_file: bool = False) -> Optional[str]:
        """List all available agents organized by category"""
        if not self.agents:
            message = "No agents loaded"
            print(message)
            return None

        # Group by category
        categories = {}
        for agent in self.agents.values():
            category = agent['category']
            if category not in categories:
                categories[category] = []
            categories[category].append(agent)

        # Build output
        output_lines = []
        output_lines.append("🤖 Available Research Agents:")
        output_lines.append("=" * 50)

        for category, agents in categories.items():
            output_lines.append(f"\n📁 {category} ({len(agents)} agents):")
            for agent in agents:
                output_lines.append(f"  • {agent['name']}")
                # Show first line of description
                desc_lines = agent['description'].split('\n')
                if desc_lines:
                    first_line = desc_lines[0].strip()
                    if first_line:
                        output_lines.append(f"    {first_line[:80]}...")

        output_text = '\n'.join(output_lines)
        print(output_text)

        # Save to file if requested
        if save_to_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = self.output_dir / f'agents_list_{timestamp}.txt'

            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(output_text)
                f.write(f"\n\nGenerated at: {datetime.now().isoformat()}")

            logging.info(f"Saved agents list to {output_file}")
            return str(output_file)

        return None
    
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
    
    def execute_agent(self, agent_name: str, user_query: str, context: str = "", save_output: bool = False) -> Dict[str, Any]:
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
        instructions = self._get_execution_instructions(agent)

        result = {
            'success': True,
            'agent': agent['name'],
            'category': agent['category'],
            'tools': agent['tools'],
            'prompt': augment_prompt,
            'instructions': instructions,
            'timestamp': datetime.now().isoformat(),
            'user_query': user_query,
            'context': context
        }

        # Save output if requested
        if save_output:
            output_file = self._save_execution_output(result)
            result['output_file'] = output_file

        return result

    def _save_execution_output(self, result: Dict[str, Any]) -> str:
        """Save execution output to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        agent_name_safe = re.sub(r'[^\w\-_]', '_', result['agent'])
        output_file = self.output_dir / f'execution_{agent_name_safe}_{timestamp}.txt'

        output_content = f"""AUGMENT AGENT EXECUTION OUTPUT
{'=' * 50}

Agent: {result['agent']}
Category: {result['category']}
Timestamp: {result['timestamp']}
Tools: {', '.join(result['tools']) if result['tools'] else 'All tools'}

User Query:
{result['user_query']}

Context:
{result['context'] if result['context'] else 'No additional context provided'}

{result['instructions']}

{'=' * 60}
PROMPT FOR AUGMENT:
{'=' * 60}
{result['prompt']}
"""

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(output_content)

        logging.info(f"Saved execution output to {output_file}")
        return str(output_file)

    def get_agent_statistics(self) -> Dict[str, Any]:
        """Get statistics about loaded agents"""
        if not self.agents:
            return {'total_agents': 0, 'categories': {}}

        categories = {}
        tools_usage = {}

        for agent in self.agents.values():
            # Count by category
            category = agent['category']
            categories[category] = categories.get(category, 0) + 1

            # Count tool usage
            for tool in agent['tools']:
                tools_usage[tool] = tools_usage.get(tool, 0) + 1

        return {
            'total_agents': len(self.agents),
            'categories': categories,
            'tools_usage': tools_usage,
            'most_common_category': max(categories.items(), key=lambda x: x[1])[0] if categories else None,
            'most_used_tool': max(tools_usage.items(), key=lambda x: x[1])[0] if tools_usage else None
        }

    def search_agents(self, search_term: str, search_in: List[str] = None) -> List[Dict[str, Any]]:
        """Search agents by term in specified fields"""
        if search_in is None:
            search_in = ['name', 'description', 'category']

        search_term_lower = search_term.lower()
        matching_agents = []

        for agent in self.agents.values():
            match_found = False

            for field in search_in:
                if field in agent:
                    field_value = str(agent[field]).lower()
                    if search_term_lower in field_value:
                        match_found = True
                        break

            if match_found:
                matching_agents.append(agent)

        return matching_agents

    def validate_agents(self) -> Dict[str, List[str]]:
        """Validate all loaded agents and return issues"""
        issues = {
            'missing_fields': [],
            'invalid_tools': [],
            'empty_descriptions': [],
            'missing_files': []
        }

        required_fields = ['name', 'description', 'system_prompt', 'file_path']

        for agent_name, agent in self.agents.items():
            # Check required fields
            for field in required_fields:
                if field not in agent or not agent[field]:
                    issues['missing_fields'].append(f"{agent_name}: missing {field}")

            # Check if description is meaningful
            if agent.get('description', '').strip() == '':
                issues['empty_descriptions'].append(agent_name)

            # Check if file still exists
            file_path = Path(agent.get('file_path', ''))
            if not file_path.exists():
                issues['missing_files'].append(f"{agent_name}: {file_path}")

        return issues
    
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
    parser.add_argument('--output-dir', type=str, default='output', help='Output directory for files')
    parser.add_argument('--save-output', action='store_true', help='Save output to files')
    parser.add_argument('--export-format', type=str, choices=['json', 'yaml', 'csv'],
                       help='Export agents data in specified format')
    parser.add_argument('--search', type=str, help='Search agents by term')
    parser.add_argument('--stats', action='store_true', help='Show agent statistics')
    parser.add_argument('--validate', action='store_true', help='Validate all agents')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose logging')

    args = parser.parse_args()

    # Initialize the system
    system = AugmentAgentSystem(args.agents_dir, args.output_dir, args.verbose)
    
    # Handle various commands
    if args.export_format:
        try:
            output_file = system.export_agents_data(args.export_format)
            print(f"✅ Exported agents data to: {output_file}")
        except Exception as e:
            print(f"❌ Export failed: {e}")
        return

    if args.stats:
        stats = system.get_agent_statistics()
        print("📊 Agent Statistics:")
        print("=" * 30)
        print(f"Total Agents: {stats['total_agents']}")
        print(f"Categories: {len(stats['categories'])}")

        if stats['categories']:
            print("\nAgents by Category:")
            for category, count in sorted(stats['categories'].items()):
                print(f"  • {category}: {count}")

        if stats['tools_usage']:
            print(f"\nMost Used Tool: {stats['most_used_tool']}")
            print(f"Most Common Category: {stats['most_common_category']}")

        if args.save_output:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            stats_file = system.output_dir / f'agent_stats_{timestamp}.json'
            with open(stats_file, 'w') as f:
                json.dump(stats, f, indent=2)
            print(f"✅ Statistics saved to: {stats_file}")
        return

    if args.validate:
        issues = system.validate_agents()
        print("🔍 Agent Validation Results:")
        print("=" * 35)

        total_issues = sum(len(issue_list) for issue_list in issues.values())
        if total_issues == 0:
            print("✅ All agents are valid!")
        else:
            print(f"❌ Found {total_issues} issues:")

            for issue_type, issue_list in issues.items():
                if issue_list:
                    print(f"\n{issue_type.replace('_', ' ').title()}:")
                    for issue in issue_list:
                        print(f"  • {issue}")

        if args.save_output:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            validation_file = system.output_dir / f'validation_report_{timestamp}.json'
            with open(validation_file, 'w') as f:
                json.dump(issues, f, indent=2)
            print(f"✅ Validation report saved to: {validation_file}")
        return

    if args.search:
        matching_agents = system.search_agents(args.search)
        print(f"🔍 Search Results for '{args.search}':")
        print("=" * 40)

        if not matching_agents:
            print("No matching agents found.")
        else:
            print(f"Found {len(matching_agents)} matching agents:")
            for agent in matching_agents:
                print(f"\n• {agent['name']} ({agent['category']})")
                desc_lines = agent['description'].split('\n')
                if desc_lines:
                    print(f"  {desc_lines[0].strip()[:100]}...")

        if args.save_output and matching_agents:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            search_file = system.output_dir / f'search_results_{timestamp}.json'
            with open(search_file, 'w') as f:
                json.dump({
                    'search_term': args.search,
                    'results_count': len(matching_agents),
                    'agents': matching_agents
                }, f, indent=2)
            print(f"✅ Search results saved to: {search_file}")
        return

    if args.list_agents:
        output_file = system.list_agents(save_to_file=args.save_output)
        if output_file:
            print(f"✅ Agents list saved to: {output_file}")
        return
    
    if args.use_agent:
        if not args.query:
            print("Error: --query is required when using --use-agent")
            return
        
        result = system.execute_agent(args.use_agent, args.query, args.context, args.save_output)

        if result['success']:
            print(result['instructions'])
            print("\n" + "="*60)
            print("PROMPT FOR AUGMENT:")
            print("="*60)
            print(result['prompt'])

            if 'output_file' in result:
                print(f"\n✅ Execution output saved to: {result['output_file']}")
        else:
            print(f"❌ Error: {result['error']}")
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
            
            result = system.execute_agent(top_agent['name'], args.auto_select, args.context, args.save_output)
            if result['success']:
                print(result['instructions'])
                print("\n" + "="*60)
                print("PROMPT FOR AUGMENT:")
                print("="*60)
                print(result['prompt'])

                if 'output_file' in result:
                    print(f"\n✅ Execution output saved to: {result['output_file']}")
        return
    
    # If no specific action, show help
    parser.print_help()

if __name__ == "__main__":
    main()
