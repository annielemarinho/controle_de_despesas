import sqlite3 as lite
from collections import defaultdict

DB = 'dados.db'

#Funções de Inserção
#Inserir categoria
def inserir_categoria(i):
    with lite.connect(DB) as con:
        con.execute("INSERT INTO Categoria (nome) VALUES (?)", i)

#Inserir Receitas
def inserir_receita(i):
     with lite.connect(DB) as con:
        con.execute("INSERT INTO Receitas (categoria, adicionado_em, valor) VALUES (?,?,?)", i)

#Inserir gastos
def inserir_gastos(i):
    with lite.connect(DB) as con:
        con.execute("INSERT INTO Gastos (categoria, retirado_em, valor) VALUES (?,?,?)", i)

#Funções para Deletar
#Deletar Receitas
def deletar_receitas(i):
    with lite.connect(DB) as con:
        con.execute("DELETE FROM Receitas WHERE id=?", i)

#Deletar Gastos
def deletar_gastos(i):
    with lite.connect(DB) as con:
        con.execute("DELETE FROM Gastos WHERE id=?", i)


#Funções para visualizar dados
#Ver categoria
def ver_categoria():
    with lite.connect(DB) as con:
        return con.execute("SELECT * FROM Categoria").fetchall()

#Ver receitas
def ver_receitas():
    with lite.connect(DB) as con:
        return con.execute("SELECT * FROM Receitas").fetchall()

#Ver gastos
def ver_gastos():
    with lite.connect(DB) as con:
        return con.execute("SELECT * FROM Gastos").fetchall()

#função para dados na tabela 
def tabela():
    return ver_gastos() + ver_receitas()

#função grafico bar
def bar_valores():
    receita_total  = sum(i[3] for i in ver_receitas())
    despesas_total = sum(i[3] for i in ver_gastos())
    saldo_total    = receita_total - despesas_total
    return [receita_total, despesas_total, saldo_total]

#função grafico pizza
def pie_valores():
    agrupado = defaultdict(float)
    for row in ver_gastos():
        agrupado[row[1]] += row[3]
    return [list(agrupado.keys()), list(agrupado.values())]

def porcentagem_valor():
    receita_total  = sum(i[3] for i in ver_receitas())
    despesas_total = sum(i[3] for i in ver_gastos())
    if receita_total == 0:
        return [0.0]
    return [((receita_total - despesas_total) / receita_total) * 100]

