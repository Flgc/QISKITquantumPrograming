# Algoritmo de Grover - Busca em Banco de Dados Não Ordenado
# Atividade baseada no projeto final de curso - Graduação Engenharia da Computação:
#  "Fatoração de Números com Recursos da Computação Quântica Para Aplicação na Criptografia"
# Min. Defesa Dep. Ciência e Tecnologia - IME
# Autoria original: Bianca de Meira Lopes e Thainá Lucciola Hipolito de Lima - APÊNDICE D
# Orientadores: José Antonio Moreira Xexéo, D.C. | Anderson Fernandes Pereira dos Santos,D.Sc.

# Atualizações realizadas com base na versão do Linux Mint 22.1 (Xia), respeitando as diretrizes PEP 668.
# Este código utiliza a sintaxe atualizada do Qiskit (1.x), garantindo compatibilidade moderna.
# Bibliotecas de simulação atualizadas para incluir a transpilação explícita.

# Rio de Janeiro-RJ - 29-09-26


# Qiskit 1.x - Importes essenciais
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

# 1. Registrador quântico
qreg_q = QuantumRegister(5, 'q')

# 2. Registrador clássico
creg_c = ClassicalRegister(4, 'c')

# 3. Circuito quântico
# Associa os registradores quântico e clássico ao circuito
circuito = QuantumCircuit(qreg_q, creg_c)

# Preparação do Estado Inicial
# Reseta os qubits para garantir o estado |0>
circuito.reset(qreg_q[2])
circuito.reset(qreg_q[3])
circuito.reset(qreg_q[1])
circuito.reset(qreg_q[0])

# Porta Identidade (não altera o estadi)
circuito.id(qreg_q[2])    

# Aplica a porta Pauli-X no qubit 4 para prepará-lo no estado |1> (necessário para o Oráculo)
circuito.x(qreg_q[4])

# Aplica a porta Hadamard (H) para criar uma superposição uniforme de todos os estados possíveis
circuito.h(qreg_q[0])
circuito.h(qreg_q[1])
circuito.h(qreg_q[3])
circuito.h(qreg_q[4])

# Barreira visual para separar a preparação dos dados do processamento
circuito.barrier(qreg_q[0], qreg_q[1], qreg_q[2], qreg_q[3])
circuito.barrier(qreg_q[4])

# Oráculo e reflexão de amplitude (iteração de Grover)
# As portas Toffoli (CCX) são usadas para marcar o estado desejado invertendo sua fase
circuito.ccx(qreg_q[0], qreg_q[1], qreg_q[2])
circuito.ccx(qreg_q[2], qreg_q[3], qreg_q[4])
circuito.ccx(qreg_q[0], qreg_q[1], qreg_q[2])

# Barreira visual antes da medição
circuito.barrier(qreg_q[0], qreg_q[1], qreg_q[2], qreg_q[3])

# 4. Mediação
# Colapsa o estado quântico dos qubits de busca e salva os resultados nos bits clássicos correspondentes
circuito.measure(qreg_q[0], creg_c[0])
circuito.measure(qreg_q[1], creg_c[1])
circuito.measure(qreg_q[3], creg_c[3])

# Apresenta o desenho do circuito no terminal em formato de texto
print("--- Desenho do circuito de Grover ---")
print(circuito.draw(output='text'))

# 5. Execução no simulador local (AerSimulator)
simulador = AerSimulator()

# Transpila o circuito para otimizá-lo para o simulador
circuito_compilado = transpile(circuito, simulador)

# Executa o circuito 1024 vezes (shots) para obter a distribuição estatística de probabilidade
resultado = simulador.run(circuito_compilado, shots=1024).result()

# Obtém a contagem dos resultados (o estado marcado pelo Oráculo deve ter a maior contagem)
contagens = resultado.get_counts(circuito_compilado)
print("\n--- Resultados da medição ---")
print(contagens)

# 6. Visualização gráfica (Plot)
# Gera o histograma destacando a alta probabilidade do elemento buscado
plot_histogram(contagens, color='midnightblue', title="Resultados do Algoritmo de Grover")
plt.ylabel("Quantidade de medições")

# Salva o arquivo com o gráfico ajustando as margens para não cortar o título
plt.savefig("resultado_histograma_grover.png", bbox_inches="tight")
print("\nO gráfico foi salvo com sucesso como 'resultado_histograma_grover.png'.")