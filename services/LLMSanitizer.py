import re
from langchain_core.messages import AIMessage, HumanMessage
import sqlparse


class SQLSanitizer:
    pattern : str = re.compile(
        r"""
        \b(
            # DML
            SELECT\s+.+?\s+FROM |
            INSERT\s+INTO |
            UPDATE\s+\w+\s+SET |
            DELETE\s+FROM |
            # DDL
            CREATE\s+(TABLE|DATABASE|INDEX|VIEW) |
            DROP\s+(TABLE|DATABASE|INDEX|VIEW) |
            ALTER\s+TABLE |
            TRUNCATE\s+TABLE |
            # altri
            MERGE\s+INTO |
            EXEC(UTE)? |
            CALL\s+\w+
        )\b
        """,
        re.IGNORECASE | re.VERBOSE | re.DOTALL
    )


    def isContainingSQL(self, text:str,  sqlPattern: str = None):
        if sqlPattern is not None:
            patternToUse = re.compile(sqlPattern)
        else:
            patternToUse = self.pattern

        match  = re.findall(patternToUse, text)

        return bool(match)

    def produceInputFailOutput(self) -> AIMessage:
        return AIMessage("Your message is not acceptable.")

    def isInputMalicious(self, text:str) -> bool:
       return self.isContainingSQL(text)

    def sanitizeOutput(self, text:AIMessage) -> AIMessage:
        if self.isContainingSQL(text.content):
            return AIMessage("Cannot answer this question because it might expose sensible information")
        else:
            return text



