from __future__ import annotations
import pytest
from langgraph_sdk import get_client
from langgraph_sdk.client import LangGraphClient


@pytest.fixture()
def client() -> LangGraphClient:
    return get_client()


async def test_list_assistants(client: LangGraphClient):
    assistants = await client.assistants.search()
    print(assistants)
    assert len(assistants) > 0

    graph_ids = [assistant["graph_id"] for assistant in assistants]
    assert set(graph_ids) == {"my_first_agent", "my_second_agent"}


async def test_local_client(client):
    thread = await client.threads.create()
    assistant = (await client.assistants.search(graph_id="my_second_agent"))[0]

    input = {"messages": [{"role": "user", "content": "what's the weather in sf"}]}
    async for chunk in client.runs.stream(
        thread["thread_id"],
        assistant_id=assistant["assistant_id"],
        input=input,
        stream_mode="updates",
    ):
        print(f"Receiving new event of type: {chunk.event}...")
        print(chunk.data)
        print("\n\n")
