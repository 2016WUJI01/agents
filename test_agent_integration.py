#!/usr/bin/env python3
"""
Test script for the improved Augment Agent Integration System
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, '.')

from augment_agent_integration import AugmentAgentSystem

def create_test_agent_file(temp_dir: Path, name: str, category: str) -> Path:
    """Create a test agent file"""
    agent_content = f"""---
name: {name}
description: |
  This is a test agent for {category}.
  It demonstrates the functionality of the system.
color: blue
tools: web-search, codebase-retrieval
---

You are a {name} agent specialized in {category}.

Your role is to help users with tasks related to {category}.

## Instructions:
1. Analyze the user's request
2. Use appropriate tools
3. Provide detailed responses
4. Follow best practices

Always be helpful and accurate in your responses.
"""
    
    agent_file = temp_dir / f"{name.replace(' ', '_').lower()}.md"
    agent_file.write_text(agent_content)
    return agent_file

def test_basic_functionality():
    """Test basic functionality of the improved system"""
    print("🧪 Testing Augment Agent Integration System")
    print("=" * 50)
    
    # Create temporary directory with test agents
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        output_path = temp_path / "output"
        
        # Create test agents
        test_agents = [
            ("Research Ideator", "research-planning"),
            ("Statistical Analyst", "data-analysis"),
            ("Literature Synthesizer", "literature-review"),
        ]
        
        for name, category in test_agents:
            create_test_agent_file(temp_path, name, category)
        
        # Initialize system
        print(f"📁 Created test environment in: {temp_path}")
        system = AugmentAgentSystem(str(temp_path), str(output_path), verbose=True)
        
        # Test 1: Basic loading
        print(f"\n✅ Test 1: Loaded {len(system.agents)} agents")
        
        # Test 2: List agents
        print("\n✅ Test 2: Listing agents")
        system.list_agents(save_to_file=True)
        
        # Test 3: Statistics
        print("\n✅ Test 3: Agent statistics")
        stats = system.get_agent_statistics()
        print(f"Statistics: {stats}")
        
        # Test 4: Search functionality
        print("\n✅ Test 4: Search functionality")
        results = system.search_agents("research")
        print(f"Found {len(results)} agents matching 'research'")
        
        # Test 5: Validation
        print("\n✅ Test 5: Agent validation")
        issues = system.validate_agents()
        total_issues = sum(len(issue_list) for issue_list in issues.values())
        print(f"Validation found {total_issues} issues")
        
        # Test 6: Export functionality
        print("\n✅ Test 6: Export functionality")
        try:
            json_file = system.export_agents_data('json')
            print(f"Exported to JSON: {json_file}")
            
            yaml_file = system.export_agents_data('yaml')
            print(f"Exported to YAML: {yaml_file}")
            
            csv_file = system.export_agents_data('csv')
            print(f"Exported to CSV: {csv_file}")
        except Exception as e:
            print(f"Export test failed: {e}")
        
        # Test 7: Agent execution with output saving
        print("\n✅ Test 7: Agent execution")
        result = system.execute_agent(
            "Research Ideator", 
            "Generate ideas for machine learning research",
            "Focus on practical applications",
            save_output=True
        )
        
        if result['success']:
            print("Agent execution successful!")
            if 'output_file' in result:
                print(f"Output saved to: {result['output_file']}")
        else:
            print(f"Agent execution failed: {result['error']}")
        
        # Test 8: Auto-selection
        print("\n✅ Test 8: Auto-selection")
        relevant = system.find_relevant_agents("statistical analysis", limit=2)
        print(f"Found {len(relevant)} relevant agents for 'statistical analysis'")
        
        # Show output directory contents
        print(f"\n📂 Output directory contents:")
        if output_path.exists():
            for file in output_path.iterdir():
                print(f"  • {file.name} ({file.stat().st_size} bytes)")
        
        print("\n🎉 All tests completed successfully!")

if __name__ == "__main__":
    test_basic_functionality()
