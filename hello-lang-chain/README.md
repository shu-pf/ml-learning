# hello-lang-chain

LangChainを使用した簡単なエージェントの例です。

## セットアップ

1. 依存関係のインストール（既にインストール済み）:
```bash
uv sync
```

2. 環境変数の設定:
実際のLLMモデルを使用するには、以下のいずれかのAPIキーを設定してください:

- OpenAIを使用する場合:
```bash
export OPENAI_API_KEY="your-api-key"
```

- Anthropicを使用する場合:
```bash
export ANTHROPIC_API_KEY="your-api-key"
```

## 実行方法

```bash
uv run main.py
```

## 機能

このプロジェクトには以下のツールを持つエージェントが含まれています:

1. **計算ツール (`calculate`)**: 数式を計算します
2. **天気ツール (`get_weather`)**: 指定された都市の天気情報を返します（デモ用）

## カスタマイズ

`main.py`の`create_agent`関数でモデル名を変更できます:

- OpenAI: `"gpt-4o"` または `"gpt-3.5-turbo"`
- Anthropic: `"claude-sonnet-4-5-20250929"`
- ローカルモデル（Ollamaなど）: `"ollama:llama3"`

## 参考資料

- [LangChain公式ドキュメント](https://docs.langchain.com/oss/python/langchain)

