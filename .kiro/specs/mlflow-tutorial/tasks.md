# Implementation Plan

## Task Overview

本チュートリアルの実装は、プロジェクト基盤の構築を起点に、各ノートブックを並行して実装し、最後にデプロイ設定で統合する構成とする。

---

- [x] 1. プロジェクト基盤と環境設定の構築
- [x] 1.1 (P) conda仮想環境定義ファイルの作成
  - `environment.yml` に `python=3.11`・`mlflow>=2.8.0`・`scikit-learn`・`torch`・`optuna`・`fastapi`・`uvicorn`・`jupyter-book>=0.15,<1.0`・`pydantic>=2.0` を定義する
  - `requirements.txt` を pip 形式で出力する
  - `README.md` にオンライン環境向けの `conda env create -f environment.yml` とオフライン環境向けの pip wheel 方式・conda channel 方式のインストールコマンドを記載する
  - _Requirements: 5.4, 7.1, 7.2, 7.4, 7.5_

- [x] 1.2 (P) Jupyter Book設定ファイルの作成
  - `_config.yml` に `title`・`author`・`execute_notebooks: "off"`・`myst_enable_extensions: ["colon_fence"]` を定義する
  - `_toc.yml` に `intro` を root として `notebooks/01_concepts/`・`notebooks/02_sklearn/`・`notebooks/03_pytorch/`・`notebooks/04_experiment_management/`・`notebooks/05_champion_challenger/`・`notebooks/06_deployment/` の章構成を定義する
  - `jupyter-book build .` 一コマンドでローカルビルドが完了する構成にする
  - 全ての実習コードを `.ipynb` として提供し Jupyter Book 上でレンダリングされる状態にする
  - _Requirements: 5.1, 5.2, 5.5_

- [x] 1.3 「はじめに」ページと環境セットアップガイドの実装
  - Python・conda・MLflow のインストール手順と動作確認コマンド（`mlflow --version` 等）を記述する
  - チュートリアル全体で使用する MLflow・scikit-learn・PyTorch の具体的バージョンを明記する
  - MLflow Tracking Server のローカル起動（`mlflow ui`）からサンプルコード実行までの手順を 5 ステップ以内で説明する
  - conda 仮想環境の作成（`conda create -n mlflow-tutorial python=3.11`）とアクティベート手順を標準手順として記載する
  - オフラインインストール手順（pip wheel 方式・conda channel 方式）を補足として提供する
  - Phase 1（シングルマシン・ローカルファイルシステム `./mlruns`）と Phase 2（別ホスト MLflow Server・`MLFLOW_TRACKING_URI`）の 2 パターンを段階的に説明する
  - 「インターネット接続が必要なステップ（初回パッケージインストールのみ）」「内部ネットワークが必要なステップ（MLflow Server 接続）」「完全ローカルで完結するステップ」をネットワーク前提として区別して説明する
  - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5, 7.6, 8.6_

---

- [x] 2. (P) MLflowコア概念説明ノートブックの実装
- [x] 2.1 4コンポーネント説明コンテンツの実装
  - Tracking・Models・Model Registry・Projects それぞれの役割と相互関係を説明するセルを実装する
  - 各コンポーネントに「概念説明」「コード例」「実行結果」の 3 セットを含める
  - ノートブック先頭に「前提条件」「学習目標」、末尾に「まとめ」のセクションを設ける
  - 次に読むべきページへのナビゲーションリンクを Markdown で提供する
  - _Requirements: 1.1, 1.2, 1.3, 5.3_

- [x] 2.2 MLflow UI起動手順の実装
  - `mlflow ui` コマンドでローカル Tracking Server の UI を起動する手順をコードセルと Markdown で説明する
  - UI でのラン一覧・メトリクス確認方法をスクリーンショットまたはコードで示す
  - _Requirements: 1.4_

---

