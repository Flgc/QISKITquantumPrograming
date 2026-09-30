# Algoritmo de Shor (atualizado)
# Atividade baseada no projeto final de curso - Graduação Engenharia da Computação:
#  "Fatoração de Números com Recursos da Computação Quântica Para Aplicação na Criptografia"
# Min. Defesa Dep. Ciência e Tecnologia - IME
# Autoria original: Bianca de Meira Lopes e Thainá Lucciola Hipolito de Lima - APÊNDICE E
# Orientadores: José Antonio Moreira Xexéo, D.C. | Anderson Fernandes Pereira dos Santos,D.Sc.

# Atualizações realizadas com base na versão do Linux Mint 22.1 (Xia), respeitando as diretrizes PEP 668.
# Este código utiliza a sintaxe atualizada do Qiskit (1.x), garantindo compatibilidade moderna.

# Rio de Janeiro-RJ - 30-09-26


# Qiskit 1.x - Importes essenciais
import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram, plot_distribution
import matplotlib.pyplot as plt


# FUNÇÕES AUXILIARES QUÂNTICAS

def U_f(x, power):
    """
    Operador de exponenciação modular controlada (oráculo).
    Aplica a transformação unitária U|y> = |(y * x^power) mod 15>.
    Esta função implementa circuitos otimizados (hardcoded) composto
      por portas SWAP e X para simular a aritmética modular do número 15, 
      evitando a complexidade de um somador quântico completo.
    """
    
    U = QuantumCircuit(4)
    U.name = "U_f^%i" % (power)

    """
    Validação: o algoritmo de Shor exige que 'x' (ou 'a') seja comprimo de N (15).
    Caso o MDC(x, 15) !=1, o próprio MDC já é um fator não trivial, dispensando a 
      fase quântica. 
    """

    if x in [1,3,5,6,9,10,12,14]:
        raise ValueError("MDC entre 'a' e N deve ser 1. Escolha a = 2, 4, 7, 8, 11 ou 13.")

    current_power = power
    while (current_power > 0):
        current_power -= 1
        
        # Implementação em nível de portas lógicas da multiplicação modular para N=15
        if x in [2,13]:
            U.swap(0,1)
            U.swap(1,2)
            U.swap(2,3)
        if x in [7,8]:
            U.swap(2,3)    
            U.swap(1,2)
            U.swap(0,1)
        if x in [4,11]:
            U.swap(1,3)
            U.swap(0,2)
        if x in [7,11,13]:
            for q in range(4):
                U.x(q)

    # Transforma o circuito em um portão quântico controlado (C-U)
    c_Uf = U.to_gate().control()                
    return c_Uf


def qft(n):
    """
    Transformada de Fourier Quântica Inversa  (IQFT ou QFT†).
    No algoritmo  de Shor, a IQFT é aplicada ao primeiro registrador para extrair a fase
      (que contém o período 'r') do estado emaranhado gerado pela exponenciação modular.
    Ela realiza interferência construtiva nas amplitudes que correspondem aos múltiplos de 1/r.
    """
    qc = QuantumCircuit(n)
    qc.name = "QFT†"

    #Inversão da ordem dos qubits (necessário para a correta representação da QFT)
    for qubit in range(n//2):
        qc.swap(qubit, n-qubit-1)

    # Aplicação das portas de fase controlada (CP) e Hadamard (H)
    for j in range(n):
        for m in range(j):
            qc.cp(-np.pi/float(2**(j-m)), m, j)
        qc.h(j)
    return qc.to_gate()

# CONSTRUÇÃO DO CIRCUITO PRINCIPAL

# 1. Configuração dos parâmetros do algoritmo de Shor
n = 8 # Registrador de contagem (Reg 1): 8 qubits garantem adequaç~precisão adequada (normalmente 2*log2(N))
a = 2 # 'a' (ou 'x': Base aleatória escolhida para fatorar N=15. Deve ser coprimo de 15.

# 2. Inicialização do circuito quântico
# Total de 12 qubits: 8 para o Reg 1 e 4 para o Reg 2 (já quê, 2^4 = 16, suficiente para armazenar N=15)
qc = QuantumCircuit(n + 4, n)

# Gera a superposição: Portas Hadamard no Reg 1 cobrem todos os valores possíveis de 'x' simultaneamente
for q in range(n):
    qc.h(q)

# Preparo do estado próprio (Eigenstate): O Reg 2 é inicializado no estado |1> em vez de |0>
# Isso é um requisito matemático para que a exponenciação a^0 mod N resulte em 1.
qc.x(3+n)    

# 3. Aplicação do oráculo de exponenciação modular controlada
# Aplica U_f condicionada a cada qubit do Reg 1. Isso emaranha o Reg 1 com o Reg 2, 
# codificando a função periódica f(x) = a^x mod N no estado quântico.
for q in range(n):
    aux = 2**q
    qc.append(U_f(a, aux), [q] + [i+n for i in range(4)])

# 4. Aplica a Transformada de Fourier Quântica Inversa (QFT†)
# Extrai o período 'r' da função avaliada, gerando picos de probabilidade nos estados mensuráveis
qc.append(qft(n), range(n))

# 5. Medição do primeiro registrador
# O colapso da função de onda revelará aproximações de s/r (onde 's' é um inteiro e 'r' o período procurado)
qc.measure(range(n), range(n))

# Desenho do circuito no terminal
print("\n--- Desenho do circuito de Shor ---")
print(qc.draw(output='text'))

# EXECUÇÃO E VISUALIZAÇÃO

# 6. Execução no simulador local (AerSimulator)
simulador = AerSimulator()
qc_transpilado = transpile(qc, simulador)

# Executa 1024 medições (shots) para compor a estatística probabilística
job = simulador.run(qc_transpilado, shorts=1024)
contagens = job.result().get_counts()

print("\n--- Resultados da simulação de Shor:\n")
print(contagens)

# 7. Gráfico 1: Histograma clássico
# Os picos visíveis no gráfico representam os estados onde ocorreu interferência construtiva.
# Esses valores (em decimal) podem ser convertidos em frações contínuas para encontrar o período 'r'.
plot_histogram(
    contagens,
    color='darkcyan',
    title=f"Resultados de Shor (fatoração com a={a})",
    figsize=(10, 6) # Gráfico ligeiramente mais largo para acomodar os estados de 8 bits
)
plt.ylabel("Frequência das medições")
plt.savefig("resultado_histograma_shor.png", bbox_inches="tight")
print("\n[✔] Gráfico primário salvo como 'resultado_histograma_shor.png'.")

# 8. Gráfico 2: Distribuição probabilística
plot_distribution(
    contagens,
    color='crimson',
    title="Distribuição probabilística de Shor"
)
plt.ylabel("Probabilidade (%)")
plt.savefig("resultado_distribuicao_shor.png", bbox_inches="tight")
print("[✔] Gráfico secundário (probabilidade) salvo como 'resultado_distribuicao_shor.png'.")