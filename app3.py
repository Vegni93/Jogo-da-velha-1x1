from flask import Flask, render_template, request, redirect, url_for
 
app = Flask(__name__)
 
tabuleiro = {i: ' ' for i in range(1, 10)}
jogador_atual = 1
jogador_inicial = 1
mensagem = ''
jogo_acabou = False
 
 
def verificar_vencedor(tab, letra):
    """Verifica se o jogador com a letra dada ganhou"""
    combinacoes = [
        [1, 2, 3], [4, 5, 6], [7, 8, 9],  
        [1, 4, 7], [2, 5, 8], [3, 6, 9],  
        [1, 5, 9], [3, 5, 7],              
    ]
    for a, b, c in combinacoes:
        if tab[a] == tab[b] == tab[c] == letra:
            return True
    return False
 
 
def tabuleiro_cheio(tab):
    """Verifica se não há mais posições disponíveis"""
    for posicao in tab:
        if tab[posicao] == ' ':
            return False
    return True
 
 
def letra_do_jogador(jogador):
    """Retorna X ou O dependendo de quem começa"""
    if jogador_inicial == 1:
        return 'X' if jogador == 1 else 'O'
    else:
        return 'O' if jogador == 1 else 'X'
 
 
@app.route('/')
def index():
    return render_template('index3.html',
                           tabuleiro=tabuleiro,
                           jogador_atual=jogador_atual,
                           letra=letra_do_jogador(jogador_atual),
                           mensagem=mensagem,
                           jogo_acabou=jogo_acabou)
 
 
@app.route('/jogar', methods=['POST'])
def jogar():
    global tabuleiro, jogador_atual, mensagem, jogo_acabou
 
    if jogo_acabou:
        return redirect(url_for('index'))
 
    posicao = int(request.form['posicao'])
    letra = letra_do_jogador(jogador_atual)
 
    if tabuleiro[posicao] != ' ':
        mensagem = '⚠️ Posição ocupada! Escolha outra.'
        return redirect(url_for('index'))
 
    
    tabuleiro[posicao] = letra
 
    
    if verificar_vencedor(tabuleiro, letra):
        mensagem = f'🏆 Jogador {jogador_atual} ({letra}) GANHOU! Parabéns!'
        jogo_acabou = True
        return redirect(url_for('index'))
 
    if tabuleiro_cheio(tabuleiro):
        mensagem = '🤝 EMPATE! O tabuleiro está cheio.'
        jogo_acabou = True
        return redirect(url_for('index'))
 
    
    if jogador_atual == 1:
        jogador_atual = 2
    else:
        jogador_atual = 1
 
    mensagem = ''
    return redirect(url_for('index'))
 
 
@app.route('/reiniciar', methods=['POST'])
def reiniciar():
    global tabuleiro, jogador_atual, jogador_inicial, mensagem, jogo_acabou
 
    
    if jogador_inicial == 1:
        jogador_inicial = 2
    else:
        jogador_inicial = 1
 
    tabuleiro = {i: ' ' for i in range(1, 10)}
    jogador_atual = jogador_inicial
    mensagem = f'🔄 Agora o Jogador {jogador_inicial} começa!'
    jogo_acabou = False
 
    return redirect(url_for('index'))
 
 
if __name__ == '__main__':
    app.run(debug=True)