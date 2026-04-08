import logging
from abc import ABC, abstractmethod

from langchain_core.messages import AIMessage

from services.LLMSanitizer import SQLSanitizer


class BaseForLLM(ABC):
    logger = logging.getLogger(__name__)
    def __init__(self, sanitizer : SQLSanitizer):
        self.sanitizer = sanitizer

    async def sendMessage(self, message: str):
        san = self.sanitizer

        self.logger.debug("sanitizing input")
        if san.isInputMalicious(message):
            return san.produceInputFailOutput()

        response = await self._sendMessage(message)

        self.logger.debug("sanitized output")
        return san.sanitizeOutput(response)

    @abstractmethod
    async def _sendMessage(self, message: str) -> AIMessage:
        pass
