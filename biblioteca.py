import os
import time
import json
import string
import pwinput
import random

maiuscula = string.ascii_uppercase
minuscula = string.ascii_lowercase
digitos = string.digits
pontuacao = string.punctuation
cripto_senha = []
# lista predefinida de generos literarios, para padronizar a escolha dos generos
generos_livros = (
    "Autoajuda", "Aventura", "Biografia",
    "Ciência", "Clássicos", "Distopia",
    "Ficção Científica", "Filosofia", "Fantasia", 
    "História", "Humor", "Infantil", 
    "Jovem Adulto", "Mistério", "Poesia", 
    "Policial", "Religião", "Romance", 
    "Suspense", "Tecnologia", "Terror"
)
acervo = []
usuarios = []
# salvar os dados dos usuarios e dos livros em arquivos json
# toda função que fizer alterações nos usuários e/ou acervo terá o salvar_dados() dentro dela
def salvar_dados():
    global usuarios, acervo
    usuarios = sorted(usuarios, key=lambda novo_usuario: novo_usuario['nome'])
    acervo = sorted(acervo, key=lambda livro: livro['Titulo'])
    with open('usuarios.json', 'w', encoding='utf8') as usuarios_json:
        json.dump(usuarios, usuarios_json, ensure_ascii=True, indent=2)

    with open('acervo.json', 'w', encoding='utf8') as acervo_json:
        json.dump(acervo, acervo_json, ensure_ascii=True, indent=2)

# pegar os dados já cadastrados no json para usar durante o sistema
def carregar_dados():
    global usuarios, acervo
    try:
        with open('usuarios.json', 'r', encoding='utf8') as usuarios_json:
            usuarios_desordenado = json.load(usuarios_json)
        usuarios = sorted(usuarios_desordenado, key=lambda novo_usuario: novo_usuario['nome'])
    except FileNotFoundError:
        usuarios = []

    try:
        with open('acervo.json', 'r', encoding='utf8') as acervo_json:
            acervo_desordenado = json.load(acervo_json)
            for i, livro in enumerate(acervo_desordenado):
                livro['Ano'] = int(livro['Ano'])
                livro['Paginas'] = int(livro['Paginas'])
                acervo_desordenado[i] = livro
        acervo = sorted(acervo_desordenado, key=lambda livro: livro['Titulo'])
    except FileNotFoundError:
        acervo = []


# limpa o terminal
# com entrada == True tem uma leve confirmação 
def limpar_terminal(entrada=False):
    if entrada:
        enter = input('\nPressione enter: ')
    if os.name == 'nt':
        os.system('cls') # cls é pra sistemas windows
    else:
        os.system('clear') # clear serve pra mac e linux


# recebe como parametro uma tupla com os valores numericos em string 
# exemplo: ('0', '1', '2')
# vão ser esses valores que a variavel opcao tera que obedecer
def escolha(opcao_tupla):
    while True:
        opcao = input('Insira sua escolha: ').lower().strip()
        if opcao not in (opcao_tupla):
            print('Selecione uma opção válida!')
        else:
            return opcao
            

# criptografia simples para as senhas
# pega o primeiro digito da senha e verifica em qual das listas o elemento está
# ai pega esse elemento e anda 3 casas pra frente, trocando o elemento pelo novo
def cifraCesar(senha):
    if len(cripto_senha) == 0:
        cripto_senha.clear()

    if len(senha) == 0:
        senha_criptografada = ''.join(cripto_senha)
        cripto_senha.clear()
        return senha_criptografada

    if senha[0] in digitos:
        lista = digitos

    elif senha[0] in maiuscula:
        lista = maiuscula

    elif senha[0] in minuscula:
        lista = minuscula
    
    elif senha[0] in pontuacao:
        lista = pontuacao 

    else:
        lista = None
        cripto_senha.append(senha[0])

    if lista:
        posicao = lista.index(senha[0])
        if (posicao + 3) >= len(lista):
            posicao = (posicao + 3) - len(lista)
            cripto_senha.append(lista[posicao])
        else:
            cripto_senha.append(lista[posicao + 3])

    return cifraCesar(senha[1:])


