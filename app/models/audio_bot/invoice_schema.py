from langchain_core.pydantic_v1 import BaseModel, Field


class InvoiceJson(BaseModel):
    title: str = Field(description="Um titulo para o texto.")
    subtitle: str = Field(description="Um titulo para o texto como menos de 24 caracteres.")
    summary: str = Field(description="O resumo do texto.")