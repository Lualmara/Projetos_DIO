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

def menu():
    print("""
    Operações disponíveis
    1. Depositar
    2. Sacar
    3. Extrato
    4. Criar novo usuário
    5. Criar nova conta
    6. Listar contas
    7. Sair""")

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
        linha = f"""\
            Agencia:\t{conta['agencia']}
            Conta:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """

def conferencia_user(cpf, usuarios):
    conferencia_user = [usuario for usuario in usuarios if usuarios["cpf"] == cpf]
    return conferencia_user[0] if conferencia_user else None

saldo = 0.0
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