# função para cadastrar novos usuarios
def cadastro(nome, senha, email, celular):
    global usuarios
    
    novo_usuario = {
        'nome': nome,
        'senha': cifraCesar(senha),
        'email': email,
        'celular': celular,
        'livros': [],
        'is_admin': len(usuarios) == 0 # o primeiro usuario a cadastrar sera o administrador
    }                                  # a partir disso so administradores poderao tornar outros usuarios administradores
    usuarios.append(novo_usuario.copy())
    print('Cadastro realizado. Efetue o login.')
    salvar_dados()


# sistema de login
def login(nome, senha):
    for usuario in usuarios:
        if usuario['nome'] == nome and usuario['senha'] == cifraCesar(senha):
            print('Login realizado, seja bem vino!')
            return usuario
    print('Usuario ou senha incorreta!')
    return False


def recuperar_senha():
    email = input('Digite o e-mail cadastrado: ')
    for usuario in usuarios:
        if email == usuario['email']:
            print(f'Enviando codigo de confirmacao para o email {email}')

            while True:
                codigo = random.randint(100000, 999999)
                print(f'Simulando o codigo: {codigo}')
                codigo_ativo = input('Digite o codigo recebido no email: ')

                if codigo_ativo == str(codigo):
                    nova_senha = pwinput.pwinput("Digite sua nova senha: ")
                    usuario['senha'] = cifraCesar(nova_senha)
                    print("Senha redefinida com sucesso!")
                    salvar_dados()
                    return 
                else:
                    print("Código incorreto!")
                    print('Reenviando o codigo para o email')
    print('E-mail nao encontrado')
    return False


# ver informações do perfil, incluindo os livros cadastrados nele
# a senha aparece escondida com o uso de *
def ver_perfil(usuario):
    print(f"{' Meu Perfil ':-^32}")
    for k, v in usuario.items():
        if k == 'senha':
            print(f"{k}: {'*'*len(v)}")
        elif k == 'livros':
            print('Livros: ')
            for livro in usuario[k]:
                print(f" - {livro['Titulo']} ({livro['Autor']})")
        elif k == 'is_admin':
            pass
        else:
            print(f"{k}: {v}")


# mostra todos os livros no acervo
def mostrar_acervo():
    for id, livro in enumerate(acervo):
        print(f"{id + 1}. {livro['Titulo']} ({livro['Autor']})")


# mostra as informacoes do livro selecionado pelo usuario anteriormente
def buscar_livro(titulo):
    for livro in acervo:
        if titulo == livro['Titulo']:
            print('\n','-'*20, sep='')
            for k,v in livro.items():
                print(f'{k}: {v}')
            print('-'*20,'\n')
            return
    print('Não há livro cadastrado com esse nome!')


# pega o livro selecionado pelo id da lista acervos e registra no perfil do usuario
def pegar_livro(usuario):
    if len(usuario['livros']) == 3:
        print('Você atingiu o limite de 3 livros emprestados ao mesmo tempo. \nCancele um livro para poder pegar outro')
        return

    try:
        id = int(input('Numero do livro: [numero a esquerda do nome do livro] ')) - 1
        livro = acervo[id]
        usuario['livros'].append(livro.copy())
        print(f'\n{livro['Titulo']} adicionado ao seu perfil')
        print('\nMuito obrigado! Tenha uma ótima leitura!')
        salvar_dados()
        return
    except ValueError:
        print('Error - Id invalido')
    except IndexError:
        print(f'Error - Livro com id {id} nao encontrado')
        

# cancela o emprestimo de um livro no perfil do usuario
def cancelar_meus_livros(usuario):
    try:
        id = int(input('Id do livro a ser devolvido: [Numero a esquerda do titulo] '))
        usuario['livros'].pop(id)
        print('Livro removido do seu perfil!')
        salvar_dados()
        return
    except ValueError:
        print('Error - Id invalido')
    except IndexError:
        print(f'Error - Id nao encontrado')
        

