#!/usr/bin/env node

const yargs = require('yargs/yargs');
const { hideBin } = require('yargs/helpers');

yargs(hideBin(process.argv))
  .command('run <agent>', '特定のエージェントを実行します', (yargs) => {
    return yargs.positional('agent', {
      describe: '実行するエージェントの名前',
      type: 'string'
    });
  }, (argv) => {
    console.log(`エージェントを実行中: ${argv.agent}`);
    // ここでエージェントを実行するロジックを実装
  })
  .help()
  .argv;