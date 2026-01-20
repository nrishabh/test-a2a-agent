from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.apps import A2AStarletteApplication
from a2a.server.events import EventQueue
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import AgentCapabilities, AgentCard, AgentSkill
from a2a.utils import new_agent_text_message

skill = AgentSkill(
    id="city_facts",
    name="City Facts",
    description="Returns an interesting fact about a city",
    tags=["city", "facts", "trivia"],
    examples=[
        "Tell me about Paris",
        "What's interesting about Tokyo?",
        "Facts about New York",
    ],
)


public_agent_card = AgentCard(
    name="City Facts Agent",
    description="An agent that tells you an interesting fact about the city you provide",
    url="https://test-a2a-agent.onrender.com",
    version="1.0.0",
    default_input_modes=["text"],
    default_output_modes=["text"],
    capabilities=AgentCapabilities(streaming=False),
    skills=[skill],  # Only the basic skill for the public card
)


class CityFactsAgent:
    """City Facts Agent Agent."""

    async def invoke(self) -> str:
        return "Hello! Nice to meet you!"


class HelloWorldAgentExecutor(AgentExecutor):
    """Test AgentProxy Implementation."""

    def __init__(self):
        self.agent = CityFactsAgent()

    async def execute(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:
        result = await self.agent.invoke()
        await event_queue.enqueue_event(new_agent_text_message(result))

    # --8<-- [end:HelloWorldAgentExecutor_execute]

    # --8<-- [start:HelloWorldAgentExecutor_cancel]
    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        raise Exception("cancel not supported")


request_handler = DefaultRequestHandler(
    agent_executor=HelloWorldAgentExecutor(),
    task_store=InMemoryTaskStore(),
)

server = A2AStarletteApplication(
    agent_card=public_agent_card,
    http_handler=request_handler,
)

app = server.build()
