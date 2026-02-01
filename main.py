import sqlite3
from datetime import datetime


# Conectar (ou criar) banco de dados
conn = sqlite3.connect("info.db")
cursor = conn.cursor()

cursor.execute('DROP TABLE IF EXISTS treinos;') # Tirar depois dos testes
def criar_tabela():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS treinos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    exercicio TEXT NOT NULL,
    peso REAL,
    repeticoes FLOAT,
    rir FLOAT,
    data TEXT
)
""")
conn.commit()
criar_tabela()

def adicionar_treino(exercicio, peso, repeticoes, rir, data=None):
    if not data:
        data_formatada = datetime.now().strftime("%d/%m/%Y") # Formatação dia/mês/ano
    else:
        try:
            data_obj = datetime.strptime(data, "%d/%m/%Y")
            data_formatada = data_obj.strftime("%d/%m/%Y")
        except ValueError:
            print("Data inválida! Use o formato DD/MM/AAAA.")
            return

    cursor.execute("""
    INSERT INTO treinos (exercicio, peso, repeticoes, rir, data)
    VALUES (?, ?, ?, ?, ?)
    """, (exercicio, peso, repeticoes, rir, data_formatada)) # "?" é pra segurança do código, pra evitar exploits do sql
    conn.commit()
    print("Exercício registrado com sucesso!")

def listar_treinos():
    cursor.execute("SELECT * FROM treinos")
    treinos = cursor.fetchall()

    if not treinos:
        print("Nenhum exercício registrado.")
        return

    print("Histórico de Exercícios:\n")
    for treino in treinos:
        print(f"""
ID: {treino[0]}
Exercício: {treino[1]}
Peso: {treino[2]} kg
Repetições: {treino[3]} 
RIR (Repetições na reserva): {treino[4]} reps. na reserva
Data: {treino[5]}
-----------------------
""")

def listar_treinos_por_data(data):
    try:
        data_obj = datetime.strptime(data, "%d/%m/%Y")
        data_formatada = data_obj.strftime("%d/%m/%Y")
    except ValueError:
        print("Data inválida! Use o formato DD/MM/AAAA.")
        return

    cursor.execute("""
        SELECT * FROM treinos WHERE data = ?
    """, (data_formatada,))

    treinos = cursor.fetchall()

    if not treinos:
        print("Nenhum exercício encontrado para essa data.")
        return

    print(f"\nTreinos em {data_formatada}:\n")
    for treino in treinos:
        print(f"""
ID: {treino[0]}
Exercício: {treino[1]}
Peso: {treino[2]} kg
Repetições: {treino[3]}
RIR (Repetições na reserva): {treino[4]} reps. na reserva
-----------------------
""")
        
def deletar_exercicio(deletar):
    cursor.execute("""
        DELETE FROM treinos WHERE id = ?
    """, (deletar,))
    if cursor.rowcount >=1:
        print(f"Exercício com o ID:{deletar} deletado com sucesso.")
    else:
        print(f'Nenhum exercício encontrado com o ID: {deletar}.')
    conn.commit()

# Menu simples
while True:
    print("""
1 - Adicionar exercício
2 - Listar exercícios
3 - Listar exercícios por data
4 - Deletar exercício
5 - Sair
""")
    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        exercicio = input("Nome do exercício: ")
        peso = float(input("Peso (kg): "))
        repeticoes = float(input("Repetições: "))
        rir = float(input("Repetiçoes na reserva: "))
        data = input("Data (DD/MM/AAAA) (Use enter para data atual): ").strip()
        adicionar_treino(exercicio, peso, repeticoes, rir, data)

    elif opcao == "2":
        listar_treinos()

    elif opcao == "3":
        data = input('Digite uma data no formato dia/mês/ano: ').strip()
        listar_treinos_por_data(data)

    elif opcao == "4":
        deletar = (input('Escolha um exercício para excluir:'))
        try:
            deletar_id = int(deletar)
            deletar_exercicio(deletar_id)
        except ValueError:
            print('ID desconhecido, digite um ID válido.')
    
    elif opcao == "5":
        print("Encerrando...")
        break

    else:
        print("Opção inválida!")

conn.close()
