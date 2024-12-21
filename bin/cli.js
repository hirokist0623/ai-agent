#!/usr/bin/env node

const { spawn } = require('child_process');
const path = require('path');
const yargs = require('yargs');

const argv = yargs
  .command('generate <projectName>', 'Generate GCP infrastructure', (yargs) => {
    yargs.positional('projectName', {
      describe: 'Name of the project',
      type: 'string'
    })
  })
  .help()
  .argv;

if (argv._[0] === 'generate') {
  // Set the PYTHONPATH to include the directory containing the 'agents' package
  const agentsDir = path.join(__dirname, '..');
  process.env.PYTHONPATH = `${agentsDir}:${process.env.PYTHONPATH || ''}`;

  // Use Python's -m option to run the module as a script
  const pythonProcess = spawn('python', [
    '-m',
    'agents.planning.create_readme.structures.main',
    argv.projectName
  ], {
    stdio: 'inherit', // This will forward all stdio to the parent process
    env: process.env // Make sure to pass the modified environment
  });

  pythonProcess.on('close', (code) => {
    console.log(`Python script exited with code ${code}`);
  });
}