def deposito(saldo, historico):
    valor_depositado = float(input("digite o valor depositado: R$"))
    if valor_depositado > 0:
        saldo += valor_depositado
        historico.append(f"Depósito: R$ {valor_depositado:.2f}")
        print(f"Depósito de R$ {valor_depositado:.2f} realizado com sucesso.")
    else:
        print("O valor do depósito deve ser positivo.")
    return saldo, historico

def saque(saldo, historico):
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

def menu():
    print("""
    Operações disponíveis
    1. Depositar
    2. Sacar
    3. Extrato
    4. Sair""")

def extrato(saldo, historico):
    print(f"\nSaldo atual: R$ {saldo:.2f}")
    if historico:
        print("Histórico de Transações:")
        for transacao in historico:
            print(f" - {transacao}")
    else:
        print("Não foram realizadas movimentações")

saldo = 0.0
historico = []
while True:
    menu()
    opcao = input("Selecione a operação desejada: ")
    match opcao:
    case 1:
        saldo, historico = deposito(saldo, historico)
    case 2:
        saldo, historico = saque(saldo, historico)
    case 3:
        extrato(saldo, historico)
    case 4:
        print("Encerrando operação")
        break
    case _:
        print("Opção inválida. Por favor, escolha uma opção válida.")