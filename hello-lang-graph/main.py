"""
LangGraphの複雑な例 - グラフの利点を実感できるワークフロー

この例では以下の機能を実装します：
1. 質問の分類（計算、天気、一般的な質問）
2. 分類に応じた条件分岐
3. 複数の処理ノード（計算、天気取得、LLM応答）
4. 結果の統合
"""

from langgraph.graph import StateGraph, MessagesState, START, END
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_openai import ChatOpenAI
from typing import Literal, TypedDict, Annotated
from langgraph.graph.message import add_messages
import re

llm = ChatOpenAI(model="gpt-4o-mini")


# カスタム状態を定義（MessagesStateを拡張）
class GraphState(TypedDict):
    messages: Annotated[list, add_messages]
    category: str


def get_message_content(message) -> str:
    """メッセージから文字列コンテンツを安全に取得"""
    if isinstance(message.content, str):
        return message.content
    elif isinstance(message.content, list):
        # リストの場合は最初の要素を取得
        if message.content and isinstance(message.content[0], dict):
            return message.content[0].get("text", "")
        return str(message.content)
    return str(message.content)


def classify_question(state: GraphState) -> dict:
    """ユーザーの質問を分類する"""
    last_message = state["messages"][-1]
    content = get_message_content(last_message)
    
    # 計算式のパターンを検出
    if re.search(r'\d+\s*[+\-*/×÷]\s*\d+', content) or "計算" in content:
        category = "calculation"
    # 天気に関する質問を検出
    elif "天気" in content or "weather" in content.lower():
        category = "weather"
    # その他は一般的な質問
    else:
        category = "general"
    
    # 分類結果をメッセージに追加
    classification_msg = AIMessage(
        content=f"[分類結果: {category}] 質問を分類しました。"
    )
    
    return {
        "messages": [classification_msg],
        "category": category
    }


def calculate(state: GraphState) -> dict:
    """計算を実行する"""
    # ユーザーの元のメッセージを取得（分類メッセージの前）
    user_message = state["messages"][-2]
    content = get_message_content(user_message)
    
    # 数式を抽出して計算
    match = re.search(r'(\d+)\s*([+\-*/×÷])\s*(\d+)', content)
    if match:
        num1 = int(match.group(1))
        op = match.group(2)
        num2 = int(match.group(3))
        
        # 演算子を変換
        op_map = {"×": "*", "÷": "/", "+": "+", "-": "-", "*": "*", "/": "/"}
        op = op_map.get(op, op)
        
        try:
            result = eval(f"{num1} {op} {num2}")
            response = AIMessage(
                content=f"計算結果: {num1} {op} {num2} = {result}"
            )
        except:
            response = AIMessage(content="計算に失敗しました。")
    else:
        response = AIMessage(content="数式を認識できませんでした。")
    
    return {"messages": [response]}


def get_weather(state: GraphState) -> dict:
    """天気情報を取得する（デモ用）"""
    # ユーザーの元のメッセージを取得（分類メッセージの前）
    user_message = state["messages"][-2]
    content = get_message_content(user_message)
    
    # 都市名を抽出（簡易版）
    city = "東京"  # デフォルト
    if "東京" in content:
        city = "東京"
    elif "大阪" in content:
        city = "大阪"
    elif "京都" in content:
        city = "京都"
    
    response = AIMessage(
        content=f"{city}の天気は晴れ、気温は22度です。"
    )
    
    return {"messages": [response]}


def general_response(state: GraphState) -> dict:
    """一般的な質問にLLMで応答する"""
    response = llm.invoke(state["messages"])
    return {"messages": [response]}


def route_question(state: GraphState) -> Literal["calculation", "weather", "general"]:
    """分類結果に基づいてルーティング"""
    category = state.get("category", "general")
    if category == "calculation":
        return "calculation"
    elif category == "weather":
        return "weather"
    else:
        return "general"


# グラフを構築
graph = StateGraph(GraphState)

# ノードを追加
graph.add_node("classify", classify_question)
graph.add_node("calculate", calculate)
graph.add_node("weather", get_weather)
graph.add_node("general", general_response)

# エッジを追加
graph.add_edge(START, "classify")

# 条件分岐を追加
graph.add_conditional_edges(
    "classify",
    route_question,
    {
        "calculation": "calculate",
        "weather": "weather",
        "general": "general",
    }
)

# すべての処理ノードから終了へ
graph.add_edge("calculate", END)
graph.add_edge("weather", END)
graph.add_edge("general", END)

# グラフをコンパイル
graph = graph.compile()


def main():
    """メイン関数"""
    print("=== LangGraph 複雑なワークフロー例 ===\n")
    
    # 例1: 計算の質問
    print("1. 計算の質問:")
    result1 = graph.invoke({  # type: ignore
        "messages": [HumanMessage(content="25 × 4 を計算してください")],
        "category": ""
    })
    print(f"質問: 25 × 4 を計算してください")
    print(f"回答: {result1['messages'][-1].content}\n")
    
    # 例2: 天気の質問
    print("2. 天気の質問:")
    result2 = graph.invoke({  # type: ignore
        "messages": [HumanMessage(content="東京の天気はどうですか？")],
        "category": ""
    })
    print(f"質問: 東京の天気はどうですか？")
    print(f"回答: {result2['messages'][-1].content}\n")
    
    # 例3: 一般的な質問
    print("3. 一般的な質問:")
    result3 = graph.invoke({  # type: ignore
        "messages": [HumanMessage(content="Pythonとは何ですか？")],
        "category": ""
    })
    print(f"質問: Pythonとは何ですか？")
    print(f"回答: {result3['messages'][-1].content}\n")
    
    # グラフの構造を可視化
    print("=== グラフの構造 ===")
    print("START -> classify -> [calculation/weather/general] -> END")
    print("\nグラフの利点:")
    print("- 条件分岐による柔軟なルーティング")
    print("- 複数のノードによる処理の分離")
    print("- 状態管理による情報の保持")
    print("- ワークフローの可視化とデバッグの容易さ")


if __name__ == "__main__":
    main()