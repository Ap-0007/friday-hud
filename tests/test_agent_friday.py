import pytest
from unittest.mock import AsyncMock, patch, MagicMock, PropertyMock

from agent_friday import MayaAgent

@pytest.mark.asyncio
async def test_maya_agent_on_enter():
    with patch("agent_friday.silero.VAD.load") as mock_vad_load, \
         patch("agent_friday.mcp.MCPServerHTTP") as mock_mcp, \
         patch("agent_friday._mcp_server_url", return_value="http://fake:8000"):

        stt = MagicMock()
        llm = MagicMock()
        tts = MagicMock()

        agent = MayaAgent(stt=stt, llm=llm, tts=tts)
        mock_session = AsyncMock()
        with patch.object(MayaAgent, 'session', new_callable=PropertyMock) as mock_session_prop:
            mock_session_prop.return_value = mock_session

            await agent.on_enter()

            mock_session.generate_reply.assert_called_once_with(
                instructions=(
                    "Greet the user exactly with: 'Greetings boss, you're awake late at night today. What you up to?' "
                    "Maintain a helpful but dry tone."
                )
            )
