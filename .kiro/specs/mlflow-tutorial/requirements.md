# Requirements Document

## Introduction

MLflowを端的に理解するためのチュートリアルコンテンツを作成する。対象者はMLflowを初めて使うMLエンジニア・データサイエンティスト。scikit-learnおよびPyTorchを使った実践的なサンプルコードを含み、Jupyter Book形式でGitHub Pagesへ公開できる構成とする。

**運用前提**: チュートリアルのノートブック実行はオフライン環境（インターネット非接続）での動作を保証する。ランタイム中の外部通信（データセットのダウンロード・外部APIコール等）は一切行わない。

## Requirements

### Requirement 1: MLflowコア概念の説明

**Objective:** As a MLエンジニア・データサイエンティスト, I want MLflowの主要コンポーネント（Tracking / Models / Model Registry / Projects）を体系的に学べること, so that MLflowの全体像を短時間で把握できる

#### Acceptance Criteria
1. The Tutorial shall MLflowの4つの主要コンポーネント（Tracking・Models・Model Registry・Projects）それぞれの役割と相互関係を説明するページを提供する
2. The Tutorial shall 各コンポーネントのページに、概念説明・コード例・実行結果の3セットを含める
3. When 読者が概念ページを読み終えたとき, the Tutorial shall 次に読むべきページへのナビゲーションリンクを提供する
4. The Tutorial shall MLflow Tracking ServerをローカルでUI付きで起動する手順（`mlflow ui`）を含める

---

### Requirement 2: scikit-learnサンプルセット

**Objective:** As a データサイエンティスト, I want scikit-learnモデルのトレーニングからロギング・登録までを一貫して体験できること, so that 既存のsklearnワークフローにMLflowをどう組み込むか理解できる

#### Acceptance Criteria
1. The Tutorial shall scikit-learn（例: LogisticRegression / RandomForest）を用いたモデルトレーニングとMLflow Trackingへのメトリクス・パラメータ・アーティファクトのロギングを実演するノートブックを提供する
2. The Tutorial shall `mlflow.sklearn.autolog()` を使った自動ロギングと手動ロギングの両方のコード例を含める
3. When モデルトレーニングが完了したとき, the Tutorial shall Model Registryへのモデル登録手順（`mlflow.register_model`）をコード例で示す
4. The Tutorial shall ロギング済みモデルを `mlflow.sklearn.load_model()` でロードして推論する例を含める
5. If sklearn モデルのロギング中にエラーが発生した場合, the Tutorial shall 典型的なトラブルシューティング手順（バージョン確認・run IDの確認等）を説明する

---

### Requirement 3: PyTorchサンプルセット

**Objective:** As a MLエンジニア, I want PyTorchモデルのトレーニングループとMLflow Trackingを組み合わせた実例を学べること, so that ディープラーニングワークフローにMLflowを適用できる

#### Acceptance Criteria
1. The Tutorial shall PyTorchを用いた簡単なニューラルネットワーク（合成データによる回帰または分類）のトレーニングループ内でMLflowにメトリクス（loss・accuracy）をエポックごとにロギングするノートブックを提供する（実行時のデータダウンロードは行わない）
2. The Tutorial shall PyTorchモデルを `mlflow.pytorch.log_model()` でアーティファクトとして保存し、後からロードする手順を含める
3. Where PyTorch Lightning が利用可能な環境では, the Tutorial shall `mlflow.pytorch.autolog()` または MLflowLogger の使用例を補足説明として提供する
4. The Tutorial shall sklearnサンプルとPyTorchサンプルで共通する概念（run・experiment・artifact）を対比しながら説明する

---

### Requirement 4: ハイパーパラメータ最適化・実験比較サンプル

**Objective:** As a MLエンジニア・データサイエンティスト, I want 複数のrunを比較する実験管理ワークフローを体験できること, so that MLflowのExperiment比較機能の実用的な価値を理解できる

#### Acceptance Criteria
1. The Tutorial shall 複数のハイパーパラメータ設定（例: 学習率・深さ・正則化強度）でrunを記録し、MLflow UIで比較する手順を示すノートブックを提供する
2. The Tutorial shall `mlflow.search_runs()` を使ったプログラム上でのrun検索・ソートのコード例を含める
3. When 複数runが記録されたとき, the Tutorial shall MLflow UIの「Compare」機能でメトリクスチャートを並べて確認する操作手順をスクリーンショットまたはコードで説明する

---

### Requirement 5: Jupyter Book形式のドキュメント構成

