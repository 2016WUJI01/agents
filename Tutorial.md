# Research Agents Tutorial

This tutorial provides a comprehensive guide to using specialized research agents for academic and scientific work. Each agent is designed for specific research tasks and contexts.

## Table of Contents

1. [🚀 Quick Start - How to Use](#🚀-quick-start---how-to-use)
2. [💡 Choosing the Right Agent](#💡-choosing-the-right-agent)
3. [📋 Detailed Agent Functions](#📋-detailed-agent-functions)
   - [Data Analysis Agents](#data-analysis-agents)
   - [Experimental Design Agents](#experimental-design-agents)
   - [Literature Review Agents](#literature-review-agents)
   - [Paper Writing Agents](#paper-writing-agents)
   - [Research Development Agents](#research-development-agents)
   - [Research Operations Agents](#research-operations-agents)
   - [Research Planning Agents](#research-planning-agents)

---

## 🚀 Quick Start - How to Use

### Method 1: Command Line Tool Usage

Your workspace contains a complete agent integration system. Here's how to use it:

#### 1. List All Available Agents
```bash
python augment_agent_integration.py --list-agents
```

#### 2. Use a Specific Agent
```bash
python augment_agent_integration.py --use-agent research-ideator --query "Generate research ideas for sparse time series forecasting"
```

#### 3. Auto-Select Most Relevant Agent
```bash
python augment_agent_integration.py --auto-select "I need help with statistical analysis"
```

#### 4. Search for Specific Agents
```bash
python augment_agent_integration.py --search "statistical"
```

#### 5. View Agent Statistics
```bash
python augment_agent_integration.py --stats
```

#### 6. Export Agent Configuration
```bash
python augment_agent_integration.py --export-format json
```

### Method 2: Direct Use in Augment

Based on the system configuration, these agents are automatically triggered based on your request descriptions. The system recognizes these patterns:

#### Auto-Trigger Rules
- **"research ideas"** → triggers `research-ideator`
- **"literature review"** → triggers `literature-synthesizer`
- **"statistical analysis"** → triggers `statistical-analyst`
- **"write paper"** → triggers `academic-writer`
- **"data visualization"** → triggers `data-visualizer`
- **"experiment design"** → triggers `methodology-designer`

#### Specific Usage Examples

**Example 1: Generate Research Ideas**
```
User Input: "I want to explore new applications of transformer models but I'm not sure what hasn't been done yet"
System Response: Automatically uses research-ideator agent
```

**Example 2: Literature Review**
```
User Input: "I need to find and synthesize all research on remote work productivity"
System Response: Uses paper-finder → literature-synthesizer → citation-analyzer
```

**Example 3: Experimental Research**
```
User Input: "I want to test whether music affects coding performance"
System Response: Uses methodology-designer → statistical-consultant → experiment-planner
```

### Method 3: Multi-Agent Workflows

#### Complete Research Project Pipeline
```
research-ideator → gap-analyzer → hypothesis-generator → proposal-writer
↓
paper-finder → literature-synthesizer → reference-manager
↓
methodology-designer → experiment-planner → statistical-consultant
↓
research-coder → statistical-analyst → data-visualizer → results-interpreter
↓
academic-writer → figure-creator → citation-formatter → research-documenter
```

#### Execute Workflows via Command Line
```bash
# Step 1: Generate research ideas
python augment_agent_integration.py --use-agent research-ideator --query "AI applications in healthcare" --save-output

# Step 2: Analyze research gaps
python augment_agent_integration.py --use-agent gap-analyzer --query "Analyze gaps in the generated ideas" --context "Previous step output" --save-output

# Step 3: Generate hypotheses
python augment_agent_integration.py --use-agent hypothesis-generator --query "Create testable hypotheses from the gaps" --save-output
```

### Configuration Files

The system automatically generates configuration files:
- `output/agents_config.json` - Agent configuration information
- `output/agent_system.log` - System operation logs
- `output/execution_*.txt` - Execution output files

### Advanced Features

#### 1. Agent Validation
```bash
python augment_agent_integration.py --validate
```

#### 2. Detailed Statistics
```bash
python augment_agent_integration.py --stats --save-output
```

#### 3. Batch Export
```bash
python augment_agent_integration.py --export-format yaml --save-output
```

### Best Practice Recommendations

1. **Start Simple**: Begin with single agents to familiarize yourself with the system
2. **Save Outputs**: Use `--save-output` flag to preserve all results
3. **Provide Context**: Use `--context` parameter to provide relevant background
4. **Chain Usage**: Use one agent's output as input for the next
5. **Regular Validation**: Use `--validate` to ensure all agents are working properly

### Troubleshooting

#### Common Issues:
- **Agent Not Found**: Use `--list-agents` to see available agents
- **No Output Files**: Ensure write permissions and use `--save-output`
- **No Query Results**: Try more specific keywords

#### Get Help:
```bash
python augment_agent_integration.py --help
```

---

## 💡 Choosing the Right Agent

### How to Choose the Right Agent

1. **Identify your research phase**: Planning → Design → Implementation → Analysis → Writing → Dissemination
2. **Match your specific need**: Each agent specializes in particular tasks and contexts
3. **Consider your expertise level**: Some agents provide more guidance for beginners, others assume advanced knowledge
4. **Think about collaboration needs**: Some agents excel at coordinating team efforts
5. **Assess time constraints**: Some agents help with quick tasks, others support long-term projects

### Getting Started

1. Identify which research phase you're in
2. Review the agent descriptions for your phase
3. Choose the agent that best matches your specific needs
4. Provide clear context about your research when engaging the agent
5. Ask for specific, actionable guidance
6. Follow up with questions to clarify any uncertainties

---

## 📋 Detailed Agent Functions

---

## Data Analysis Agents

### 1. Data Visualizer
**When to use**: Creating research visualizations, designing publication figures, or developing interactive data exploration tools.

**Key capabilities**:
- Publication-quality figure creation (300+ DPI, vector formats)
- Statistical visualization (error bars, confidence intervals, correlation matrices)
- Interactive dashboards and exploratory data analysis tools
- Specialized scientific visualizations (networks, geographic, temporal)
- Accessibility-focused design (colorblind-friendly palettes)

**Tools**: Python (Matplotlib, Seaborn, Plotly), R (ggplot2, shiny), JavaScript (D3.js, Observable)

**Example use cases**:
- "Create publication-quality figures for my clinical trial results"
- "Build an interactive dashboard for longitudinal study data exploration"
- "Design accessible visualizations for policymaker presentations"

### 2. ML Researcher
**When to use**: Applying machine learning to research problems, developing novel ML algorithms, or using AI for scientific discovery.

**Key capabilities**:
- Research-oriented ML applications with domain knowledge integration
- Novel algorithm development and rigorous benchmarking
- Interpretable and explainable ML for research transparency
- Scientific data analysis with small sample strategies
- Hypothesis generation using unsupervised learning
- Ethical and responsible ML practices

**Specializations**: Bioinformatics, social sciences, healthcare, education, environmental science

**Example use cases**:
- "Use ML to identify genomic patterns predicting disease susceptibility"
- "Develop a new clustering algorithm for social network analysis"
- "Build interpretable models for educational outcome prediction"

### 3. Results Interpreter
**When to use**: Interpreting complex research results, drawing meaningful conclusions, or translating technical findings into actionable insights.

**Key capabilities**:
- Statistical result interpretation in plain language
- Effect size assessment and practical significance evaluation
- Complex pattern recognition (interactions, mediation, moderation)
- Uncertainty and limitation assessment
- Contextual integration with existing literature
- Audience-specific communication

**Framework**: What → Confidence → Importance → Meaning → Context → Implications → Next Steps

**Example use cases**:
- "My results are opposite to my hypothesis - how do I interpret this?"
- "Explain this three-way interaction effect in practical terms"
- "Assess whether my statistically significant results are practically meaningful"

### 4. Statistical Analyst
**When to use**: Conducting advanced statistical analyses, building statistical models, or performing complex data analysis.

**Key capabilities**:
- Advanced statistical modeling (mixed-effects, survival analysis, time series)
- Complex hypothesis testing with appropriate corrections
- Specialized techniques (SEM, factor analysis, causal inference)
- Missing data handling and sampling issue resolution
- Model validation and diagnostics
- Statistical interpretation and communication

**Software expertise**: R, Python, SAS, Stata, SPSS, Stan/BUGS

**Example use cases**:
- "Analyze longitudinal nested data with missing values"
- "Build predictive models for patient outcomes"
- "Conduct meta-analysis of 20 intervention studies"

---

## Experimental Design Agents

### 5. Experiment Planner
**When to use**: Planning detailed experimental procedures, creating research protocols, or organizing data collection activities.

**Key capabilities**:
- Detailed protocol development with step-by-step procedures
- Standard Operating Procedure (SOP) creation
- Data collection planning and quality control measures
- Resource and logistics coordination
- Risk management and contingency planning
- Implementation monitoring systems

**Protocol components**: Background, objectives, design, procedures, data collection, quality control, analysis plan, timeline

**Example use cases**:
- "Create a detailed protocol for a randomized controlled trial"
- "Standardize laboratory procedures across multiple sessions"
- "Plan data collection for a 5-year longitudinal study"

### 6. Methodology Designer
**When to use**: Designing research methodologies, selecting appropriate research approaches, or creating comprehensive research designs.

**Key capabilities**:
- Research methodology selection and optimization
- Mixed-methods design integration
- Sampling strategy development
- Validity and reliability enhancement
- Ethical consideration integration
- Cross-cultural research adaptation

**Example use cases**:
- "Design a mixed-methods study for educational intervention research"
- "Select appropriate methodology for cross-cultural psychology research"
- "Create a research design that balances internal and external validity"

### 7. Statistical Consultant
**When to use**: Planning statistical analyses, conducting power analyses, or selecting appropriate statistical tests.

**Key capabilities**:
- Statistical analysis planning and power analysis
- Appropriate statistical test selection
- Sample size determination
- Analysis assumption checking
- Statistical interpretation guidance
- Reproducible analysis workflow design

**Example use cases**:
- "Plan statistical analysis for my experimental study"
- "Determine required sample size for detecting meaningful effects"
- "Select appropriate tests for my complex survey data"

---

## Literature Review Agents

### 8. Citation Analyzer
**When to use**: Analyzing citation patterns, tracking research impact, or understanding knowledge networks.

**Key capabilities**:
- Citation pattern analysis and network mapping
- Research impact assessment
- Influential paper identification
- Knowledge network visualization
- Trend analysis in citation patterns
- Bibliometric indicator calculation

**Example use cases**:
- "Identify the most influential papers in machine learning ethics"
- "Map citation networks in climate change research"
- "Track the evolution of research impact over time"

### 9. Literature Synthesizer
**When to use**: Synthesizing findings from multiple papers, creating comprehensive literature reviews, or integrating diverse research perspectives.

**Key capabilities**:
- Thematic analysis across multiple studies
- Evidence synthesis and integration
- Contradiction and consensus identification
- Theoretical framework development
- Gap identification and future direction mapping
- Narrative construction from diverse sources

**Example use cases**:
- "Synthesize findings from 50 studies on remote work effectiveness"
- "Create a comprehensive literature review for my dissertation"
- "Integrate conflicting findings on social media and mental health"

### 10. Paper Finder
**When to use**: Searching for academic literature, finding relevant papers, or conducting systematic literature searches.

**Key capabilities**:
- Systematic search strategy development
- Database-specific search optimization
- Boolean search query construction
- Citation chaining and snowball sampling
- Grey literature identification
- Search result screening and filtering

**Example use cases**:
- "Find all relevant papers on AI bias in healthcare"
- "Conduct a systematic search for meta-analysis inclusion"
- "Identify emerging research in quantum computing applications"

### 11. Reference Manager
**When to use**: Organizing research references, formatting citations, or managing bibliographic databases.

**Key capabilities**:
- Reference organization and categorization
- Citation style formatting and conversion
- Bibliographic database management
- Duplicate detection and removal
- Reference verification and validation
- Integration with writing workflows

**Example use cases**:
- "Organize 200+ references for my thesis project"
- "Convert citations from APA to Nature format"
- "Clean and validate my reference database"

---

## Paper Writing Agents

### 12. Academic Writer
**When to use**: Writing research papers, crafting academic manuscripts, or developing scholarly communications.

**Key capabilities**:
- Academic writing structure and flow
- Discipline-specific writing conventions
- Argument development and evidence presentation
- Journal requirement compliance
- Revision and editing guidance
- Collaborative writing coordination

**Example use cases**:
- "Write the methods section for my experimental study"
- "Develop a compelling introduction for my Nature submission"
- "Revise my manuscript based on peer review feedback"

### 13. Citation Formatter
**When to use**: Formatting citations and references, converting between citation styles, or ensuring citation accuracy.

**Key capabilities**:
- Multi-style citation formatting (APA, MLA, Chicago, Nature, etc.)
- Automated citation generation from DOIs/URLs
- Reference list organization and formatting
- Citation accuracy verification
- Style guide compliance checking
- Batch citation processing

**Example use cases**:
- "Format 100 references in APA style"
- "Convert my entire bibliography from MLA to Chicago format"
- "Verify accuracy of all citations in my manuscript"

### 14. Figure Creator
**When to use**: Creating scientific figures, designing publication graphics, or developing visual elements for papers.

**Key capabilities**:
- Publication-standard figure design
- Multi-panel figure composition
- Scientific illustration creation
- Graph and chart optimization
- Figure caption writing
- Journal-specific formatting

**Example use cases**:
- "Create a multi-panel figure showing experimental results"
- "Design a graphical abstract for my paper"
- "Optimize figures for Nature journal submission"

### 15. Research Documenter
**When to use**: Creating comprehensive research documentation, developing research reports, or organizing research materials.

**Key capabilities**:
- Comprehensive documentation creation
- Research report structuring
- Method documentation and reproducibility
- Data documentation and metadata creation
- Protocol documentation
- Knowledge preservation and sharing

**Example use cases**:
- "Document my entire research methodology for reproducibility"
- "Create a comprehensive research report for stakeholders"
- "Organize and document my 3-year research project"

---

## Research Development Agents

### 16. Research Coder
**When to use**: Developing research software, implementing algorithms, or creating tools for data collection and analysis.

**Key capabilities**:
- Research-focused software development
- Algorithm implementation and optimization
- Data collection tool creation
- Analysis pipeline development
- Reproducible research code
- Open science tool development

**Example use cases**:
- "Implement a novel machine learning algorithm for my research"
- "Create a data collection app for field research"
- "Build reproducible analysis pipelines for my lab"

---

## Research Operations Agents

### 17. Collaboration Coordinator
**When to use**: Managing research collaborations, facilitating team communication, or coordinating multi-institutional projects.

**Key capabilities**:
- Multi-institutional collaboration management
- Communication protocol establishment
- Resource sharing coordination
- Timeline and milestone management
- Conflict resolution and mediation
- Partnership agreement development

**Example use cases**:
- "Coordinate a 5-institution research consortium"
- "Establish communication protocols for international collaboration"
- "Manage resource sharing across research teams"

### 18. Ethics Advisor
**When to use**: Navigating research ethics issues, preparing IRB applications, or ensuring ethical compliance.

**Key capabilities**:
- IRB application preparation and guidance
- Ethical framework application
- Risk assessment and mitigation
- Informed consent development
- Privacy and confidentiality planning
- Ethical review and compliance monitoring

**Example use cases**:
- "Prepare IRB application for human subjects research"
- "Assess ethical implications of AI research on vulnerable populations"
- "Develop informed consent procedures for sensitive research"

### 19. Research Project Manager
**When to use**: Managing complex research projects, coordinating research teams, or organizing multi-phase initiatives.

**Key capabilities**:
- Project planning and timeline management
- Resource allocation and budget tracking
- Team coordination and communication
- Risk management and contingency planning
- Quality assurance and milestone tracking
- Stakeholder management and reporting

**Example use cases**:
- "Manage a 3-year, multi-million dollar research grant"
- "Coordinate a complex clinical trial across multiple sites"
- "Plan and execute a large-scale longitudinal study"

---

## Research Planning Agents

### 20. Gap Analyzer
**When to use**: Conducting systematic literature reviews to identify research gaps or finding underexplored research areas.

**Key capabilities**:
- Systematic gap identification in literature
- Knowledge mapping and visualization
- Opportunity assessment and prioritization
- Trend analysis and future prediction
- Interdisciplinary gap discovery
- Research agenda development

**Example use cases**:
- "Identify research gaps in sustainable energy for my PhD proposal"
- "Map knowledge gaps in AI ethics research"
- "Find underexplored areas in educational technology"

### 21. Hypothesis Generator
**When to use**: Formulating testable hypotheses, developing theoretical predictions, or creating research questions.

**Key capabilities**:
- Testable hypothesis formulation
- Theoretical prediction development
- Research question refinement
- Hypothesis hierarchy creation
- Falsifiability assessment
- Experimental design alignment

**Example use cases**:
- "Generate testable hypotheses for my social psychology experiment"
- "Develop theoretical predictions for my computational model"
- "Refine my research questions for better testability"

### 22. Proposal Writer
**When to use**: Writing research proposals, grant applications, or project plans for academic research.

**Key capabilities**:
- Grant proposal structure and writing
- Funding agency requirement compliance
- Budget development and justification
- Impact statement creation
- Timeline and milestone planning
- Collaboration plan development

**Example use cases**:
- "Write an NSF research proposal for my machine learning project"
- "Develop a compelling NIH grant application"
- "Create a research proposal for industry partnership"

### 23. Research Ideator
**When to use**: Brainstorming research ideas, identifying novel research directions, or exploring interdisciplinary opportunities.

**Key capabilities**:
- Creative research question generation
- Interdisciplinary connection making
- Trend analysis and future forecasting
- Innovation opportunity identification
- Problem-to-research translation
- Research impact assessment

**Example use cases**:
- "Generate novel applications for transformer models"
- "Identify interdisciplinary opportunities combining psychology and AI"
- "Find new research directions in climate change mitigation"


