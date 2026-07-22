"""Chapter 12 - OpenTelemetry for Agents.

LangSmith is convenient but vendor-specific. OpenTelemetry is the
vendor-neutral fallback: you can send the same spans to Jaeger, Tempo,
Datadog, or Honeycomb. This script wires up a console exporter and
wraps a tiny "agent run" in nested spans.

Env vars needed:
    ANTHROPIC_API_KEY - your Anthropic API key (for the LLM call)

Run:
    python 02_opentelemetry_tracing.py
"""
import os

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor, ConsoleSpanExporter)

from langchain_anthropic import ChatAnthropic

trace.set_tracer_provider(TracerProvider())
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(ConsoleSpanExporter()))

tracer = trace.get_tracer("agent")

llm = ChatAnthropic(model="claude-sonnet-4-5")


def run_agent(query):
    with tracer.start_as_current_span("agent.run") as span:
        span.set_attribute("agent.query", query)
        with tracer.start_as_current_span("llm.plan"):
            plan = llm.invoke(query).content
        span.set_attribute("agent.plan_tokens", len(plan.split()))
        return plan


if __name__ == "__main__":
    if not os.environ.get("ANTHROPIC_API_KEY"):
        raise SystemExit("Set ANTHROPIC_API_KEY before running this script.")
    result = run_agent("Draft a one-line plan to research India's AI policy.")
    print(result)
