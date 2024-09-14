from langchain.schema import (
    ChatGeneration,
    Generation,
    OutputParserException,
)
from langchain.output_parsers.openai_functions import JsonOutputFunctionsParser
from langchain_core.pydantic_v1 import BaseModel, Field
from typing import Any, List, Optional
import regex as re
import json


class Person(BaseModel):
    nome: Optional[str] = Field(description="O nome da pessoa.")
    rg: Optional[str] = Field(description="O RG da pessoa.")
    cpf: Optional[str] = Field(description="O CPF da pessoa.")
    endereco: Optional[str] = Field(description="O endereço da pessoa.")
    
    
class Company(BaseModel):
    razao_social: Optional[str] = Field(description="A razão social da empresa.")
    cnpj: Optional[str] = Field(description="O CNPJ da empresa.")
    endereco: Optional[str] = Field(description="O endereço da empresa.")
    representante: Optional[Person] = Field(description="O representante (pessoa) da empresa.")
    

class InvoiceJson(BaseModel):
    numero_contrato: Optional[str] = Field(description="O número do contrato do contrato (ID).")
    objeto_contrato: Optional[str] = Field(description="O objeto do contrato.")
    data_contrato: Optional[str] = Field(description="A data em que o contrato foi escrito.")
    valor_contrato: Optional[str] = Field(description="O valor do contrato.")
    vigencia_contrato: Optional[str] = Field(description="A vigência do contrato.")
    contratante: Optional[Company] = Field(description="A empresa contratante.")
    contratada: Optional[Company] = Field(description="A empresa contratada.")
    pessoas_citadas: Optional[List[Person]] = Field(default_factory=list, description="A lista de pessoas citadas.")


class JsonFixOutputFunctionsParser(JsonOutputFunctionsParser):
    """Parse an output as the Json object."""

    def get_fixed_json(self, text : str) -> str:
        """Fix LLM json"""
        text = re.sub(r'",\s*}', '"}', text)
        text = re.sub(r"},\s*]", "}]", text)
        text = re.sub(r"}\s*{", "},{", text)

        open_bracket = min(text.find('['), text.find('{'))
        if open_bracket == -1:
            return text

        close_bracket = max(text.rfind(']'), text.rfind('}'))
        if close_bracket == -1:
            return text
        return text[open_bracket:close_bracket+1]

    def parse_result(self, result: List[Generation], *, partial: bool = False) -> Any:
        if len(result) != 1:
            raise OutputParserException(
                f"Expected exactly one result, but got {len(result)}"
            )
        generation = result[0]
        if not isinstance(generation, ChatGeneration):
            raise OutputParserException(
                "This output parser can only be used with a chat generation."
            )
        message = generation.message
        try:
            function_call = message.additional_kwargs["function_call"]
        except KeyError as exc:
            if partial:
                return None
            else:
                raise OutputParserException(f"Could not parse function call: {exc}")
        fixed_json = self.get_fixed_json(str(function_call["arguments"]))
        return json.loads(fixed_json)