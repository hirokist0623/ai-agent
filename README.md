# ai-agent

# メモ

- 各種ローカルでnpxで呼び出すことで、実装からPRまでを実行してくれるagent群を想定

```
npx ai-agent create-document "<機能名>"
```

- 必要な資料を作成して、実行ログをはく

```
.
└ .ai-agent/
  └ log/
```

```
[2024/12/01 01:00:00] npx ai-agent create-document "<機能名>"
[2024/12/01 01:00:00] PR: https://github.com/<org>/<repository>/pull/1
```