- [x] 3. (P) scikit-learnサンプルノートブックの実装
- [x] 3.1 autologと手動ログの実装
  - scikit-learn（LogisticRegression または RandomForest）でモデルをトレーニングし、`mlflow.sklearn.autolog()` による自動ロギングのコード例を実装する
  - `log_params` / `log_metrics` / `log_model` を手動で呼ぶ手動ロギングのコード例も実装する
  - `sklearn.datasets` の内蔵データセットのみを使用し、実行時のダウンロードを一切行わない
  - `np.random.seed()` でシードを設定して結果を再現可能にする
  - ノートブック先頭に「前提条件」「学習目標」、末尾に「まとめ」のセクションを設ける
  - _Requirements: 2.1, 2.2, 5.3, 8.1, 8.3, 8.4_

- [x] 3.2 Model Registry登録とモデルロードの実装
  - `mlflow.register_model()` で Model Registry へのモデル登録手順をコード例で実装する
  - `mlflow.sklearn.load_model()` でモデルをロードして推論する例を実装する
  - _Requirements: 2.3, 2.4_

- [x] 3.3 トラブルシューティング手順の実装
  - ロギング中の典型的エラー（バージョン確認・run ID 確認・Experiment 設定確認等）のトラブルシューティング手順をノートブック内に記載する
  - _Requirements: 2.5_

---

- [x] 4. (P) PyTorchサンプルノートブックの実装
- [x] 4.1 トレーニングループとエポックごとのメトリクスロギングの実装
  - `torch` の乱数生成による合成データ（回帰または分類）で簡単なニューラルネットワークを定義・実装する
  - トレーニングループ内で loss・accuracy をエポックごとに `mlflow.log_metric(key, value, step=epoch)` でロギングする
  - `torch.manual_seed()` をノートブック先頭で設定して出力を再現可能にする
  - `torchvision.datasets` 等のダウンロードを伴うデータセット API を使用しない
  - sklearn サンプルと PyTorch サンプルで共通する概念（run・experiment・artifact）を対比しながら説明するセルを追加する
  - ノートブック先頭に「前提条件」「学習目標」、末尾に「まとめ」のセクションを設ける
  - _Requirements: 3.1, 3.4, 5.3, 8.1, 8.2, 8.3, 8.4_

- [x] 4.2 mlflow.pytorch.log_modelによるモデル保存とロードの実装
  - `mlflow.pytorch.log_model()` でモデルをアーティファクトとして保存し、後からロードする手順を実装する
  - PyTorch Lightning 利用可能環境向けに `mlflow.pytorch.autolog()` または `MLflowLogger` の使用例を補足説明として追加する
  - _Requirements: 3.2, 3.3_

---

- [x] 5. (P) Optuna HPO・実験比較ノートブックの実装
- [x] 5.1 Optuna + MLflow Tracking統合の実装
  - `study.optimize()` のコールバック内で `mlflow.start_run(nested=True)` を呼び出し、trial ごとに 1 MLflow run を作成するコードを実装する
  - `TPESampler(seed=42)` を使用し、`trial.suggest_float` / `trial.suggest_int` / `trial.suggest_categorical` の探索空間設定例を含める
  - `sklearn.datasets` の内蔵データセットのみを使用し、実行時の外部接続を一切行わない
  - ノートブック先頭に「前提条件」「学習目標」、末尾に「まとめ」のセクションを設ける
  - _Requirements: 4.1, 4.5, 4.6, 5.3, 8.1, 8.3, 8.4_

- [x] 5.2 run検索・比較・ベストモデル登録の実装
  - `mlflow.search_runs()` を使ったプログラム上での run 検索・スコア順ソートのコード例を実装する
  - MLflow UI の「Compare」機能でメトリクスチャートを並べて確認する操作手順を説明する（スクリーンショットまたはコード）
  - `study.best_trial` からベストパラメータを取得し、対応する run ID から `mlflow.register_model()` でモデルを Model Registry に登録する手順を実装する
  - _Requirements: 4.2, 4.3, 4.4_

---

- [x] 6. チャンピオン/チャレンジャー管理ノートブックの実装
- [x] 6.1 エイリアスAPIを使ったモデル登録とエイリアス付与の実装
  - MLflow 2.8.0 以降の `MlflowClient.set_registered_model_alias()` を使って `"champion"` および `"challenger"` エイリアスを付与する手順をノートブックで実装する
  - `models:/モデル名@champion` 形式の URI でチャンピオンモデルをロードする方法を実装する
  - チャンピオン/チャレンジャー管理のライフサイクル（登録 → 評価 → 昇格 → ロールバック）をフローチャートまたは Markdown の図で示す
  - ノートブック先頭に「前提条件」「学習目標」、末尾に「まとめ」のセクションを設ける
  - _Requirements: 9.1, 9.4, 9.5, 5.3_