**Objective:** As a チュートリアル読者, I want ブラウザ上でインタラクティブに読み進められる構成のドキュメントサイトを閲覧できること, so that コードと説明を一体で把握しやすい

#### Acceptance Criteria
1. The Tutorial shall `jupyter-book` でビルド可能な `_toc.yml` と `_config.yml` を含むプロジェクト構成とする
2. The Tutorial shall 全ての実習コードをJupyter Notebook（`.ipynb`）として提供し、Jupyter Book上でレンダリングされる状態にする
3. The Tutorial shall 各ノートブックに「前提条件」「学習目標」「まとめ」のセクションを設ける
4. If ビルド時に依存パッケージが不足している場合, the Tutorial shall `requirements.txt` または `environment.yml` に必要パッケージを明示し、インストールコマンドをREADMEに記載する
5. The Tutorial shall `jupyter-book build .` コマンド1つでローカルビルドが完了する構成とする

---

### Requirement 6: GitHub Pages自動デプロイ

**Objective:** As a チュートリアル管理者, I want mainブランチへのpush時に自動でGitHub Pagesへ公開できること, so that コンテンツ更新の運用コストを最小化できる

#### Acceptance Criteria
1. The Tutorial shall GitHub Actionsワークフロー（`.github/workflows/deploy.yml`）を提供し、mainブランチへのpush時にJupyter Bookをビルドして `gh-pages` ブランチへデプロイする
2. The Tutorial shall GitHub Actions上でノートブックを実行せず、事前実行済みの出力をリポジトリに含める方針（`execute_notebooks: off`）を採用するか、またはキャッシュ戦略を明示する
3. When デプロイが成功したとき, the Tutorial shall GitHub Pagesの公開URLでサイトが閲覧可能になる
4. If GitHub Actionsのビルドが失敗した場合, the Tutorial shall エラーログから原因を特定できるよう、ビルドステップを分割して記録する

---

### Requirement 7: 環境セットアップ・前提条件ガイド

**Objective:** As a MLflowを初めて使う読者, I want ローカル環境の構築手順を迷わず実行できること, so that チュートリアル開始までのハードルを最小化できる

#### Acceptance Criteria
1. The Tutorial shall Python・conda・MLflowのインストール手順と動作確認コマンドを含む「はじめに」ページを提供する
2. The Tutorial shall チュートリアル全体で使用するPythonおよび主要ライブラリのバージョン（MLflow・scikit-learn・PyTorch）を明記する
3. The Tutorial shall MLflow Tracking Serverのローカル起動（`mlflow server` / `mlflow ui`）とサンプルコードの実行に必要な最小限の手順を5ステップ以内で説明する
4. The Tutorial shall ローカル開発環境としてconda仮想環境（`conda create -n mlflow-tutorial python=X.X` / `conda activate mlflow-tutorial`）を標準とし、その手順を「はじめに」ページに記載する
5. The Tutorial shall オフライン環境向けに `conda install --offline` またはcondaローカルチャネル経由でのパッケージインストール手順を補足として提供する（pipのwheel方式も併記可）
6. The Tutorial shall 学習フェーズ（ノートブック実行）はシングルマシン向けにローカルファイルシステム（`mlruns/`）を使用し、デプロイフェーズ（Req 10・11）ではMLflow Tracking Serverを別ホストで起動する2パターンを段階的に説明する

---

### Requirement 8: オフライン動作保証

**Objective:** As a オフライン環境のMLエンジニア・データサイエンティスト, I want パッケージインストール後のノートブック実行をインターネット接続なしで完了できること, so that ネットワーク制限のある企業環境や閉域網でもチュートリアルを利用できる

#### Acceptance Criteria
1. The Tutorial shall 全ノートブックで使用するデータセットをsklearn内蔵データセット（`sklearn.datasets`）またはコード内で生成する合成データ（`numpy`・`torch` での乱数生成）のみに限定し、実行時のダウンロードを行わない
2. The Tutorial shall `torchvision.datasets`・`datasets`（HuggingFace）等のダウンロードを伴うデータセットAPIを使用しない
3. The Tutorial shall 外部インターネットへの接続を一切行わず、内部ネットワーク（MLflow Tracking Server・アプリサーバー間）のみで動作する構成を前提とする
4. If インターネット接続が存在しない環境でノートブックを実行した場合, the Tutorial shall 全セルが正常に完了する
5. The Tutorial shall 外部クラウドサービス（AWS S3・Azure Blob・GCS等）へのアーティファクト保存を使用せず、MLflow Tracking Serverのローカルファイルシステムのみを使用する
6. The Tutorial shall「ネットワーク前提」として、インターネット接続が必要なステップ（初回パッケージインストールのみ）・内部ネットワークが必要なステップ（MLflow Server接続・モデル取得）・完全ローカルで完結するステップを「はじめに」ページで明確に区別して説明する

