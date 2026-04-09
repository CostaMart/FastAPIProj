import logging
from abc import ABC, abstractmethod

from langchain_core.messages import AIMessage

from services.LLMService.InputOutputSanitizer import InputOutputSanitizer


class BaseForLLM(ABC):
    logger = logging.getLogger(__name__)
    def __init__(self, sanitizer : InputOutputSanitizer | None = None):
        if sanitizer is not None:
            self.sanitizer = sanitizer

    async def sendMessage(self, message: str):
        sanitizier = self.sanitizer

        self.logger.debug("sanitizing input")

        if sanitizier.isInputMalicious(message):
            return sanitizier.getInputRejectedResponse()

        response = await self._sendMessage(message)

        self.logger.debug("sanitized output")
        return sanitizier.sanitizeOutput(response)

    @abstractmethod
    async def _sendMessage(self, message: str) -> AIMessage:
        pass
