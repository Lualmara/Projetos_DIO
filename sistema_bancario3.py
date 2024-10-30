import textwrap
from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime


class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def saque(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")

        elif valor > 0:
            self._saldo -= valor
            print("\n=== Saque realizado com sucesso! ===")
            return True

        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

        return False

    def deposito(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\n=== Depósito realizado com sucesso! ===")
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            return False

        return True

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    def saque(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )

        excedeu_limite = valor > self._limite
        excedeu_saques = numero_saques >= self._limite_saques

        if excedeu_limite:
            print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")

        elif excedeu_saques:
            print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")

        else:
            return super().saque(valor)

        return False

    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """

class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%s"),
            }
        )

class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.saque(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.deposito(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


def menu():
    print("""
    Operações disponíveis
    1. deposito
    2. saque
    3. Extrato
    4. Criar novo usuário
    5. Criar nova conta
    6. Listar contas
    7. Sair""")

def conferencia_user(cpf, usuarios):
    conferencia_user = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return conferencia_user[0] if conferencia_user else None

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\n@@@ Cliente não possui conta! @@@")
        return

    # FIXME: não permite cliente escolher a conta
    return cliente.contas[0]

def deposito(saldo, historico, /):
    valor_depositado = float(input("digite o valor depositado: R$"))
    if valor_depositado > 0:
        saldo += valor_depositado
        historico.append(f"Depósito: R$ {valor_depositado:.2f}")
        print(f"Depósito de R$ {valor_depositado:.2f} realizado com sucesso.")
    else:
        print("O valor do depósito deve ser positivo.")
    return saldo, historico

def saque(*, saldo, historico):
    valor_sacado = float(input("digite o valor a ser sacado: R$"))
    if valor_sacado > 0:
        if valor_sacado <= saldo:
            saldo -= valor_sacado
            historico.append(f"Saque: R$ {valor_sacado:.2f}")
            print(f"Saque de R$ {valor_sacado:.2f} realizado com sucesso.")
        else:
            print("Saldo insuficiente.")
    else:
        print("O valor do saque deve ser positivo.")
    return saldo, historico

def extrato(saldo, /, *, historico):
    print(f"\nSaldo atual: R$ {saldo:.2f}")
    if historico:
        print("Histórico de Transações:")
        for transacao in historico:
            print(f" - {transacao}")
    else:
        print("Não foram realizadas movimentações")

def criar_user(usuarios):
    cpf = input("digite o CPF (somente números): ")
    usuario = conferencia_user(cpf, usuarios)
    
    if usuario:
        print("\n já existe usuario com esse CPF")
        return
    
    nome = input("informe o nome completo: ")
    data_nascimento = input ("informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    usuarios.append({"nome":nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})
    print("usuário criado com sucesso")

def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("digite o CPF (somente números): ")
    usuario = conferencia_user(cpf, usuarios)
    
    if usuario:
        print("\n Conta criada com sucesso")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}
    print("\n Usuário não encontrado")

def listar_contas(contas):
    for conta in contas:
        linha = f"""
            Agencia:\t{conta['agencia']}
            Conta:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
        print(linha)

def main():
    usuarios = []
    historico = []
    contas = []
    AGENCIA = "0001"
    while True:
        menu()
        opcao = int(input("Selecione a operação desejada: "))
        match opcao:
            case 1:
                saldo, historico = deposito(saldo, historico)
            case 2:
                saldo, historico = saque(saldo=saldo, historico=historico)
            case 3:
                extrato(saldo, historico=historico)
            case 4:
                criar_user(usuarios)
            case 5:
                numero_conta = len(contas) + 1
                conta = criar_conta(AGENCIA, numero_conta, usuarios)
                if conta:
                    contas.append(conta)
            case 6:
                listar_contas(contas)
            case 7:
                print("Encerrando operação")
                break
            case _:
                print("Opção inválida. Por favor, escolha uma opção válida.")

main()