# funcao que mostra os livros cadastrados no perfil do usuario
def ver_meus_livros(usuario):
    print(f'{' Meus Livros ':-^25}')
    if len(usuario['livros']) == 0:
        print('Não há livros cadastrados em seu perfil')
        return False
    else:
        for i, livro in enumerate(usuario.get('livros')):
            print(f"{i + 1}. {livro['Titulo']}")
        return True


# remove um livro do sistema
def remover_livro():
    mostrar_acervo()
    try:
        id = int(input('Id do livro: [Numero a esquerda do titulo] ')) - 1
        livro_a_remover = acervo[id]     
        for usuario in usuarios:
            if livro_a_remover in usuario['livros']:
                usuario['livros'].remove(livro_a_remover)
        acervo.remove(livro_a_remover)
        salvar_dados()
    except ValueError:
        print('Insira um numero de id valido')
    except IndexError:
        print(f'Livro com id {id} nao encontrado')


# cadastra o livro e adiciona na lista acervo
def adicionar_livros(titulo, autor, paginas, ano, isbn13, genero):
    global acervo
    livro = {
        'Titulo': titulo,
        'Autor': autor,
        'Paginas': paginas,
        'Ano': ano,
        'ISBN-13': isbn13,
        'Genero': genero,
    }
    acervo.append(livro.copy())
    salvar_dados()


def editar_livro():
    mostrar_acervo()
    while True:
        try:
            id = int(input('Numero do livro: [numero a esquerda do nome do livro] ')) - 1
            livro = acervo[id]
        except ValueError:
            print('Error - Id Inválido')
        except IndexError:
            print('Error - Livro não encontrado')
        else:
            break
    for k, v in livro.items():
        print(f'{k}: {v}')
    print(f"\nAtualizar {livro['Titulo']}")
    print('Obs: Não digite nada caso não queira mudar')
    for key in livro.keys():
        novo = input(f'Novo {key}: ')
        if novo != '':
            livro[key] = novo
    acervo[id] = livro
    salvar_dados()
    carregar_dados()

def ordenar_livros(chave, ordem):
    ordenada = sorted(acervo, key=lambda livro: livro[chave], reverse=ordem)
    for i, livro in enumerate(ordenada):
        print(f'{i+1}. {livro['Titulo']} - {chave}: {livro[chave]}')

# funcao com a entrada dos dados dos livros
def menu_cadastrar_livros():
    titulo = input('Titulo do livro: ')
    autor = input('Autor(a) do livro: ')

    while True:
        try:
            paginas = int(input('Quantidade de paginas: '))
        except ValueError:
            print('Error - Informe apenas numeros inteiros')
        else:
            break
 
    while True:
        try:
            ano = int(input('Ano de lançamento: '))
        except ValueError:
            print('Error - Ano invalido')
        else:
            break

    while True:
        try:
            isbn13 = input('Adicionar código ISBN-13: [apenas numeros] ')
            if isbn13.isdigit() == False or len(isbn13) != 13:
                raise ValueError 
            isbn13 = (isbn13[:3] + '-' +isbn13[3:])
        except ValueError:
            print('Error - Codigo ISBN invalido')
        else:
            break

    print('Generos Literátios: ')
    print("\n")
    num_colunas = 3  # Define o número de colunas
    linhas = (len(generos_livros) + num_colunas - 1) // num_colunas  # Calcula quantas linhas serão necessárias

    for i in range(linhas):
        linha = ""
        for j in range(num_colunas):
            index = i + j * linhas
            if index < len(generos_livros):
                linha += "{:<6} {:<18}".format(f"[{index + 1}]", generos_livros[index])
            else:
                linha += " " * 24  # Espaço vazio para manter o alinhamento
        print(linha)

    print("\n")

    while True:
        try:
            id = int(input('Id do genero literario: [numero a esquerda do genero] ')) - 1
            genero = generos_livros[id]
        except ValueError:
            print('Error - Id invalido')
        except IndexError:
            print('Error - Genero selecionado nao encontrado')
        else:
            break

    adicionar_livros(titulo, autor, paginas, ano, isbn13, genero)
    print('Livro adicionado!')
    limpar_terminal(True)


