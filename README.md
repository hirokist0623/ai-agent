# ai-agent


## Directory Structure

```
ai-agent/
├── .ai_base
│   └── directory_structure.yaml
├── README.md
├── agent_compositions
│   ├── agents_base.py
│   ├── agents_modern_base.py
│   ├── init
│   │   └── main.py
│   ├── readme_creator.py
│   ├── simple_commit_agent.py
│   └── specification_writer.py
├── agents
│   ├── ai_base_agent.py
│   ├── base_agent.py
│   ├── execution
│   │   ├── git
│   │   │   ├── ai_commit_manager.py
│   │   │   ├── branch_manager.py
│   │   │   ├── cleanup.py
│   │   │   ├── pr_creator.py
│   │   │   ├── prompts
│   │   │   │   └── commit_message.yaml
│   │   │   └── push_manager.py
│   │   ├── init_config
│   │   │   └── create_config.py
│   │   ├── readme
│   │   │   ├── create_structure.py
│   │   │   └── reset_readme.py
│   │   └── scan_directory_structure.py
│   ├── multi_agent
│   │   ├── information_evaluator.py
│   │   ├── interview_conductor.py
│   │   ├── multi_agent_coordinator.py
│   │   └── persona_generator.py
│   ├── planning
│   │   └── planning_agent.py
│   ├── reflection
│   │   └── reflection_agent.py
│   └── tool-use
│       └── tool_use_agent.py
├── bin
│   └── cli.js
├── documentation_agent
│   └── main.py
├── package.json
└── utils
    ├── color_print.py
    ├── git.py
    ├── load_yaml.py
    └── readme.py
```
