# Research & Design Decisions

---
**Purpose**: 設計判断の根拠となる調査結果・アーキテクチャ評価・リスクを記録する。

---

## Summary

- **Feature**: `mlflow-tutorial`
- **Discovery Scope**: New Feature（グリーンフィールド）
- **Key Findings**:
  - MLflow エイリアス API（`set_registered_model_alias` / `models:/name@alias`）は MLflow 2.8.0 で導入。チュートリアル全体でこのバージョン以上を前提とする
  - Jupyter Book 2.0 は `myst.yml` に移行済みだが、v0.15.x（1.x 系）の `_config.yml` / `_toc.yml` が要件で明示されているため、安定版 0.15.x を採用する
  - FastAPI の lifespan コンテキストマネージャーを使えばアプリ起動時に champion モデルを安全にロードできる。MLflow 2.x の Python クライアントは同期モードで動作するため、lifespan 内で呼び出すのが適切
  - Docker 不使用のマルチサーバー構成は、別ターミナルでの `mlflow server` + `uvicorn` 起動という2プロセス構成で再現する
  - conda オフラインチャンネルは `conda index` でローカル repodata を生成し `conda install -c file:///path/to/channel` でインストールする

## Research Log

### MLflow Model Registry エイリアス API

- **Context**: Req 9 でチャンピオン/チャレンジャー管理に使用するため API を確認
- **Sources Consulted**:
  - MLflow 2.8.0 リリースノート (https://mlflow.org/news/2023/10/29/2.8.0-release/)
  - MLflow Python API リファレンス (https://mlflow.org/docs/latest/python_api/mlflow.client.html)
  - MLflow モデルロードガイド (https://mlflow.org/docs/latest/getting-started/registering-first-model/step3-load-model/)
- **Findings**:
  - `MlflowClient.set_registered_model_alias(name: str, alias: str, version: str) -> None`
  - `MlflowClient.get_model_version_by_alias(name: str, alias: str) -> ModelVersion`
  - ロードURIは `models:/モデル名@エイリアス名` 形式
  - 1 バージョンに複数エイリアスを付与可能（旧 Stages とは異なり柔軟）
  - エイリアス削除: `MlflowClient.delete_registered_model_alias(name, alias)`
- **Implications**: チュートリアルで使用する MLflow バージョンは **2.8.0 以上**に固定する。`pip install mlflow>=2.8.0` を requirements に明記する

### Jupyter Book バージョン選定

- **Context**: Req 5 が `_config.yml` / `_toc.yml` を明示しているため、対応バージョンを確認
- **Sources Consulted**:
  - Jupyter Book 公式サイト (https://jupyterbook.org/)
  - MyST Markdown 実行ガイド (https://mystmd.org/guide/execute-notebooks)
- **Findings**:
  - Jupyter Book 2.0（2025年初頭リリース）は `myst.yml` に完全移行し `_config.yml` / `_toc.yml` を廃止
  - Jupyter Book 0.15.x（1.x 系）が `_config.yml` + `_toc.yml` をサポートする最後の安定版
  - `execute_notebooks: off` の設定キーは `_config.yml` の `execute` セクションに記述
  - v2 へのアップグレードは `jupyter book build` 実行時に自動移行プロンプトが出る
- **Implications**: **Jupyter Book 0.15.x を採用**。v2 への移行パスは「発展的な話題」として補足説明に留める

### GitHub Actions による GitHub Pages デプロイ

- **Context**: Req 6 の自動デプロイワークフロー設計
- **Sources Consulted**: Jupyter Book GitHub Pages ガイド (https://jupyterbook.org/en/stable/publish/gh-pages.html)
- **Findings**:
  - 標準フロー: ① パッケージインストール → ② `jupyter-book build .` → ③ `ghp-import` または `actions/deploy-pages` でデプロイ
  - `execute_notebooks: off` を `_config.yml` に設定することで CI 上でのノートブック再実行を回避
  - ノートブックの出力はリポジトリにコミット済みとして扱う（pre-executed 方式）
- **Implications**: `execute_notebooks: "off"` を `_config.yml` に明記し、開発者はローカルでノートブックを実行してから `git commit` する運用とする

### FastAPI + MLflow モデルサービング

- **Context**: Req 10 のチャンピオンモデル推論 API 設計
- **Sources Consulted**: FastAPI lifespan イベントドキュメント (https://fastapi.tiangolo.com/advanced/events/)
- **Findings**:
  - FastAPI 0.93+ の `lifespan` コンテキストマネージャーがモデルロードに最適（旧 `@app.on_event("startup")` より推奨）
  - MLflow Python クライアントは同期 API のみ提供。`asyncio.to_thread()` を使えば非同期ハンドラーからも安全に呼び出せる
  - MLflow 2.x に PR #14307（2025年1月）で FastAPI ベースのサーバーが追加されたが、`mlflow models serve` コマンド向けであり、カスタム FastAPI アプリとは別物
- **Implications**: アプリ起動時に `lifespan` でモデルをロードし、`app.state.model` に格納してハンドラーから参照するパターンを採用する

### conda オフラインインストール

- **Context**: Req 7・8 のオフライン環境セットアップ
- **Sources Consulted**: conda カスタムチャンネルドキュメント (https://docs.conda.io/projects/conda/en/stable/user-guide/tasks/create-custom-channels.html)
- **Findings**:
  - ローカルチャンネルの構造: プラットフォームごとのサブディレクトリ（`linux-64/`, `osx-arm64/` 等）
  - `conda index /path/to/channel` で `repodata.json` を生成
  - `conda install -c file:///path/to/channel パッケージ名` または `conda install -c ./my-channel パッケージ名`
  - pip の代替: `pip download -r requirements.txt -d ./wheels` → `pip install --no-index --find-links=./wheels -r requirements.txt`
- **Implications**: チュートリアルでは **pip wheel 方式をメイン**（シンプルで conda 依存なし）、conda channel 方式を補足として説明する

### Optuna + MLflow 統合パターン

- **Context**: Req 4 でハイパーパラメータ最適化に Optuna を統合するため設計を調査
- **Findings**:
  - Optuna の `objective` 関数内で `mlflow.start_run(nested=True)` を呼ぶことで trial ごとに子 run を作成できる
  - `parent_run` で `study.optimize()` 全体を囲むと MLflow UI で study → trial の階層表示が可能
  - `TPESampler` はデフォルトで `seed` を固定可能（`TPESampler(seed=42)`）→ 再現性確保
  - `study.best_trial.number` から best trial の MLflow run ID を `search_runs()` で逆引きできる
  - Optuna は外部サービスに依存しない純粋 Python ライブラリ。オフライン動作と完全に整合する
- **Implications**: `nested=True` パターンを標準とし、study 全体を1つの親 run で管理する設計を採用する

## Architecture Pattern Evaluation

| Option | 説明 | 強み | 制約 / リスク | 採用可否 |
|--------|------|------|--------------|---------|
| シングルプロセス（ファイルベース） | `./mlruns` をそのまま使い、Webアプリと同プロセス内でモデルロード | セットアップ最小 | ファイルパス依存・マルチサーバー構成に拡張できない | 学習フェーズのみで採用 |
| 2プロセス（ネットワーク経由） | `mlflow server` を別ターミナルで起動し、アプリは `MLFLOW_TRACKING_URI` で接続 | 本番構成に近い・役割分担が明確 | セットアップ手順が増える | デプロイフェーズで採用 |
| Docker Compose | コンテナで役割分担 | 再現性最高 | Docker 使用不可 | **不採用** |

## Design Decisions

### Decision: Jupyter Book バージョンを 0.15.x に固定する

- **Context**: v2.0 が最新だが、要件が `_config.yml` / `_toc.yml` を明示
- **Alternatives Considered**:
  1. Jupyter Book 0.15.x（1.x 系）— `_config.yml` + `_toc.yml`
  2. Jupyter Book 2.0（MyST）— `myst.yml`
- **Selected Approach**: 0.15.x を採用し、バージョンを `requirements.txt` に `jupyter-book>=0.15,<1.0` で固定
- **Rationale**: 要件の記述と一致し、ドキュメントや事例が豊富。v2 への移行は今後の拡張として扱う
- **Trade-offs**: v2 の新機能は使えないが、チュートリアルの目的（MLflow 学習）には十分

### Decision: Webアプリフレームワークを FastAPI に決定する

- **Context**: Req 10 が「FastAPI または Streamlit」と提示
- **Alternatives Considered**:
  1. FastAPI — REST API、`POST /predict`、`GET /health`
  2. Streamlit — GUI ダッシュボード形式
- **Selected Approach**: FastAPI を primary、Streamlit を補足サンプルとして位置づける
- **Rationale**: `POST /predict` の REST エンドポイントがマルチサーバー構成・curl テストと相性が良い。Streamlit は UI 確認用として参考に残す
- **Trade-offs**: FastAPI は uvicorn の起動が必要で Streamlit より手順が多い。ただし本番デプロイパターンとして教育的価値が高い

### Decision: ノートブック実行方式を pre-executed（出力コミット）に固定する

- **Context**: Req 6.2 の CI 上での再実行回避とオフライン運用の両立
- **Alternatives Considered**:
  1. pre-executed — ローカルで実行した出力を `.ipynb` にコミット
  2. CI 実行 — GitHub Actions 上でノートブックを実行
- **Selected Approach**: pre-executed 方式。`_config.yml` に `execute_notebooks: "off"` を設定
- **Rationale**: オフライン環境での MLflow サーバー依存・データセット依存を CI 上で解決する必要がなくなる。CI はビルド（HTML 変換）のみに集中できる
- **Trade-offs**: 開発者がノートブック出力を最新に保つ責任を持つ必要がある

## Risks & Mitigations

- **MLflow バージョン非互換** — エイリアス API は 2.8.0 以降。`environment.yml` でバージョンを `mlflow>=2.8.0` と明示し、古い環境でのエラーメッセージを「はじめに」ページに記載する
- **ノートブック出力の陳腐化** — pre-executed 方式では出力が古くなるリスクがある。README に「ノートブック更新時は再実行してコミットすること」を明記する
- **マルチサーバー間の接続失敗** — `MLFLOW_TRACKING_URI` の設定ミスが最多原因。Webアプリの起動時ヘルスチェックでエラーを早期検出し、接続先 URI を標準出力に表示する
- **PyTorch の合成データ生成の再現性** — `torch.manual_seed()` を全ノートブックで設定して出力を固定する

## References

- [MLflow 2.8.0 リリースノート](https://mlflow.org/news/2023/10/29/2.8.0-release/) — エイリアス機能の導入バージョン確認
- [MLflow MlflowClient API](https://mlflow.org/docs/latest/python_api/mlflow.client.html) — `set_registered_model_alias` シグネチャ
- [Jupyter Book 公式](https://jupyterbook.org/en/stable/) — `_config.yml` / `_toc.yml` 構成
- [FastAPI Lifespan Events](https://fastapi.tiangolo.com/advanced/events/) — モデルロードパターン
- [conda Custom Channels](https://docs.conda.io/projects/conda/en/stable/user-guide/tasks/create-custom-channels.html) — オフラインインストール手順
