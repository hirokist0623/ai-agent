# インフラ要件定義書

## 1. 概要

(プロジェクトの目的、規模、主要な要件などを簡潔に記載してください。)

## 2. 利用目的と構成詳細

(各サービスの具体的な利用目的、設定、構成などの詳細を記載してください。)

例：

- EC2: t3.medium インスタンスを使用し、Web サーバーとして構成。Auto Scaling グループを設定し、需要に応じて 2-5 台の範囲でスケール。
- ECS: Fargate を使用してマイクロサービスをデプロイ。タスク定義には Nginx とアプリケーションコンテナを含む。
- Cognito: ユーザープールを作成し、アプリケーションの認証基盤として使用。ソーシャル ID プロバイダー（Google, Facebook）との連携も行う。
- CodePipeline: GitHub リポジトリと連携し、main ブランチへのプッシュをトリガーにビルド、テスト、デプロイを自動化。

## 3. システム構成

### 2.1 利用するベンダー

- 例: Amazon Web Services (AWS)

### 2.2 利用する主要サービス/機能

#### コンピューティング

- 例: Amazon EC2 (Elastic Compute Cloud)
  - (用途: 例えば Web サーバー、アプリケーションサーバーなど)
- 例: Amazon ECS (Elastic Container Service)
  - (用途: コンテナ化されたアプリケーションの実行と管理)

#### ネットワーキング

- 例: Amazon VPC (Virtual Private Cloud)
- 例: Elastic Load Balancing
  - (用途: トラフィック分散、高可用性の確保)

#### ストレージ

- 例: Amazon S3 (Simple Storage Service)
  - (用途: 静的ファイルの保存、バックアップなど)
- 例: Amazon EBS (Elastic Block Store)
  - (用途: EC2 インスタンス用の永続的ストレージ)

#### データベース

- 例: Amazon RDS (Relational Database Service)
  - (使用するデータベースエンジン: 例えば MySQL, PostgreSQL など)

#### セキュリティ、ID、アクセス管理

- 例: AWS IAM (Identity and Access Management)
- 例: Amazon Cognito
  - (用途: ユーザー認証、認可の管理)

#### 監視とロギング

- 例: Amazon CloudWatch
- 例: AWS CloudTrail

#### CI/CD

- 例: AWS CodePipeline
  - (用途: 継続的インテグレーション/デリバリーパイプラインの構築)
- 例: AWS CodeBuild
- 例: AWS CodeDeploy

#### その他

- 例: Amazon Route 53 (DNS サービス)
- 例: Amazon CloudFront (コンテンツデリバリーネットワーク)
