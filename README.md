# ai-agent

# コマンド一覧

- 各種ローカルで npx で呼び出すことで、実装から PR までを実行してくれる agent 群を想定

## agent-compositions

| コマンド | 説明 |
| :------- | :--- |
|          |      |

## agents

| 領域     | コマンド                                                     | 説明                             |
| :------- | :----------------------------------------------------------- | :------------------------------- |
| planning | `npx github:hirokist0623/ai-agent generate <プロジェクト名>` | infra の構成図を作成してくれます |

# 実行ログ

- 必要な資料を作成して、実行ログをはく想定

```
.
└ .ai-agent/
  └ config.yaml
  └ log/
```

```
[2024/12/01 01:00:00] npx ai-agent create-document "<機能名>"
[2024/12/01 01:00:00] PR: https://github.com/<org>/<repository>/pull/1
```
