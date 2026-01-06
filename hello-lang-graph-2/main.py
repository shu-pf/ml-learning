from langgraph.graph import StateGraph, MessagesState, START, END
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini")


def user_input(state: MessagesState):
    return {"messages": [HumanMessage(content="Hello, how are you?")]}


def llm_call(state: MessagesState):
    return {
        "messages": [
            llm.invoke(
                [SystemMessage(content="You are a helpful assistant.")]
                + state["messages"]
            )
        ],
        "llm_calls": state.get("llm_calls", 0) + 1,
    }


graph = StateGraph(MessagesState)

graph.add_node(user_input)
graph.add_node(llm_call)

graph.add_edge(START, "user_input")
graph.add_edge("user_input", "llm_call")
graph.add_edge("llm_call", END)
graph = graph.compile()

result = graph.invoke({"messages": [HumanMessage(content="hi!")]})
print(result)
