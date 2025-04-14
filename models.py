from sqlmodel import SQLModel, Field, create_engine, Column, Relationship
from enum import Enum
import sqlalchemy as sa
from datetime import date


class Bancos(str, Enum):
    BB = 'Banco do Brasil'
    CAIXA = 'Caixa'
    INTER = 'Inter'
    ITAU = 'Itaú'
    NUBANK = 'Nubank' 
    SANTANDER = 'Santander' 
    
class Status(str, Enum):
    ATIVO = 'Ativo'
    INATIVO = 'Inativo'

class Tipos(str, Enum):
    ENTRADA = 'Entrada'
    SAIDA = 'Saída'


class Conta(SQLModel, table=True):
    id: int = Field(primary_key=True)
    valor: float
    banco: Bancos = Field(sa_column=(sa.Enum(Bancos)), default=Bancos.NUBANK)
    status: Status = Field(sa_column=Column(sa.Enum(Status)), default=Status.ATIVO)

    historicos: list["Historico"] = Relationship(back_populates="conta")


class Historico(SQLModel, table=True):  # Alterado de Movimentacao para Historico
    id: int = Field(primary_key=True)
    conta_id: int = Field(foreign_key="conta.id")
    conta: Conta = Relationship(back_populates="historicos")
    tipo: Tipos = Field(default=Tipos.ENTRADA)
    valor: float
    data: date


sqlite_file_name = 'datebase.db'
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)

if __name__ == "__main__":
    SQLModel.metadata.create_all(engine)
    print("Tabela criada com sucesso!")
