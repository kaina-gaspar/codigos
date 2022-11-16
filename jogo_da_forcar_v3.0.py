'''
Aris Souza
'''


# baseDeDados = open("base_palavras.txt", "x") # setenca para criar um arquivo
import random


def palavraAleatoria(nomeArquivo):
    basePalavras = open(nomeArquivo, "r")  # abrindo o arquivo para leitura
    base_lista = []

    # ler o arquivo linha a linha e armazena em uma lista
    for palavra in basePalavras:
        base_lista.append(palavra.strip().upper())
    basePalavras.close()

    # retornar uma palavra aleatoria da lista:
    index = random.randint(0, len(base_lista) - 1)  # seleciona um num aleatorio entre 0 e 19
    palavraRadom = base_lista[index]

    return palavraRadom

#método para obter o nome e o e-mail do jogador:
def jogador():
    nome = input("Digite seu nome: ")
    email = input("Digite seu email: ")
    player = [nome, email]
    print("\nBem Vindo:", player[0], "-", player[1] + "\n")
    print("Vamos começar,")
    return (player)

#método para ler uma letra do usuário a cada rodada do jogo:
def recebePalpite(palpiteFeitos):
    ''' Essa funcao garante que o usuario digite so uma letra e que confere se a mesma ja foi chutada '''

    while True:  # enquanto o palpiteFeitos for verdadeiro
        print('\nDigite alguma letra: ')
        palpite = input().upper()  # aqui a variavel ira receber uma letra e passala para Maiuscula

        # verifica se o que foi digitado e apenas 1 letra:
        unicaLetra = verifica_tamanho_da_letra(palpite).upper()

        # verifica se a letra informada é repetida
        letra = checa_letraRepetida(unicaLetra, palpiteFeitos).upper()

        # Garante que a entrada seja uma letra
        if not 'A' <= str(letra) <= 'Z':
            print('\nEscolha Somente letras!')
        else:
            return letra  # se estiver dentro dos conformes ele retorna o palpite

#método para checar se o usuário inseriu apenas uma letra:
def verifica_tamanho_da_letra(letra):
    while(len(letra) != 1):
        print("\nDigite apenas uma letra por vez: ")
        letra = input()

    return letra

#método para checar se o usuário digitou uma letra repetida:
def checa_letraRepetida(palpite, palpiteFeitos):
    ''' Essa funcao garante que o usuario digite so uma letra e que confere se a mesma ja foi chutada '''
    if palpite in palpiteFeitos: # se palpite esta dentro de palpites feitos
        print('\nVoce ja digitou essa letra, digite de novo!')
        palpite_aux = recebePalpite(palpiteFeitos)
        return palpite_aux
    else:
        return palpite  # se estiver dentro dos conformes ele retorna o palpite

#método para verificar se a letra inserida está na palavra oculta:
def letraValida(palpite, palavraSecreta, letrasAcertadas, letrasErradas):

    if palpite in palavraSecreta:  # se o palpite for uma letra que ta na palavra certa
        print("letra consta na palavra \n")
        aux = 0
        for carac in palavraSecreta:
            if (palpite == carac):
                letrasAcertadas[aux] = palpite  # inserimos essa letra na lista
            aux += 1
        return True
    else:
        print("letra não consta na palavra \n")
        letrasErradas.append(palpite)
        return False

#método para o usuário supor uma palavra.
def chutar_palavra(palavra_sorteada, palavrasChutadas, acertou):

    palavra = input("Digite sua suposição \n")
    palavrasChutadas.append(palavra)

    if palavra.upper() == palavra_sorteada.upper():
        #print("Voce ganhou \n")
        acertou = True
    else:
        print("Palavra Errada! Voce ainda pode chutar {} palavras".format(3 - len(palavrasChutadas)))
    return acertou

#Imprimi informaçoes a cada rodada
def imprimir(lista_acertas,lista_erradas,contador_letra_erradas,contador_palavra_supostas, palavra_sorteada):

    print("lista letras acertadas: ", lista_acertas )
    #print(lista_acertas)
    print("lista letras Erradas:", lista_erradas)
    #print(lista_erradas)

    print("Voce tem: {} tentativas para errar a letra.".format(contador_letra_erradas))
    print("Voce tem: {} tentativas para errar a palavra.".format(contador_palavra_supostas))

    print("Palavra ate agora:")
    for elem in lista_acertas:
        print(elem, end = " ")

#método que cria um dicionário com o nome, o e-mail, a palavra oculta e se o usuário ganhou ou perdeu o game.
# Esse dicionário é salvo em um arquivo partidas.txt
def partidas(nomeJogador, emailJogador, palavraOculta, statusPartida):
  dicionario = {
      "jogador" : nomeJogador,
      "email" : emailJogador,
      "palavra" : palavraOculta,
      "status" : statusPartida
  }

  arquivo = open("partidadas.txt", "a")
  arquivo.write(str(dicionario) + "\n")
  arquivo.close()

def menu():

    print("*********Regras do jogo******\n")
    print(
        "Voce pode errar ate 5 letras caso erre as cinco "
        "\nSera dado uma chance final para acertar a palavra caso nao aceite esse chance final voce perde")
    print("Não usar acentos nas palavras acentuadas apenas as letras ")
    print("Deseja começar S/N")
    jogo = input()

    player = jogador()
    palavraSecreta = palavraAleatoria("base_palavras.txt")
    #print(palavraSecreta)

    palpiteFeitos = []
    letrasErradas = []
    palavrasSupostas = []
    letrasAcertadas = ['_' for letra in palavraSecreta]  # uma lista com mesmo tamanha da palavra oculta

    while jogo.upper() == "S":
        status = True
        enforcou = False
        acertou = False  # True se o jogador descobriu a palavra

        # print(palavraSecreta)
        print("\n", letrasAcertadas)

        while (not enforcou and not acertou and len(palavrasSupostas) < 3):

            palpite = recebePalpite(palpiteFeitos)  # recebe palpite já tratado
            palpiteFeitos.append(palpite)
            letraValida(palpite, palavraSecreta, letrasAcertadas, letrasErradas)

            print("\n")
            contador_letras_erradas = 5 - len(letrasErradas)
            contador_palavras = 3 - len(palavrasSupostas)
            imprimir(letrasAcertadas, letrasErradas, contador_letras_erradas, contador_palavras, palavraSecreta)
            print("\n")

            # supor palavra
            print("Deseja dizer a palavra  S/N: ")
            chutar = input()
            if (chutar.upper() == "S"):
                acertou = chutar_palavra(palavraSecreta, palavrasSupostas, acertou)
            else:
                enforcou = len(letrasErradas) == 5
                acertou = "_" not in letrasAcertadas

        if (acertou):
            print("\nVoce ganhou")
        else:
            print("\nVoce perdeu")

            if len(letrasErradas) == 5:
                print("Voce exagerou o seu limite de palpites!")

            print("Depois de " + str(len(letrasErradas)) + ' letras erradas e ' + str(len([x for x in letrasAcertadas if x != "_"])), end=' ')
            print('palpites corretos, a palavra era ' + palavraSecreta + '.')

            # print(palavrasErradas)
            status = False

        partidas(player[0], player[1], palavraSecreta, status)

        print("\nDeseja jogar mais uma vez \n")
        jogo = input()
        palavraSecreta = palavraAleatoria("base_palavras.txt")
        palpiteFeitos = []
        letrasErradas = []
        palavrasSupostas = []
        letrasAcertadas = ['_' for letra in palavraSecreta]  # uma lista com mesmo tamanha da palavra oculta

menu()
