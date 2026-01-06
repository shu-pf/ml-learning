from langgraph.graph import StateGraph, MessagesState, START, END
from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini")

def mock_llm(state: MessagesState):
    return {"messages": [AIMessage(content="hello world")]}

def llm_call(state: MessagesState):
    return {
        "messages": [
            llm.invoke(
                state["messages"]
            )
        ],
        "llm_calls": state.get('llm_calls', 0) + 1
    }


graph = StateGraph(MessagesState)

graph.add_node(mock_llm)
graph.add_node(llm_call)

graph.add_edge(START, "mock_llm")
graph.add_edge("mock_llm", "llm_call")
graph.add_edge("llm_call", END)
graph = graph.compile()

result = graph.invoke({"messages": [HumanMessage(content="hi!")]})
print(result)
