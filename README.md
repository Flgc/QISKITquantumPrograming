# QISKITquantumPrograming

Repositório dedicado aos estudos práticos e desenvolvimento de algoritmos de computação quântica utilizando o ecossistema **Qiskit 1.x**.

O projeto foi estruturado com base nos conceitos teóricos de Renato Portugal (2019) e adaptado para as práticas de programação quântica modernas, sendo amplamente testado e otimizado para execução local.

## 🚀 Tecnologias utilizadas

- **Sistema operacional:** Linux Mint 22.1 (Xia) / Ubuntu 24.04 LTS
- **Linguagem:** Python 3.12.3
- **Framework quântico:** Qiskit e Qiskit-Aer (Simulador)
- **Visualização:** Matplotlib
- **IDE:** Visual Studio Code

## 💻 Instalação e configuração

Devido às restrições de segurança do Python no Linux Mint 22.1 (PEP 668), é estritamente recomendado rodar o projeto dentro de um ambiente virtual.

**1. Instale as dependências de sistema:**

```bash
sudo apt update
sudo apt install python3-venv python3-pip -y
```

**2. Crie o ambiente virtual:**

```bash
python3 -m venv qenv
```

**3. Ative o ambiente virtual:**

```bash
source qenv/bin/activate
```

_(Nota: O ambiente `qenv` deve ser reativado sempre que abrir um novo terminal para rodar os scripts deste repositório. Durante sua utilização o nome do ambiente permanecerá no início da linha do terminal)._

**4. Instale as bibliotecas requeridas:**

```bash
pip install qiskit qiskit-aer matplotlib
```

## 📂 Estrutura do projeto

Este repositório contém a implementação de diferentes circuitos quânticos:

- **`meu_primeiro_circuito.py` (Estado de Bell):** Demonstra os fenômenos de superposição (Porta Hadamard) e emaranhamento quântico (Porta CNOT) entre dois qubits, retornando resultados estatísticos próximos a 50% para `00` e `11`.

- **Algoritmo de Grover:** Implementação de busca em banco de dados não ordenado utilizando oráculos e reflexão de amplitude.

- **Algoritmo de Shor:** Rotina de fatoração de números baseada no cálculo da ordem quântica.

**5. Execute o projeto:**

```bash
python3 meu_primeiro_circuito.py

```

![Execução](Executa.png)

**6. Encerre o ambiente:**

Após terminar, finalize o ambiente virtual.

```bash
deactivate

```

![Histograma do Estado de Bell](resultado_histograma.png)

## 🛠️ Resolução de problemas comuns (Troubleshooting)

- **Erro `ModuleNotFoundError: No module named 'qiskit'`:** Isso ocorre se a pasta do projeto for renomeada ou movida. Ambientes virtuais quebram ao mudar de caminho. Solução: Apague a pasta `qenv`, crie-a novamente e reinstale as dependências.

- **Erro no método `get_counts`:** Certifique-se de grafar corretamente o método. O Qiskit não reconhece variações como `get_conts`.

- **Erro de importação na visualização:** No Qiskit moderno (1.x), a importação de gráficos ocorre via pacote principal (`from qiskit.visualization import plot_histogram`) e não pelo módulo `qiskit_aer`.

---

_Desenvolvido durante estudos de implementação de computação quântica._
