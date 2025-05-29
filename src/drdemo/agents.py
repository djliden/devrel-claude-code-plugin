import logging
from llama_index.llms.gemini import Gemini
from llama_index.core.agent.workflow import FunctionAgent, CodeActAgent
from llama_index.core.memory import (
    Memory,
    StaticMemoryBlock,
    FactExtractionMemoryBlock,
    VectorMemoryBlock,
)
from drdemo.utils import SimpleCodeExecutor
from drdemo.prompts import editor_system

logger = logging.getLogger(__name__)

class ChatManager:
    def __init__(self):
        """Initialize the chat manager with agents and memory."""
        try:
            logger.debug("Initializing Gemini LLM")
            self.llm = Gemini(model="gemini-2.0-flash", max_tokens=1000)
            logger.debug("LLM initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize LLM: {str(e)}", exc_info=True)
            raise

        # Initialize the code executor
        logger.debug("Initializing code executor")
        self.code_executor = SimpleCodeExecutor(locals={}, globals={})

        # Initialize memory
        logger.debug("Initializing memory")
        blocks = [FactExtractionMemoryBlock(llm=self.llm, name="extracted_facts", priority=1)]
        self.memory = Memory.from_defaults(
            session_id="my_session",
            token_limit=40000,
            memory_blocks=blocks,
            chat_history_token_ratio=0.5
        )

        # Initialize the editor agent
        logger.debug("Initializing editor agent")
        self.editor_agent = FunctionAgent(
            name="editor",
            llm=self.llm,
            system_prompt=editor_system.format(),
            tools=[],  # Add tools here
            can_handoff_to=["writer", "researcher", "coder"],
        )

        # Initialize other agents
        logger.debug("Initializing other agents")
        self.writer_agent = FunctionAgent(
            name="writer",
            llm=self.llm,
            tools=[],  # Add tools here
            can_handoff_to=["editor"]
        )

        self.researcher_agent = FunctionAgent(
            name="researcher",
            llm=self.llm,
            tools=[],  # Add tools here
            can_handoff_to=["editor"]
        )

        self.coder_agent = CodeActAgent(
            code_execute_fn=self.code_executor.execute,
            name="coder",
            llm=self.llm,
            tools=[],  # Add tools here
            can_handoff_to=["editor"]
        )
        logger.debug("All agents initialized successfully")

    async def run_editor(self, query: str) -> str:
        """Run the editor agent with the current memory state."""
        handler = self.editor_agent.run(query, memory=self.memory)
        result = await handler
        return result

# For backward compatibility
def initialize_editor_agent():
    """Initialize the editor agent."""
    manager = ChatManager()
    return manager.editor_agent

async def run_agent(query: str, agent) -> str:
    """Run the agent with the given query."""
    # This is now deprecated - use ChatManager instead
    logger.warning("Using deprecated run_agent function. Please use ChatManager instead.")
    manager = ChatManager()
    return await manager.run_editor(query)
