# Atividade baseado no tutorial atualizado do artigo Intrudução à Programação de Computadores Quânticos
# 38º Jornada de Atualização em Informática (JAI)
# XXXIX Congresso da Sociedade Brasileira de Computação
# Belém - PA, 15 a 18 de julho de 2019
# Autoria: Renato Portugal, Franklin L. Marquezino

# Atualizações realizadas com base na versão do inux Mint 22.1 (Xia), respeitando as diretrizes PEP 668
# Este código utiliza a sintax atualizada do Qiskit (1.x), substituindo comandos antigos como "execute"

# Rio de Janeiro-RJ - 26-09-26

# Qiskit 1.x - Importes
from qiskit import QuantumCircuit , transpile
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

# 1. Circuito quântico
# Cria um circuito com 2 qubits e 2 bits clássicos
circuito = QuantumCircuit(2, 2)

# 2. Porta lógica quântica
# Aplica a porta Hadamard (H) no qubit 0 (Superposição)
circuito.h(0)

# Aplica a porta Cnot (CX) (controle 0, alvo 1) - Emaranhamento
circuito.cx(0, 1)

# 3. Mediação
# Mede os qubits 0 e 1, salvando nos bits clássicos 0 e 1
circuito.measure([0, 1], [0, 1])

# Apresenta o desenho do circuito no terminal
print("--- Desenho do Circulo ---")
print(circuito.draw(output='text'))

# 4. Execução no simulador local
simulador = AerSimulator()

# Transpila o circuito para o simulador
circuito_compilado = transpile(circuito, simulador)

# Executa o circuito 1000 vezes (shots)
job = simulador.run(circuito_compilado, shots=1000)
resultado = job.result()

# Obtem a contagem dos resultados
contagens = resultado.get_counts(circuito_compilado)
print("\n--- Resultados da Medição ---")
print(contagens)

# 5. Visualização (Plot)
plot_histogram(contagens)
plt.title("Resultados do estado de Bell")
plt.ylabel("Quantidade de medições")
plt.savefig("resultado_histograma.png", bbox_inches="tight")
print("\nGráfico salvo como 'resultado_histograma.png'.")




