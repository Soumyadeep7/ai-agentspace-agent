import os
from agentspan.agents import Agent, AgentRuntime, tool

# আপনার সিকিউর এপিআই কী এখানে বসাবেন
# os.environ["GEMINI_API_KEY"] = "YOUR_GEMINI_API_KEY"

@tool
def save_tests(function_name: str, test_code: str) -> str:
    """Saves the generated test code into a file."""
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

with AgentRuntime() as runtime:
    # এজেন্টকে একবারে সব ডিটেইলস দিয়ে প্রম্পট রিরাইট করা হলো
    prompt = """
    Please generate a comprehensive pytest suite for the function 'calculate_total'.
    
    Function Details to use for testing:
    - Name: calculate_total(price: float, tax_rate: float) -> float
    - Logic: It returns the total price by adding tax (price * tax_rate) to the original price.
    - Edge Cases to include: 
      1. Normal positive price and tax (e.g., price=100, tax_rate=0.1)
      2. Zero price or zero tax
      3. Negative price values (should handle or raise error)
    
    After writing the test code, immediately call the 'save_tests' tool to save it into the file.
    """
    
    result = runtime.run(agent, prompt)
    result.print_result()
