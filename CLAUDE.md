# TinyRAG プロジェクト構成とガイドライン

## 🎯 プロジェクト概要

TinyRAGは、軽量なRAGシステムの実装です。llama-cpp-pythonとsqlite-vecを中心に、必要最小限の依存関係で高性能なRAG機能を提供します。

### 主な特徴
- 軽量で高速な実装
- 複数の埋め込みモデル対応（sentence-transformers / llama-cpp）
- Windows/macOS/Linux対応
- ランキング、クエリ、LLM回答機能を統合
- 多言語対応（英語、日本語、タイ語）
- uvを使用したモダンなPythonプロジェクト管理

## 📁 プロジェクト構造

```
tinyrag/
├── pyproject.toml       # プロジェクト設定とuv依存関係管理
├── uv.lock             # uv依存関係ロックファイル
├── requirements.txt    # pip互換の依存関係
├── llm.py              # LLMモデルの管理（Llama-3.2-1B）
├── database.py         # SQLiteベクトルデータベース操作
├── embedding.py        # 埋め込みモデル（ruri-v3-310m/bge-m3切り替え対応）
├── reranker.py         # リランキングモデル（bge-reranker-v2-m3）
├── search.py           # RAGシステムの実装例
├── config.py           # 言語設定、多言語対応、埋め込みモデル設定
├── wiki_app.py         # Wikipedia RAGデモアプリ（Gradio UI）
├── wiki_create-db.py   # Wikipediaデータベース作成
├── thailaw_app.py      # タイ法律RAGデモアプリ
├── thailaw_create-db.py # タイ法律データベース作成
├── wiki.db / wiki_.db  # 生成されたWikipediaデータベース
└── README.md / LICENSE # プロジェクトドキュメント
```

## 🔧 技術スタック

### 依存関係管理
- **uv**: モダンなPythonパッケージマネージャー（推奨）
- **pip**: 従来のパッケージマネージャー（requirements.txt対応）
- **Python**: >=3.13

### 主要ライブラリ
- **gradio**: Web UI フレームワーク（>=5.39.0）
- **sentence-transformers**: 日本語特化埋め込みモデル対応（>=5.0.0）
- **llama-cpp-python**: GGUF形式モデル実行（>=0.3.7）
- **sqlite-vec**: ベクトル検索用SQLite拡張（>=0.1.6）
- **datasets / huggingface-hub**: モデル・データセット管理
- **torch**: PyTorchフレームワーク（>=2.0.0）
- **numpy**: 数値計算ライブラリ（>=1.26.0）

### モデル
- **LLM**: Llama-3.2-1B-Instruct (Q4_K_S量子化)
- **Embedding**: 
  - **デフォルト**: cl-nagoya/ruri-v3-310m（日本語特化、310M）
  - **代替**: bge-m3 (Q4_K_M量子化、多言語)
- **Reranker**: bge-reranker-v2-m3 (Q4_K_M量子化)

### データベース
- **sqlite-vec**: ベクトル検索用SQLite拡張
- **次元数**: 1024次元の埋め込みベクトル

## 💻 開発ガイドライン

### コーディング規約
1. **インポート順序**: 標準ライブラリ → サードパーティ → ローカルモジュール
2. **エラーハンドリング**: データベース操作時は必ずトランザクション管理
3. **型ヒント**: 可能な限り型アノテーションを使用
4. **GPU設定**: `n_gpu_layers=-1`でGPU全使用、GPUなしの場合は`0`

### 新機能追加時の注意点
1. **言語対応**: 新しいプロンプトは`config.py`の`LanguageConfig`に追加
   - デフォルト言語は英語（`DEFAULT_LANGUAGE = "en"`）
   - 日本語（ja）、タイ語（th）、英語（en）対応
2. **埋め込みモデル設定**: `config.py`の`EmbeddingConfig`クラスで管理
   - 環境変数 `EMBEDDING_MODEL_TYPE`、`EMBEDDING_MODEL_NAME`で動的切り替え
   - 対応モデル: sentence-transformers（ruri-v3-310m等）、llama-cpp（bge-m3）
3. **ruri-v3-310m使用時**: 日本語プレフィックス（"検索文書: " / "検索クエリ: "）必須
4. **データベース拡張**: `Database`クラスを継承して機能追加
5. **依存関係**: 新しいライブラリは`pyproject.toml`に追加
6. **会話履歴処理**: Gradio UIでのrole交互パターンを維持（user/assistant/user...）

### テスト方針
- 各モジュール（llm.py、database.py、embedding.py、reranker.py）は独立してテスト可能
- 統合テストは`search.py`をベースに実装
- デモアプリ（wiki_app.py、thailaw_app.py）でエンドツーエンドテスト

## 🚀 よく使うコマンド

### セットアップ

