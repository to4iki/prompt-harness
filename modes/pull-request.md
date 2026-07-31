---
name: pull-request
triggers: pr, pull request, プルリク
---

## 判定原則

- 冗長な説明は避け、とにかくシンプル化すること
- PullRequest のテンプレートを全て埋めることを目的にしない

## 停止条件

- PullRequest の作成が失敗か、完了している

## Gate

- 無し（このモードは Gate を追加しない。同時に適用される他モードの Gate は有効）