# funcao pra remover ou tornar um usuario administrador
def gerenciar_usuarios(id):
    try:
        id = int(id) - 1
        user = usuarios[id]
        ver_perfil(user)
        print('''
    [0] Excluir usuário
    [1] Tornar administrador
    [2] Cancelar
            ''')
        opcao = escolha(('0', '1', '2'))
        if opcao == '0':
            usuarios.pop(id)
            print('Usuário removido')
        elif opcao == '1':
            user['is_admin'] = True
            print(f"Usuário {user['nome']} agora é um administrador")
        elif opcao == '2':
            return
        salvar_dados()
    except ValueError:
        print('Error - Id invalido')
    except IndexError:
        print('Error - Usuario nao encontrado')

def configurar_notificacoes():
    limpar_terminal()
    print(f'{' Notificações ':-^26}')
    print("""
Escolha o método de envio das notificações

[1] Apenas no site
[2] Via E-mail
[3] Via SMS             
""")
    opcao = escolha(('1', '2', '3'))
    if opcao == '1':
        print("Notificações configuradas para serem enviadas apenas no site.")
    elif opcao == '2':
        print(f"Notificações configuradas para serem enviadas para o e-mail.")
    elif opcao == '3':
        print(f"Notificações configuradas para serem enviadas via SMS.")
    limpar_terminal(True)

# funcao de menu para o login e cadastro
def menu_login():
    limpar_terminal()
    print('''
[0] Cadastrar
[1] Login
[2] Esqueci a senha
''')    
    opcao = escolha(('0', '1', '2'))

    if opcao == '0': # cadastro
        nome = input('Nome: ')
        senha = pwinput.pwinput('Senha: ') #esconde a senha com *
        email = input('Email: ')

        while True:
            try:
                celular = input('Celular com DDD: [apenas os numeros] ')
                if len(celular) != 11 :
                    raise IndexError
                if not celular.isdigit():
                    raise ValueError
                celular = celular[:2]+' '+celular[2:7]+'-'+celular[7:]
            except IndexError:
                print('Error - Celular deve conter 11 numeros')
            except ValueError:
                print('Error - Celular deve conter apenas numeros')
            else:
                break

        cadastro(nome, senha, email, celular)
        salvar_dados()

    elif opcao == '1': # login
        nome = input('Usuario: ')
        senha = pwinput.pwinput('Senha: ')
        return  login(nome, senha)
    
    elif opcao == '2':
        recuperar_senha()

    limpar_terminal(True)


# funcao para a parte de pesquisar livros
def menu_pesquisar_livros(usuario_ativo):
    while True: 
        limpar_terminal()
        print(f'{' Pesquisar livro ':-^40}')
        if len(acervo) == 0:
            print('Não há livros cadastrados no momento')
            limpar_terminal(True)
            break

        else:
            mostrar_acervo()
            print('''
[0] Voltar ao menu inicial
[1] Procurar livro
[2] Pegar um livro emprestado
[3] Ordenar livros
''')
            while True:
                opcao = escolha(('0', '1', '2', '3'))
                break
            if opcao == '0': # voltar ao menu
                limpar_terminal(False)
                break
            elif opcao == '1': # procurar livro, mostrando suas informacoes
                titulo = input('Titulo do livro: ')
                buscar_livro(titulo)
            elif opcao == '2': # cadastrar livro no perfil do usuario
                pegar_livro(usuario_ativo)
            elif opcao == '3':
                print('''
[1] Ano
[2] Paginas
                ''')
                while True:
                    chave = input('Opcao para ordenar os livros: ')
                    if chave == '1':
                        chave = 'Ano'
                        break
                    elif chave == '2':
                        chave = 'Paginas'
                        break
                    else:
                        print('Opcao invalida!')

                print('''
[1] Crescente
[2] Decrescente'''
                    )
                while True:
                    ordem = input('Opcao para ordenar os livros: ')
                    if ordem == '1':
                        ordem = False
                        break
                    elif ordem == '2':
                        ordem = True
                        break
                    else:
                        print('Opcao invalida!')
                ordenar_livros(chave, ordem)
            limpar_terminal(True)


