from agentspan.agents import Agent, AgentRuntime, AgentHandle, tool
import time
import os

# আপনার কীটি এখানে বসিয়ে নিন
# os.environ["GEMINI_API_KEY"] = "YOUR_GEMINI_API_KEY"

# ক্র্যাশ করার পর টার্মিনাল থেকে পাওয়া Execution ID-টি দ্বিতীয়বার রান করার আগে এখানে বসাবেন
EXECUTION_ID = ""  


@tool
def save_tests(function_name: str, test_code: str) -> str:
    """Save generated pytest tests for a function to test_price_calculator.py."""
    # ক্র্যাশ টেস্ট লজিক: প্রথমবার এই টুল কল হওয়ামাত্রই কোডটি ক্র্যাশ করবে
    if not EXECUTION_ID:
        print("\n[CRASH TEST] Simulating a sudden crash during tool execution... 🔥")
        raise ValueError("SimulationCrash: Connection lost with AgentSpan server!")

    try:
        with open("test_price_calculator.py") as f:
            if f"# Tests for {function_name}" in f.read():
                return f"Tests for {function_name} already saved."
    except FileNotFoundError:
        pass

    time.sleep(2)
    with open("test_price_calculator.py", "a") as f:
        f.write(f"\n# Tests for {function_name}\n")
        f.write(test_code)
        f.write("\n")
    return f"Tests for {function_name} saved."


agent = Agent(
    name="testbot",
    model="google_gemini/gemini-2.5-flash",
    tools=[save_tests],
)

if not EXECUTION_ID:
    with open("test_price_calculator.py", "w") as f:
        f.write("import pytest\n")
        f.write("from price_calculator import (\n")
        f.write("    calculate_discount, calculate_tax,\n")
        f.write("    calculate_shipping, calculate_total\n)\n")

try:
    with open("price_calculator.py") as f:
        source = f.read()
except FileNotFoundError:
    source = """
def calculate_discount(price: float) -> float: return price * 0.1
def calculate_tax(price: float) -> float: return price * 0.05
def calculate_shipping(price: float) -> float: return 5.0 if price < 50 else 0.0
def calculate_total(price: float) -> float: return price - calculate_discount(price) + calculate_tax(price) + calculate_shipping(price)
"""
    with open("price_calculator.py", "w") as f:
        f.write(source)

with AgentRuntime() as runtime:
    if EXECUTION_ID:
        print(f"Resuming existing execution from crash point: {EXECUTION_ID} 🚀")
        handle = AgentHandle(execution_id=EXECUTION_ID, runtime=runtime)
        result = handle.stream().get_result()
    else:
        print("Starting a fresh test generation run (Expect a simulated crash)... ⚙️")
        prompt = f"""
        Analyze the following python source code and generate separate pytest functions for ALL defined functions:
        {source}
        
        For each function found, generate comprehensive test cases and immediately use the 'save_tests' tool to save them.
        """
        result = runtime.run(agent, prompt)

    result.print_result()
