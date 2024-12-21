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
  const pythonScript = path.join(__dirname, 'agents', 'planning', 'create_readme', 'structures', 'main.py');
  const pythonProcess = spawn('python', ['-m', 'agents.planning.create_readme.structures.main', argv.projectName]);

  pythonProcess.stdout.on('data', (data) => {
    console.log(`${data}`);
  });

  pythonProcess.stderr.on('data', (data) => {
    console.error(`${data}`);
  });

  pythonProcess.on('close', (code) => {
    console.log(`Python script exited with code ${code}`);
  });
}