# funcao para o usuario ver os livros que possui em seu perfil
def menu_ver_meus_livros(usuario_ativo):
    limpar_terminal()
    
    while True:
        ver_livros = ver_meus_livros(usuario_ativo)
        if ver_livros:
            print('''
[0] Ver informações de um livro
[1] Cancelar empréstimo de um livro
[2] Voltar ao menu principal
    ''')
            opcao = escolha(('0', '1', '2'))
            if opcao == '0': # ver informacoes de um livro
                try:
                    id = int(input('Id do livro: [Numero a esquerda do titulo] ')) - 1
                    for k, v in acervo[id].items():
                        print(f'{k}: {v}')
                except ValueError:
                    print('Error - Id invalido')
                except IndexError:
                    print('Error - Livro nao encontrado')
                limpar_terminal(True)
            elif opcao == '1': # remover um livro do perfil, devolver o livro
                cancelar_meus_livros(usuario_ativo)
            elif opcao == '2':
                return
        else:
            break
    limpar_terminal(True)


# funcao principal, onde todas as outras funcoes serao invocadas
def menu():
    carregar_dados()
    usuario_ativo = None

    while not usuario_ativo: # vai realizar o menu_login ate que o usuario entre com um login valido, fazendo a funcao menu_login retorne True
        usuario_ativo = menu_login()
    # fim do login

    while True:
        limpar_terminal(False)
        print(f'{" MENU PRINCIPAL ":-^60}')
        print(
'''[0] Sair
[1] Ver perfil
[2] Pesquisar livros
[3] Ver meus livros
[4] Configurar notificações'''

)
        if usuario_ativo['is_admin'] == True:
            print(
'''[5] Adicionar livros no acervo
[6] Remover livros no acervo
[7] Editar livros
[8] Gerenciar usuários
'''
)
        if usuario_ativo['is_admin']:
            opcoes_disponiveis = ('0', '1', '2', '3', '4', '5', '6', '7', '8')
        else:
            opcoes_disponiveis = ('0', '1', '2', '3', '4')
        opcao = escolha(opcoes_disponiveis)

        if opcao == '0': # sair da sua conta
            print('Volte sempre')
            limpar_terminal(True)
            menu()

        elif opcao == '1': # ver informacoes do perfil
            limpar_terminal()
            ver_perfil(usuario_ativo)
            limpar_terminal(True)

        elif opcao == '2': # pesquisar livros para adicionar ao seu perfil
            menu_pesquisar_livros(usuario_ativo)

        elif opcao == '3': # ver os livros cadastrados no seu perfil
            menu_ver_meus_livros(usuario_ativo)

        elif opcao == '4': # Configura a forma de envio das notificaçoes
            configurar_notificacoes()
            
        # opcoes exclusivas do administrador
        if usuario_ativo['is_admin']:
            if opcao == '5': # adicionar livros no acervo
                menu_cadastrar_livros()

            elif opcao == '6': # remover livros do acervo, e consequentemente dos usuarios
                remover_livro()
                print('Livro removido!')
                limpar_terminal(True)

            elif opcao == '7':
                editar_livro()
                print('Livro atualizado')
                limpar_terminal(True)

            elif opcao == '8': # gerenciar usuarios
                i = 1
                for usuario in usuarios:
                    if usuario != usuario_ativo:   
                        print(f"{i}. {usuario.get('nome')}")
                        i += 1
                id = input('\nId do usuario: [numero a esquerda do usuario] ')
                gerenciar_usuarios(id)
                limpar_terminal(True)
        
# programa principal (so a def menu(), tudo ta dentro dela)
menu()