```bash
# uv を使用（推奨）
uv sync

# または従来の pip
pip install -r requirements.txt
```

### データベース作成

```bash
# デフォルト（sentence-transformers + ruri-v3-310m）でWikipediaデータベース作成
python wiki_create-db.py

# llama-cpp + bge-m3でWikipediaデータベース作成
EMBEDDING_MODEL_TYPE=llama-cpp EMBEDDING_MODEL_NAME=bge-m3 python wiki_create-db.py

# タイ法律データベース作成
python thailaw_create-db.py
```

### アプリ起動

```bash
# Wikipediaデモ起動（Gradio UI）
python wiki_app.py

# タイ法律デモ起動
python thailaw_app.py

# uvを使用してスクリプト実行
uv run python wiki_app.py
```

### 埋め込みモデルの切り替え

環境変数で埋め込みモデルを動的に切り替えできます：

```bash
# sentence-transformers + ruri-v3-310m（日本語特化、デフォルト）
export EMBEDDING_MODEL_TYPE=sentence-transformers
export EMBEDDING_MODEL_NAME=ruri-v3-310m

# llama-cpp + bge-m3（多言語対応）
export EMBEDDING_MODEL_TYPE=llama-cpp
export EMBEDDING_MODEL_NAME=bge-m3

# その他のsentence-transformers対応モデル
export EMBEDDING_MODEL_TYPE=sentence-transformers
export EMBEDDING_MODEL_NAME=intfloat/multilingual-e5-base
# または
export EMBEDDING_MODEL_NAME=BAAI/bge-m3

# 一時的な設定でアプリ起動
EMBEDDING_MODEL_TYPE=llama-cpp EMBEDDING_MODEL_NAME=bge-m3 python wiki_app.py
```

### 設定管理（config.py）

```python
# 埋め込みモデル情報を取得
from config import EmbeddingConfig
model_info = EmbeddingConfig.get_model_info()
print(f"Type: {model_info['type']}, Name: {model_info['name']}")

# 言語設定を変更
from config import LanguageConfig
LanguageConfig.set_default_language("ja")  # 日本語に変更
```

### 重要な注意点

- **ruri-v3-310m**: 日本語プレフィックス（"検索文書: " / "検索クエリ: "）が必須
- **bge-m3**: 多言語対応でプレフィックス不要
- 埋め込みモデル変更時は、データベースを再作成する必要があります

## ⚠️ 注意事項

1. **メモリ使用量**: モデルロード時に数GBのメモリを使用
2. **初回実行**: モデルファイルのダウンロードに時間がかかる
3. **スレッドセーフティ**: `Database`クラスは`check_same_thread=False`で初期化
4. **文字コード**: すべてUTF-8で統一

## 🔍 デバッグのヒント

- **埋め込み確認**: `get_embedding()`の出力は`["data"][0]['embedding']`にアクセス
- **リランキングスコア**: 0以上が関連文書、負の値は無関係
- **SQLiteエラー**: sqlite-vec拡張のロードを確認
- **GPU利用**: `n_gpu_layers`パラメータを調整
- **モデル選択**: 環境変数`EMBEDDING_MODEL_TYPE`、`EMBEDDING_MODEL_NAME`で確認
- **ruri-v3-310m問題**: 日本語プレフィックスが正しく付加されているか確認
- **uvエラー**: `uv sync`で依存関係を再同期
- **Gradio会話エラー**: 「Conversation roles must alternate」エラーは`wiki_app.py`のrole順序問題
- **言語設定**: `LanguageConfig.DEFAULT_LANGUAGE`でデフォルト言語を確認
- **設定クラス**: `EmbeddingConfig.get_model_info()`で現在のモデル設定を確認

## 📝 TODO/改善案

- [ ] バッチ処理対応でパフォーマンス向上
- [ ] キャッシュ機能の実装
- [ ] より詳細なロギング機能
- [ ] Web UIの改善（Gradio UIの更なる機能追加）
- [ ] ドキュメントチャンク分割の最適化
- [ ] 他のsentence-transformersモデル対応拡張
- [ ] テストスイートの実装
- [ ] CI/CD パイプラインの構築
- [ ] 設定ファイル（YAML/JSON）による設定管理
- [ ] APIエンドポイントの実装（FastAPI等）
- [ ] ベクトルデータベースの永続化最適化

## 🔧 最新の変更履歴

### 2024年12月 主要更新
- ✅ `EmbeddingConfig`クラス追加: 埋め込みモデルの動的切り替え対応
- ✅ `LanguageConfig`の日本語対応強化: 適切な日本語プロンプト・エラーメッセージ
- ✅ Gradio UIの会話履歴処理改善: role交互パターンエラー修正
- ✅ 依存関係更新: pyproject.toml準拠、最新バージョン対応
- ✅ 多言語プロンプトテンプレート充実: 英語・日本語・タイ語対応