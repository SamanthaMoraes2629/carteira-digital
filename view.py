from models import Conta, engine, Bancos, Status, Historico, Tipos
from sqlmodel import Session, select
from datetime import date, timedelta
import matplotlib.pyplot as plt

def criar_conta(conta: Conta):
    with Session(engine) as session:
        statement = select(Conta).where(Conta.banco==conta.banco)
        results = session.exec(statement).all()
        if results:
            print('Já existe uma conta nesse banco!')
            return
        
        session.add(conta)
        session.commit()
        return conta

def listar_contas():
    with Session(engine) as session:
        statement = select(Conta)
        results = session.exec(statement).all()
    return results


def desativar_conta(id):
    with Session(engine) as session:
        statement = select(Conta).where(Conta.id==id)
        conta = session.exec(statement).first()
        if conta.valor > 0:
            raise ValueError('Essa conta ainda possui saldo')
        conta.status = Status.INATIVO
        session.commit()

def transferir_saldo(id_conta_saida, id_conta_entrada, valor):
    with Session(engine) as session:
        statement = select(Conta).where(Conta.id==id_conta_saida)
        conta_saida = session.exec(statement).first()
        if conta_saida.valor < valor:
            raise ValueError('Saldo insuficiente')
        statement = select(Conta).where(Conta.id==id_conta_entrada)
        conta_entrada = session.exec(statement).first()

        conta_saida.valor -= valor
        conta_entrada.valor += valor
        session.commit()


def total_contas ():
    with Session(engine) as session:
        statement = select(Conta)
        contas = session.exec(statement).all()
    
    total = 0
    for conta in contas:
        total += conta.valor
    return float(total)


def buscar_historico_entre_datas(data_inicio: date, data_fim: date):
    with Session(engine) as session:
        statement = select(Historico).where(
            Historico.data >= data_inicio,
            Historico.data <= data_fim
        )
        resultados = session.exec(statement).all()
        return resultados




#x = buscar_historico_entre_datas(date.today() - timedelta(days=1), date.today() + timedelta(days=1)) 
#print(x)       

#conta = Conta(valor=10, banco=Bancos.SANTANDER)
#resultado = criar_conta(conta)
#transferir_saldo(2, 3, 5)
#historico = Historico(conta_id =1, tipos=Tipos.ENTRADA, valor=10, data=date.today())
#movimentar_dinheiro(historico)
#print(total_contas())


with Session(engine) as session:
    contas = session.exec(select(Conta)).all()
    print(contas)

print(Bancos.SANTANDER)

def criar_grafico_por_conta():
    with Session(engine) as session:
        statement = select(Conta).where(Conta.status==Status.ATIVO)
        contas = session.exec(statement).all()
        bancos = [i.banco.value for i in contas]
        valores = [i.valor for i in contas]
        
        plt.figura(figsize=(10,6))
        bars = plt.bar(bancos, valores,color='skyblue')

        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                     f"R4 {height: .2f}",
                     ha="center", va="bottom")
        
        plt.title("Saldo por Conta Bancária")
        plt.xlabel("Bancos")
        plt.ylabel("Valor (R$)")
        plt.xticks(rotation=45)
        plt.toght_layout()
        plt.show()