---

### Requirement 9: チャレンジャー/チャンピオン管理

**Objective:** As a MLエンジニア・データサイエンティスト, I want MLflow Model Registryのエイリアス機能を使って複数モデルバージョンをチャレンジャー/チャンピオンとして管理するワークフローを学べること, so that 本番モデルの安全な更新・ロールバック手順を習得できる

#### Acceptance Criteria
1. The Tutorial shall MLflow Model Registry にモデルを登録し、`MlflowClient.set_registered_model_alias()` を使って `"champion"` および `"challenger"` エイリアスを付与する手順をノートブックで実演する
2. The Tutorial shall チャレンジャーモデルとチャンピオンモデルのメトリクスをプログラム上で比較し（`MlflowClient.search_model_versions()` + `get_run()` によるメトリクス取得）、チャレンジャーが優れる場合にエイリアスを昇格させる（`champion` ← 旧 `challenger`）コード例を含める
3. When チャレンジャーがチャンピオンに昇格したとき, the Tutorial shall 旧チャンピオンのエイリアスを削除または `"archived"` エイリアスへ移行するコードを示す
4. The Tutorial shall `models:/モデル名@champion` 形式のURIでチャンピオンモデルをロードする方法を説明する
5. The Tutorial shall チャンピオン/チャレンジャー管理のライフサイクル（登録→評価→昇格→ロールバック）を図またはフローチャートで示す

---

### Requirement 10: チャンピオンモデルのWebアプリ搭載・サービング

**Objective:** As a MLエンジニア, I want MLflow Model Registryのチャンピオンモデルを最小限のWebアプリに組み込んで推論APIとして提供する構成を学べること, so that モデルのデプロイメントパターンを実務レベルで理解できる

#### Acceptance Criteria
1. The Tutorial shall FastAPIまたはStreamlitを使ったWebアプリのサンプルコード（`app/`ディレクトリ）を提供し、起動時に `models:/モデル名@champion` からモデルを動的にロードする実装を含める
2. The Tutorial shall WebアプリがMLflow Tracking Serverに対して内部ネットワーク経由（例: `http://mlflow-server:5000`）で接続し、チャンピオンモデルを取得する構成を示す
3. The Tutorial shall MLflow Tracking Server・Webアプリサーバーを別々のプロセス（例: 別ターミナル・別仮想環境）または別ホストで起動することを前提とした起動手順書を提供する
4. When チャンピオンモデルのエイリアスが更新されたとき, the Tutorial shall Webアプリ再起動またはエンドポイント経由のモデルリロードによって新チャンピオンを反映する手順を説明する
5. The Tutorial shall Webアプリの推論エンドポイント（例: `POST /predict`）に入力データを送信し、予測結果を返すcurlまたはPythonのリクエスト例を含める
6. If MLflow Tracking Serverへの接続が失敗した場合, the Tutorial shall Webアプリが起動エラーを明示的に出力し、接続先URIの確認手順を示す

---

### Requirement 11: マルチサーバー構成ガイド

**Objective:** As a インフラ担当MLエンジニア, I want MLflow Tracking Serverとアプリサーバーを分離した構成を理解・再現できること, so that 本番環境に近い役割分担で各コンポーネントを運用できる

#### Acceptance Criteria
1. The Tutorial shall 以下の役割分担を図示する: **MLflow Serverホスト**（Tracking Server・Model Registry・アーティファクトストレージ）/ **アプリサーバーホスト**（WebアプリまたはAPIサーバー）
2. The Tutorial shall 個別の起動コマンド（別ターミナルでの `mlflow server` とアプリ起動）を使って2サーバー構成をローカル環境で再現する手順を提供する（外部インターネット接続は不要）
3. The Tutorial shall MLflow Serverの `--host 0.0.0.0` オプションおよびアーティファクトルート（`--default-artifact-root`）の設定を含む起動コマンド例を示す
4. The Tutorial shall アプリサーバー側の環境変数（`MLFLOW_TRACKING_URI`）によってMLflow接続先を設定する方法を説明する
5. While 2サーバーが内部ネットワークで接続されている間, the Tutorial shall アプリサーバーがチャンピオンモデルを正常にロードできることを確認するヘルスチェック手順を示す
