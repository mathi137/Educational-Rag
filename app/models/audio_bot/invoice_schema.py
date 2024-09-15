from langchain_core.pydantic_v1 import BaseModel, Field


class InvoiceJson(BaseModel):
    title: str = Field(description="Um titulo para o texto.")
    summary: str = Field(description="O resumo do texto.")