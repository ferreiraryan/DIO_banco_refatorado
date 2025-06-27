
import textwrap


def mostrar_menu():
    mensagem = """
    ======= MENU PRINCIPAL =======
    [d] Depositar
    [s] Sacar
    [e] Ver extrato
    [nu] Cadastrar usuario
    [nc] Cadastrar conta
    [lc] Listar contas
    [q] Sair
    => """
    return input(textwrap.dedent(mensagem))


def processar_deposito(balance, amount, log, /):
    if amount > 0:
        balance += amount
        log += f"Deposito:\tR$ {amount:.2f}\n"
        print("Deposito realizado com sucesso!")
    else:
        print("Operacao falhou! Valor invalido para deposito.")
    return balance, log


def processar_saque(*, balance, amount, log, limit, saques_realizados, max_saques):
    if amount > balance:
        print("Operacao falhou! Saldo insuficiente.")
    elif amount > limit:
        print("Operacao falhou! Valor excede o limite por saque.")
    elif saques_realizados >= max_saques:
        print("Operacao falhou! Limite de saques diarios atingido.")
    elif amount > 0:
        balance -= amount
        log += f"Saque:\t\tR$ {amount:.2f}\n"
        saques_realizados += 1
        print("Saque efetuado com sucesso.")
    else:
        print("Operacao falhou! Valor invalido para saque.")
    return balance, log


def imprimir_extrato(balance, /, *, log):
    print("\n========= EXTRATO =========")
    print(log if log else "Sem movimentacoes registradas.")
    print(f"Saldo atual:\tR$ {balance:.2f}")
    print("===========================")


def novo_usuario(lista_usuarios):
    cpf_input = input("CPF (somente numeros): ")
    if buscar_usuario(cpf_input, lista_usuarios):
        print("Ja existe usuario com este CPF.")
        return

    nome = input("Nome completo: ")
    nascimento = input("Data de nascimento (dd-mm-aaaa): ")
    endereco = input("Endereco (logradouro, numero - bairro - cidade/UF): ")

    lista_usuarios.append({
        "nome": nome,
        "data_nascimento": nascimento,
        "cpf": cpf_input,
        "endereco": endereco
    })

    print("Usuario cadastrado com sucesso.")


def buscar_usuario(cpf, lista_usuarios):
    return next((u for u in lista_usuarios if u["cpf"] == cpf), None)


def nova_conta(ag, num_conta, lista_usuarios):
    cpf = input("CPF do titular: ")
    usuario = buscar_usuario(cpf, lista_usuarios)

    if usuario:
        print("Conta criada com sucesso.")
        return {
            "agencia": ag,
            "numero_conta": num_conta,
            "usuario": usuario
        }

    print("Usuario nao encontrado.")
    return None


def exibir_contas(lista_contas):
    for c in lista_contas:
        detalhes = f"""\
        Agencia:\t{c['agencia']}
        Conta:\t\t{c['numero_conta']}
        Titular:\t{c['usuario']['nome']}
        """
        print("-" * 50)
        print(textwrap.dedent(detalhes))


def sistema_bancario():
    MAX_SAQUES = 3
    CODIGO_AGENCIA = "0001"

    saldo_atual = 0
    limite_saque = 500
    extrato_log = ""
    contagem_saques = 0
    usuarios = []
    contas = []

    while True:
        escolha = mostrar_menu()

        if escolha == "d":
            valor = float(input("Valor do deposito: "))
            saldo_atual, extrato_log = processar_deposito(
                saldo_atual, valor, extrato_log)

        elif escolha == "s":
            valor = float(input("Valor do saque: "))
            saldo_atual, extrato_log = processar_saque(
                balance=saldo_atual,
                amount=valor,
                log=extrato_log,
                limit=limite_saque,
                saques_realizados=contagem_saques,
                max_saques=MAX_SAQUES
            )

        elif escolha == "e":
            imprimir_extrato(saldo_atual, log=extrato_log)

        elif escolha == "nu":
            novo_usuario(usuarios)

        elif escolha == "nc":
            numero = len(contas) + 1
            conta = nova_conta(CODIGO_AGENCIA, numero, usuarios)
            if conta:
                contas.append(conta)

        elif escolha == "lc":
            exibir_contas(contas)

        elif escolha == "q":
            print("Encerrando o sistema.")
            break

        else:
            print("Opcao invalida. Tente novamente.")


if __name__ == "__main__":
    sistema_bancario()
