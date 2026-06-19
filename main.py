import os
from agentspan.agents import Agent, AgentRuntime, tool

# ১. সরাসরি স্ক্রিপ্টের ভেতরেই এনভায়রনমেন্ট ভেরিয়েবল ইঞ্জেক্ট করুন
os.environ["GEMINI_API_KEY"] = "AQ.Ab8RN6IbjJAZOC7xbxKzqBGXrZPuptcNPrK3z9s3VFzIDvvy9g"
os.environ["GOOGLE_CLOUD_PROJECT"] = "ai-agent-project"  # এটি দেওয়া নিরাপদ

@tool
def get_weather(city: str) -> str:
    return f"72 degrees and sunny in {city}"

# ২. সঠিক অফিশিয়াল মডেল প্রিফিক্স 'google_gemini/' ব্যবহার করুন
agent = Agent(
    name="weatherbot",
    model="google_gemini/gemini-2.5-flash", 
    tools=[get_weather],
)

with AgentRuntime() as runtime:
    result = runtime.run(agent, "What's the weather in NYC?")
    result.print_result()
