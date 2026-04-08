# はじめに

MLflow Tutorial へようこそ。本チュートリアルは MLflow を初めて使う ML エンジニア・データサイエンティストを対象に、MLflow の全体像から実務レベルのモデル管理・サービングまでを段階的に学べるコンテンツを提供します。

## ネットワーク前提

本チュートリアルの各ステップに必要なネットワーク環境を以下に整理します。

| ステップ | 必要なネットワーク |
|--------|-----------------|
| パッケージインストール（初回のみ） | **インターネット接続が必要** |
| ノートブック実行（学習フェーズ） | **完全ローカルで完結**（接続不要） |
| MLflow Server 起動・接続（デプロイフェーズ） | **内部ネットワークのみ**（同一マシン内または LAN） |

---

## 使用バージョン

| ライブラリ | バージョン |
|---------|---------|
| Python | 3.11 |
| MLflow | >= 2.8.0 |
| scikit-learn | 最新安定版 |
| PyTorch | 最新安定版 |
| Optuna | 最新安定版 |
| FastAPI | 最新安定版 |

---

## 環境セットアップ（5ステップ）

### ステップ 1: conda のインストール確認

```bash
conda --version
```

### ステップ 2: 仮想環境の作成

```bash
conda create -n mlflow-tutorial python=3.11
conda activate mlflow-tutorial
```

### ステップ 3: パッケージのインストール

**オンライン環境（推奨）**:

```bash
conda env create -f environment.yml
conda activate mlflow-tutorial
```

**オフライン環境（pip wheel 方式）**:

```bash
# オンライン環境で事前ダウンロード
pip download -r requirements.txt -d ./wheels

# オフライン環境でインストール
pip install --no-index --find-links=./wheels -r requirements.txt
```

**オフライン環境（conda channel 方式）**:

```bash
conda index ./local-channel
conda install -c file:///path/to/local-channel --offline パッケージ名
```

### ステップ 4: インストール確認

```bash
mlflow --version
python -c "import sklearn; print(sklearn.__version__)"
python -c "import torch; print(torch.__version__)"
```

### ステップ 5: MLflow UI の起動確認

```bash
mlflow ui
# ブラウザで http://localhost:5000 を開く
```

---

## 学習フェーズとデプロイフェーズ

本チュートリアルは 2 つのフェーズで構成されています。

### Phase 1: シングルマシン学習モード

ノートブック実行時は MLflow がローカルファイルシステム（`./mlruns`）に記録します。MLflow Server のセットアップは不要です。

```python
import mlflow
mlflow.set_tracking_uri("./mlruns")
```

### Phase 2: マルチサーバーモード（デプロイ）

デプロイフェーズでは MLflow Tracking Server と FastAPI Web アプリを別プロセスで起動します。

**ターミナル 1（MLflow Server）**:
```bash
mlflow server --host 0.0.0.0 --default-artifact-root ./mlartifacts --port 5000
```

**ターミナル 2（FastAPI アプリ）**:
```bash
MLFLOW_TRACKING_URI=http://localhost:5000 MODEL_NAME=MyModel \
  uvicorn app.main:app --port 8000
```

アプリ側は環境変数 `MLFLOW_TRACKING_URI` で接続先を切り替えます（クラウドストレージは使用しません）。

---

## チュートリアルの構成

1. **{doc}`notebooks/01_concepts/mlflow_overview`** — MLflow の 4 コンポーネント概要
2. **{doc}`notebooks/02_sklearn/sklearn_autolog`** — scikit-learn サンプル（autolog・手動ログ・Model Registry）
3. **{doc}`notebooks/03_pytorch/pytorch_tracking`** — PyTorch サンプル（トレーニングループ・ログ・モデル保存）
4. **{doc}`notebooks/04_experiment_management/hyperparam_search`** — Optuna HPO + 実験比較
5. **{doc}`notebooks/05_champion_challenger/champion_challenger`** — チャンピオン/チャレンジャー管理
6. **{doc}`notebooks/06_deployment/fastapi_serving`** — FastAPI によるモデルサービング