- [x] 6.2 昇格ロジックとロールバック手順の実装
  - `MlflowClient.search_model_versions()` と `get_run()` でチャレンジャー/チャンピオンのメトリクスをプログラム上で比較するコードを実装する
  - チャレンジャーが優秀な場合に `@champion` エイリアスを新バージョンに更新し、旧チャンピオンを `@archived` エイリアスへ移行するコードを実装する
  - `get_model_version_by_alias()` で昇格後のエイリアスが正しく更新されていることを確認するアサーション例を含める
  - _Requirements: 9.2, 9.3_

---

- [x] 7. FastAPI Webアプリの実装
- [x] 7.1 lifespanによるチャンピオンモデルロードの実装
  - `MLFLOW_TRACKING_URI` と `MODEL_NAME` 環境変数で MLflow 接続先を設定する `app/main.py` を実装する
  - lifespan コンテキストマネージャーで起動時に `@champion` モデルをロードして `app.state.model` に保持する
  - MLflow Server 未起動・モデル未登録・エイリアス未設定の場合に明確なエラーメッセージを出力してプロセスを終了するエラーハンドリングを実装する
  - FastAPI アプリは MLflow Server と別プロセスで起動する構成とする
  - _Requirements: 10.1, 10.2, 10.6_

- [x] 7.2 /predictおよび/healthエンドポイントの実装
  - Pydantic v2 で `PredictRequest` / `PredictResponse` / `HealthResponse` データモデルを定義する
  - `POST /predict` エンドポイントで `asyncio.to_thread()` を使い、同期 `model.predict()` をイベントループをブロックせずに実行する
  - `GET /health` エンドポイントで MLflow 接続状態・モデル名・バージョンを返す
  - curl または Python リクエスト例をノートブックまたはコメントに含める
  - _Requirements: 10.3, 10.5_

- [x] 7.3 マルチサーバー構成ガイドの実装
  - MLflow サーバーホスト（Tracking Server・Model Registry・アーティファクトストレージ）とアプリサーバーホスト（FastAPI）の役割分担を図示するセルまたは Markdown を実装する
  - `mlflow server --host 0.0.0.0 --default-artifact-root ./mlartifacts` と `MLFLOW_TRACKING_URI=http://localhost:5000 MODEL_NAME=MyModel uvicorn app.main:app --port 8000` の別ターミナル起動コマンド例を記載する
  - アプリサーバー側の `MLFLOW_TRACKING_URI` 環境変数による接続先設定方法を説明する
  - 2 サーバー接続中にチャンピオンモデルが正常ロードできることを確認するヘルスチェック手順（`GET /health` 呼び出し）を示す
  - チャンピオンエイリアス更新後の Webアプリ再起動による新チャンピオン反映手順を説明する
  - 外部インターネット接続不要でローカル環境に 2 サーバー構成を再現できることを確認する
  - クラウドストレージ（S3・Azure Blob・GCS 等）を使用せずローカルファイルシステムのみを使用することを明示する
  - _Requirements: 10.4, 11.1, 11.2, 11.3, 11.4, 11.5, 8.5_

---

- [x] 8. (P) GitHub Actions CI/CDワークフローの構築
  - `push` to `main` をトリガーに Jupyter Book をビルドして `gh-pages` ブランチへデプロイする `.github/workflows/deploy.yml` を実装する
  - `execute_notebooks: "off"` の設定のもと、事前実行済みノートブックの出力を HTML 変換するのみとする
  - checkout → Python setup → 依存インストール → `jupyter-book build .` → `peaceiris/actions-gh-pages@v3` によるデプロイのステップを分割して記録し、失敗時に原因を特定できる構成にする
  - デプロイ成功後に GitHub Pages の公開 URL でサイトが閲覧可能になることを確認する
  - _Requirements: 6.1, 6.2, 6.3, 6.4_
