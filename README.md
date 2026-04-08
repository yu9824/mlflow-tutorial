# MLflow Tutorial

MLflow を初めて使う ML エンジニア・データサイエンティスト向けのチュートリアルコンテンツです。

## 環境セットアップ

### オンライン環境（推奨）

```bash
conda env create -f environment.yml
conda activate mlflow-tutorial
```

### オフライン環境（pip wheel 方式）

```bash
# オンライン環境で wheel を事前ダウンロード
pip download -r requirements.txt -d ./wheels

# オフライン環境でインストール
pip install --no-index --find-links=./wheels -r requirements.txt
```

### オフライン環境（conda channel 方式）

```bash
# ローカルチャネルを作成
conda index ./local-channel

# オフラインでインストール
conda install -c file:///path/to/local-channel --offline パッケージ名
```

## チュートリアルのビルド

```bash
conda activate mlflow-tutorial
jupyter-book build .
```

生成された `_build/html/index.html` をブラウザで開いてください。

## 章構成

1. はじめに（環境セットアップ）
2. MLflow コア概念
3. scikit-learn サンプル
4. PyTorch サンプル
5. ハイパーパラメータ最適化（Optuna）
6. チャンピオン/チャレンジャー管理
7. FastAPI によるモデルサービング
