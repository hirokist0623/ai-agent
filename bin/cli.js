#!/usr/bin/env node

const { spawn } = require('child_process');
const path = require('path');
const yargs = require('yargs');

const commandConfigs = {
  "init": {
    "command": ['init', 'Initialize the agent structure', {}],
    "module": 'agent_compositions.init'
  },
  "start": {
    "command": ['start', 'Start using agents', {}],
    "module": 'agent_compositions.start'
  },
  "cleanup": {
    "command": ['cleanup', 'Clean up local environment', {}],
    "module": 'agents.execution.git.cleanup'
  },
  "commit": {
    "command": ['commit', 'Support committing', {}],
    "module": 'agent_compositions.simple_commit_agent'
  },
  "generate": {
    "command": ['generate <projectName>', 'Generate GCP infrastructure', (yargs) => {
      yargs.positional('projectName', {
        describe: 'Name of the project',
        type: 'string'
      });
    }],
    "module": 'agents.planning.create_readme.structures.main'
  }
};

const yargsInstance = yargs;

// コマンドの動的生成
Object.entries(commandConfigs).forEach(([key, config]) => {
  yargsInstance.command(...config.command);
});

const argv = yargsInstance.help().argv;

const executeCommand = (command) => {
  const config = commandConfigs[command];
  if (!config) {
    console.error(`Unknown command: ${command}`);
    process.exit(1);
  }

  const agentsDir = path.join(__dirname, '..');
  process.env.PYTHONPATH = `${agentsDir}:${process.env.PYTHONPATH || ''}`;

  const args = ['-m', config.module];
  if (command === 'generate') {
    args.push(argv.projectName);
  }

  const pythonProcess = spawn('python', args, {
    stdio: 'inherit',
    env: process.env
  });

  pythonProcess.on('close', (code) => {
    console.log(`Python script exited with code ${code}`);
  });
};

if (argv._[0]) {
  executeCommand(argv._[0]);
}