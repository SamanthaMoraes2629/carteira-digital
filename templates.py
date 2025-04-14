from models import *
from view import *
from sqlmodel import Session, select
from models import Conta, Historico  
import sys
import io
import os


if sys.stdout.encoding != 'UTF-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    os.environ["PYTHONIOENCODING"] = "utf-8"

class UI:

    def __init__(self, controlador):
        self.controlador = controlador
        self.bancos_dict = {banco.value.lower(): banco for banco in Bancos}  

    def start(self):
        while True:
            print(''' 
            [1] -> Criar conta
            [2] -> Desativar conta
            [3] -> Transferir dinheiro
            [4] -> Movimentar dinheiro
            [5] -> Total contas
            [6] -> Filtrar histórico
            [7] -> Gráfico
            ''')
            
            try:
                choice = int(input('Escolha uma opção: '))
                print(f'Você escolheu: {choice}')
            except ValueError:
                print('Por favor, insira um número válido!')
                continue

            if choice == 1:
                self.criar_conta()
            elif choice == 2:
                self._desativar_conta()
            elif choice == 3:
                self._transferir_saldo()  
            elif choice == 4:
                self.movimentar_dinheiro()  
            elif choice == 5:
                self._total_contas()  
            elif choice == 6:
                self._filtrar_movimentacoes()  
            elif choice == 7:
                self._criar_grafico()
            else:
                print("Opção inválida, por favor escolha um número entre 1 e 7.")
                continue

    def criar_conta(self):
        print('Digite o nome de algum banco abaixo:')
        
        for banco in Bancos:
            print(f'---{banco.value}---')
        
        banco = input().strip().lower()

        if banco not in self.bancos_dict:
            print("Banco inválido. Tente novamente.")
            return

        with Session(engine) as session:
            statement = select(Conta).where(Conta.banco == self.bancos_dict[banco])
            conta_existente = session.exec(statement).first()
            if conta_existente:
                print("Já existe uma conta nesse banco!")
                return
        
        try:
            valor = input('Digite o valor em sua conta: ').replace(',', '.')
            valor = float(valor)
            if valor < 0:
                print("O valor deve ser positivo.")
                return
        except ValueError:
            print("Valor inválido! Digite um número válido.")
            return

        conta = Conta(banco=self.bancos_dict[banco], valor=valor)
        criar_conta(conta)
        print('Conta criada com sucesso!')

    def _desativar_conta(self):  
        print("\n=== Desativar Conta ===")
        
        # Listar contas ativas disponíveis
        with Session(engine) as session:
            contas_ativas = session.exec(
                select(Conta).where(Conta.status == Status.ATIVO)
            ).all()
            
            if not contas_ativas:
                print("Nenhuma conta ativa encontrada!")
                return
                
            print("\nContas ativas disponíveis:")
            for conta in contas_ativas:
                print(f"- {conta.banco.value} (Saldo: R$ {conta.valor:.2f})")
        
        # Solicitar nome do banco
        nome_banco = input("\nDigite o nome do banco que deseja desativar: ").strip().lower()
        
        with Session(engine) as session:
            # Buscar conta pelo nome do banco
            conta = session.exec(
                select(Conta)
                .where(
                    Conta.banco == self.bancos_dict.get(nome_banco),
                    Conta.status == Status.ATIVO
                )
            ).first()
            
            if not conta:
                print("Conta não encontrada ou já inativa!")
                return
                
            if conta.valor > 0:
                print(f"Não é possível desativar: a conta ainda possui saldo de R$ {conta.valor:.2f}")
                return
                
            # Confirmar desativação
            confirmacao = input(f"Tem certeza que deseja desativar a conta do {conta.banco.value}? (s/n): ").lower()
            
            if confirmacao == 's':
                conta.status = Status.INATIVO
                session.add(conta)
                session.commit()
                print(f"Conta do {conta.banco.value} desativada com sucesso!")
            else:
                print("Operação cancelada.")

    def _transferir_saldo(self):
        print("Transferir saldo:")
        try:
            origem = input("Digite o banco de origem: ").strip().lower()
            destino = input("Digite o banco de destino: ").strip().lower()
            valor = float(input("Digite o valor a ser transferido: ").replace(",", "."))

            if valor <= 0:
                print("O valor de transferência deve ser positivo!")
                return

            # Verificação dos bancos de origem e destino
            with Session(engine) as session:
                origem_conta = session.exec(select(Conta).where(Conta.banco == self.bancos_dict.get(origem))).first()
                destino_conta = session.exec(select(Conta).where(Conta.banco == self.bancos_dict.get(destino))).first()

                if not origem_conta or not destino_conta:
                    print("Conta de origem ou destino não encontrada!")
                    return

                if origem_conta.valor < valor:
                    print("Saldo insuficiente!")
                    return

                origem_conta.valor -= valor
                destino_conta.valor += valor

                session.add(origem_conta)
                session.add(destino_conta)
                session.commit()

                print(f"Transferência de {valor} realizada com sucesso de {origem} para {destino}!")
        except ValueError:
            print("Valor inválido! Tente novamente.")

    def movimentar_dinheiro(self):  
        print("Movimentar dinheiro:")
        try:
            banco = input("Digite o banco para movimentar o dinheiro: ").strip().lower()
            valor = float(input("Digite o valor a ser movimentado: ").replace(",", "."))

            if valor <= 0:
                print("O valor de movimentação deve ser positivo!")
                return

            with Session(engine) as session:
                conta = session.exec(select(Conta).where(Conta.banco == self.bancos_dict.get(banco))).first()
                if not conta:
                    print("Conta não encontrada!")
                    return

                conta.valor += valor
                session.add(conta)
                session.commit()

                print(f"Movimentação de {valor} realizada com sucesso na conta de {banco}!")
        except ValueError:
            print("Valor inválido! Tente novamente.")

    def _criar_grafico(self):
        print("Gerando gráfico...")
        with Session(engine) as session:
            statement = select(Conta).where(Conta.status == Status.ATIVO)
            contas = session.exec(statement).all()
            bancos = [i.banco.value for i in contas]
            total = [i.valor for i in contas]
        
        import matplotlib.pyplot as plt
        plt.bar(bancos, total)
        plt.xlabel('Bancos')
        plt.ylabel('Valor')
        plt.title('Saldo por Banco')
        plt.show()

    def _total_contas(self):  
        print("Calculando o total de contas ativas:")
        with Session(engine) as session:
            statement = select(Conta).where(Conta.status == Status.ATIVO)
            contas = session.exec(statement).all()
        
        total_saldo = sum(conta.valor for conta in contas)
        print(f"O total de saldo nas contas ativas é: {total_saldo:.2f}")

    def _filtrar_movimentacoes(self):
        print("Filtrando movimentações:")
        try:
            banco = input("Digite o banco para filtrar as movimentações: ").strip().lower()
            
            with Session(engine) as session:
                conta = session.exec(select(Conta).where(Conta.banco == self.bancos_dict.get(banco))).first()
                if not conta:
                    print("Conta não encontrada!")
                    return

                movimentacoes = session.exec(select(Historico).where(Historico.conta_id == conta.id)).all()  # Corrigido para Historico

                if not movimentacoes:
                    print("Nenhuma movimentação encontrada para esse banco.")
                    return

                # Exibe as movimentações
                print(f"Movimentações para o banco {banco}:")
                for mov in movimentacoes:
                    print(f"Data: {mov.data}, Tipo: {mov.tipo}, Valor: {mov.valor}")

        except ValueError:
            print("Erro ao filtrar as movimentações. Tente novamente.")

if __name__ == "__main__":
    controlador = None
    ui = UI(controlador)
    ui.start()
