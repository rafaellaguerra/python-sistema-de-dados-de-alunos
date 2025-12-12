#Sistema  de Dados de Alunos
#Aluna: Rafaella Alves Guerra



# -->Importa a biblioteca 'pandas' para trabalhar com arquivos CSV
import pandas as pd

# -->Importa a biblioteca 'os' para verificar se o arquivo existe
import os

# Nome do arquivo onde os dados dos alunos serão salvos:
arquivo = "alunos.csv"


# Função que vai carregar os dados do arquivo CSV
# Caso o arquivo não exista, ele será criado vazio
def carregar():
    # Verifica se o arquivo já existe:
    if os.path.exists(arquivo):
        # Se existir, lê o arquivo CSV e retorna os dados
        return pd.read_csv(arquivo)
    else:
        # Se não existir, cria um DataFrame vazio com as colunas necessárias
        df = pd.DataFrame(columns=[
            "matricula", "nome", "rua", "numero",
            "bairro", "cidade", "uf", "telefone", "email"
        ])
        # Salva o arquivo CSV vazio
        df.to_csv(arquivo, index=False)
        return df


# Função para gerar automaticamente o número da matrícula
def gerar_matricula(df):
    # Se não houver alunos cadastrados, a matrícula começa em 1
    if len(df) == 0:
        return 1
    # Caso contrário, pega a maior matrícula e soma 1
    return df["matricula"].max() + 1


# Função que vai inserir um novo aluno
def inserir(df):
    # Gera a matrícula automaticamente
    matricula = gerar_matricula(df)

    # Dicionário para armazenar os dados do aluno:
    aluno = {
        "matricula": matricula,
        "nome": input("Nome: "),
        "rua": input("Rua: "),
        "numero": input("Número: "),
        "bairro": input("Bairro: "),
        "cidade": input("Cidade: "),
        "uf": input("UF: "),
        "telefone": input("Telefone: "),
        "email": input("Email: ")
    }

    # Adiciona o novo aluno ao DataFrame
    df = pd.concat([df, pd.DataFrame([aluno])], ignore_index=True)

    # Salva os dados atualizados no arquivo CSV
    df.to_csv(arquivo, index=False)

    print("Aluno cadastrado com sucesso!")
    return df


# -->Função que vai pesquisar aluno pelo nome ou matrícula:
def pesquisar(df):
    # Solicita o dado de busca
    busca = input("Digite matrícula ou nome: ")

    # Verifica se a busca é um número (matrícula)
    if busca.isdigit():
        aluno = df[df["matricula"] == int(busca)]
    else:
        # Se for nome, faz a comparação sem diferenciar maiúsculas e minúsculas
        aluno = df[df["nome"].str.lower() == busca.lower()]

    # Se não encontrar nenhum aluno
    if aluno.empty:
        print("Aluno não encontrado")
        return None

    # Mostra os dados do aluno encontrado
    print(aluno)

    # Retorna a matrícula para possíveis ações futuras
    return int(aluno["matricula"].values[0])


# Função para editar os dados de um aluno
def editar(df, matricula):
    # Localiza o índice do aluno pelo número da matrícula
    i = df[df["matricula"] == matricula].index[0]

    # Lista com os campos que podem ser editados
    campos = ["nome", "rua", "numero", "bairro", "cidade", "uf", "telefone", "email"]

    # Mostra os campos disponíveis para edição
    for n, campo in enumerate(campos, 1):
        print(n, campo)

    # Usuário vai escolher qual campo deseja alterar
    op = int(input("Qual deseja editar: "))

    # Solicita o novo valor
    novo = input("Novo valor: ")

    # Atualiza o valor escolhido
    df.loc[i, campos[op - 1]] = novo

    # Salva as alterações no arquivo CSV
    df.to_csv(arquivo, index=False)

    print("Dado atualizado com sucesso!")
    return df


# Função para remover um aluno do sistema
def remover(df, matricula):
    # Confirmação antes de remover
    conf = input("Deseja remover o aluno? (s/n): ")

    if conf.lower() == "s":
        # Remove o aluno com a matrícula informada
        df = df[df["matricula"] != matricula]

        # Atualiza o arquivo CSV
        df.to_csv(arquivo, index=False)

        print("Aluno removido")
    else:
        print("Remoção cancelada")

    return df


# Função principal que exibe o menu do sistema
def menu():
    # Carrega os dados do arquivo
    df = carregar()

    # Loop do menu
    while True:
        print("\n1 - Inserir aluno")
        print("2 - Pesquisar aluno")
        print("3 - Sair")

        # Lê a opção escolhida
        op = input("Escolha: ")

        if op == "1":
            df = inserir(df)

        elif op == "2":
            mat = pesquisar(df)
            if mat:
                acao = input("(E)ditar ou (R)emover: ").lower()
                if acao == "e":
                    df = editar(df, mat)
                elif acao == "r":
                    df = remover(df, mat)

        elif op == "3":
            print("Saindo do sistema...")
            break

        else:
            print("Opção inválida")


# Inicia o programa chamando o menu
menu()