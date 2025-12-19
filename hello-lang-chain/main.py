"""
簡単なLangChainエージェントの例

この例では、計算ツールと天気ツールを持つエージェントを作成し、呼び出します。
"""

from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain.tools import tool


@tool
def calculate(expression: str) -> str:
    """数式を計算します。
    
    Args:
        expression: 計算する数式（例: "2 + 2", "10 * 5"）
    
    Returns:
        計算結果の文字列
    """
    try:
        result = eval(expression)
        return f"計算結果: {result}"
    except Exception as e:
        return f"エラー: {str(e)}"


@tool
def get_weather(city: str) -> str:
    """指定された都市の天気情報を取得します。
    
    Args:
        city: 都市名（例: "東京", "San Francisco"）
    
    Returns:
        天気情報の文字列
    """
    # これはデモ用の実装です。実際のAPIを呼び出す場合は、ここを変更してください。
    return f"{city}の天気は晴れ、気温は22度です。"


def main():
    # エージェントを作成
    # 注意: 実際のモデルを使用するには、環境変数にAPIキーを設定する必要があります
    # 例: export OPENAI_API_KEY="your-api-key"
    # または: export ANTHROPIC_API_KEY="your-api-key"
    
    # モデル名は使用するプロバイダーに応じて変更してください
    # OpenAIの場合: "gpt-4o" または "gpt-3.5-turbo"
    # Anthropicの場合: "claude-sonnet-4-5-20250929"
    # ローカルモデルの場合: "ollama:llama3" など
    
    # モデルを初期化
    model = init_chat_model("gpt-4o")  # または使用したいモデル名
    
    # エージェントを作成
    agent = create_agent(
        model=model,
        tools=[calculate, get_weather],
        system_prompt="あなたは親切なアシスタントです。ユーザーの質問に答えるために、必要に応じてツールを使用してください。",
    )
    
    # エージェントを呼び出し
    print("エージェントに質問を送信しています...")
    
    # 例1: 計算を依頼
    result1 = agent.invoke({
        "messages": [{"role": "user", "content": "25 × 4 を計算してください"}]
    })
    print("\n=== 計算の結果 ===")
    print(result1["messages"][-1].content)
    
    # 例2: 天気を尋ねる
    result2 = agent.invoke({
        "messages": [{"role": "user", "content": "東京の天気はどうですか？"}]
    })
    print("\n=== 天気の結果 ===")
    print(result2["messages"][-1].content)
    
    # 例3: 複合的な質問
    result3 = agent.invoke({
        "messages": [{"role": "user", "content": "100 ÷ 4 を計算して、その結果を使って東京の天気を教えてください"}]
    })
    print("\n=== 複合的な質問の結果 ===")
    print(result3["messages"][-1].content)


if __name__ == "__main__":
    main()
