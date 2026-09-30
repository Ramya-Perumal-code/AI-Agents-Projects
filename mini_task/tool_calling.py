from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from langchain_groq import ChatGroq
from datetime import datetime

load_dotenv()





@tool
def get_multiply(a: int, b: int) -> int:
    """Multiply two numbers together."""
    return a * b

@tool
def get_time() -> str:
    """Return the current time."""
   
    return datetime.now().strftime("%H:%M:%S")

tools = [get_multiply, get_time]
tool_map = {t.name: t for t in tools}
print(tool_map)

llm = ChatGroq(model="openai/gpt-oss-120b", temperature=0)
llm_with_tools = llm.bind_tools(
    tools)


def run_query(question: str) -> str:
    messages = [HumanMessage(question)]
    print("Initial Messages ", messages)
    # input("Wait ....")

    # First call: model decides whether to answer directly or call a tool
    ai_msg = llm_with_tools.invoke(messages)
    messages.append(ai_msg)
    print("Messages after first call ", messages)
    # input("Wait ....")

    if ai_msg.tool_calls:
        print("tool calls ", ai_msg.tool_calls)
        # input("wait ...")
        # Execute each requested tool call
        for call in ai_msg.tool_calls:
            selected_tool = tool_map[call["name"]]
            print(f"selected_tool: {selected_tool}")
            print(f"tool_args: {call['args']}")
            tool_result = selected_tool.invoke(call["args"])
            print(f"tool_result: {tool_result}")
            messages.append(
                {
                    "role": "tool",
                    "content": str(tool_result),
                    "tool_call_id": call["id"],
                }
            )
            print("Messages after tool call ", messages)
            # input("Wait ....")

        # Second call: let the model turn tool results into a final answer
        print("Total Messages ", messages)
        input("Wait Final....")
        final_response = llm_with_tools.invoke(messages)
        return final_response.content
    else:
        # No tool needed — first response is already the final answer
        return ai_msg.content


if __name__ == "__main__":
    print(run_query("What is 47 times 89?. Use the tool if provided"))