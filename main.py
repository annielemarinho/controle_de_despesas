from tkinter import *
from tkinter import Tk, ttk
from tkinter import messagebox
from PIL import Image, ImageTk
from tkinter.ttk import Progressbar
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from tkcalendar import Calendar, DateEntry
from datetime import date
from view import inserir_categoria, inserir_receita, inserir_gastos, ver_categoria, tabela, deletar_gastos, deletar_receitas, bar_valores, pie_valores, porcentagem_valor

#cores
cor0 = "#2e2d2b"
cor1 = "#feffff"
cor2 = "#4fa882"
cor3 = "#38576b"
cor4 = "#403d3d"
cor5 = "#e06636"
cor6 = "#038cfc"
cor7 = "#3fbfb9"
cor8 = "#263238"
cor9 = "#e9edf5"


colors = ['#5588bb', '#66bbbb', '#99bb55', '#ee9944', '#444466', '#bb5555']


#criando janela
janela = Tk()
janela.title('Controle de Despesas')
janela.geometry('900x650')
janela.configure(background=cor9)
janela.resizable(width=FALSE, height=FALSE)

style = ttk.Style(janela)
style.theme_use("clam")

#criando divisões da tela
frameCima = Frame(janela, width=1043, height=50, bg=cor1, relief="flat")
frameCima.grid(row=0, column=0)

frameMeio = Frame(janela, width=1043, height=361, bg=cor1, pady=20, relief="raised")
frameMeio.grid(row=1, column=0, pady=1, padx=0, sticky=NSEW)

frameBaixo = Frame(janela, width=1043, height=300, bg=cor1,relief="flat")
frameBaixo.grid(row=2, column=0, pady=0, padx=10, sticky=NSEW)

# Trabalhando no frame cima
app_img = Image.open('logo.png')
app_img = app_img.resize((45, 45))
app_img = ImageTk.PhotoImage(app_img)

app_logo = Label(frameCima, image=app_img, text=" Controle de Despesas", width=900, compound=LEFT, padx=5, relief=RAISED, anchor=NW, font=('Verdana 20 bold'), bg=cor1, fg=cor4)
app_logo.place(x=0, y=0)

tree = None

_bar_progress   = None
_label_pct      = None
_canvas_bar     = None
_canvas_pizza   = None
_label_receita  = None
_label_despesa  = None
_label_saldo    = None

#função inserir categoria
def adicionar_categoria():
    nome = e_categoria.get()
    lista_inserir = [nome]

    for i in lista_inserir:
        if i == '':
            messagebox.showerror('Erro', 'Preencha todos os campos')
            return
    inserir_categoria(lista_inserir)
    messagebox.showinfo('Sucesso', 'Os dados foram inseridos com sucesso')

    e_categoria.delete(0, 'end')

    categoria_funcao = ver_categoria()
    categoria = []

    for i in categoria_funcao:
        categoria.append(i[1])

    combo_categoria_despesas['values'] = (categoria)


#função adicionar receitas
def adicionar_receitas():  
    nome = 'Receita'
    data = e_cal_receitas.get()
    quantia_raw = e_valor_receitas.get().strip().replace(',', '.')

    if not data or not quantia_raw:
        messagebox.showerror('Erro', 'Preencha todos os campos')
        return

    try:
        quantia = float(quantia_raw)
        if quantia <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror('Erro', 'Quantia inválida. Use apenas números positivos.')
        return

    inserir_receita([nome, data, quantia])
    messagebox.showinfo('Sucesso', 'Os dados foram inseridos com sucesso')

    e_cal_receitas.delete(0, 'end')
    e_valor_receitas.delete(0, 'end')

    mostrar_tabela()
    porcentagem()
    grafico_bar()
    resumo()
    grafico_pizza()

#função adicionar despesas
def adicionar_despesas():
    nome = combo_categoria_despesas.get().strip()
    data = e_cal_despesas.get()
    quantia_raw = e_valor_despesas.get().strip().replace(',', '.')

    if not nome or not data or not quantia_raw:
        messagebox.showerror('Erro', 'Preencha todos os campos')
        return

    try:
        quantia = float(quantia_raw)
        if quantia <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror('Erro', 'Quantia inválida. Use apenas números positivos.')
        return

    inserir_gastos([nome, data, quantia])
    messagebox.showinfo('Sucesso', 'Os dados foram inseridos com sucesso')

    combo_categoria_despesas.delete(0, 'end')
    e_cal_despesas.delete(0, 'end')
    e_valor_despesas.delete(0, 'end')

    mostrar_tabela()
    porcentagem()
    grafico_bar()
    resumo()
    grafico_pizza()

#funcao deletar
def deletar_dados():
    try:
        treev_dados = tree.focus()
        treev_dicionario = tree.item(treev_dados)
        treev_lista = treev_dicionario['values']
        
        # Verifica se algo foi selecionado para evitar erro de lista vazia
        if not treev_lista:
            messagebox.showerror('Erro', 'Selecione um dos dados na tabela')
            return

        # Extrai os dados da linha selecionada
        id_registro = treev_lista[0]      # O ID do banco de dados
        categoria_registro = treev_lista[1] # A categoria (ex: 'Receita' ou 'Aluguel')

        # Se a categoria for exatamente 'Receita', deleta da tabela de receitas
        if categoria_registro == 'Receita':
            deletar_receitas([id_registro])
        else:
            # Caso contrário (qualquer outra categoria), deleta da tabela de gastos
            deletar_gastos([id_registro])

        messagebox.showinfo('Sucesso', 'Os dados foram deletados com sucesso')

        # Atualiza todos os componentes visuais após a exclusão
        mostrar_tabela()
        porcentagem()
        grafico_bar()
        resumo()
        grafico_pizza()

    except Exception as e:
        # Mostra o erro real caso algo dê errado no processo
        messagebox.showerror('Erro', f'Não foi possível deletar: {e}')

# porcentagem
def porcentagem():
    global _bar_progress, _label_pct

    valor = porcentagem_valor()[0]

    if _bar_progress is None:
        Label(frameMeio, text="Porcentagem da receita gasta", height=1,
              anchor=NW, font=('Verdana 12'), bg=cor1, fg=cor4).place(x=7, y=5)

        style = ttk.Style()
        style.theme_use('default')
        style.configure("black.Horizontal.TProgressbar", background='#daed6b')
        style.configure("TProgressbar", thickness=25)

        _bar_progress = Progressbar(frameMeio, length=180,
                                    style='black.Horizontal.TProgressbar')
        _bar_progress.place(x=10, y=35)

        _label_pct = Label(frameMeio, text="", anchor=NW,
                           font=('Verdana 12'), bg=cor1, fg=cor4)
        _label_pct.place(x=200, y=35)

    _bar_progress['value'] = valor
    _label_pct.config(text="{:,.2f}%".format(valor))

#função para o grafico
def grafico_bar():
    global _canvas_bar

    lista_categorias = ['Rendas', 'Despesas', 'Saldo']
    lista_valores = bar_valores()

    figura = plt.Figure(figsize=(4, 3.45), dpi=60)
    ax = figura.add_subplot(111)
    ax.bar(lista_categorias, lista_valores, color=colors[:3], width=0.9)

    for c, patch in enumerate(ax.patches):
        ax.text(patch.get_x() + patch.get_width() / 2,
                patch.get_height() + 100,
                "{:,.0f}".format(lista_valores[c]),
                fontsize=17, fontstyle='italic', ha='center', va='bottom')

    ax.tick_params(axis='x', labelsize=12)
    ax.patch.set_facecolor('#ffffff')
    for spine in ['top', 'right', 'left']:
        ax.spines[spine].set_visible(False)
    ax.spines['bottom'].set_color('#CCCCCC')
    ax.tick_params(bottom=False, left=False)
    ax.set_axisbelow(True)
    ax.yaxis.grid(True, color='#EEEEEE')
    ax.xaxis.grid(False)

    if _canvas_bar is not None:
        _canvas_bar.get_tk_widget().destroy()

    _canvas_bar = FigureCanvasTkAgg(figura, frameMeio)
    _canvas_bar.get_tk_widget().place(x=10, y=70)

#painel de resumo
def resumo():
    global _label_receita, _label_despesa, _label_saldo

    receita_total, despesas_total, saldo_total = bar_valores()
    cor_saldo = cor6 if saldo_total >= 0 else cor5

    if _label_receita is None:
        Label(frameMeio, text="TOTAL RENDA MENSAL", anchor=NW,
              font=('Verdana 12'), bg=cor1, fg=cor6).place(x=300, y=40)
        Frame(frameMeio, width=230, height=1, bg=cor4).place(x=300, y=60)

        Label(frameMeio, text="TOTAL DESPESAS MENSAIS", anchor=NW,
              font=('Verdana 12'), bg=cor1, fg=cor6).place(x=300, y=110)
        Frame(frameMeio, width=230, height=1, bg=cor4).place(x=300, y=130)

        Label(frameMeio, text="TOTAL SALDO DA CAIXA", anchor=NW,
              font=('Verdana 12'), bg=cor1, fg=cor6).place(x=300, y=180)
        Frame(frameMeio, width=230, height=1, bg=cor4).place(x=300, y=200)

        _label_receita = Label(frameMeio, text="", anchor=NW,
                               font=('Verdana 16'), bg=cor1, fg=cor4)
        _label_receita.place(x=300, y=65)

        _label_despesa = Label(frameMeio, text="", anchor=NW,
                               font=('Verdana 16'), bg=cor1, fg=cor4)
        _label_despesa.place(x=300, y=135)

        _label_saldo = Label(frameMeio, text="", anchor=NW,
                             font=('Verdana 16'), bg=cor1, fg=cor4)
        _label_saldo.place(x=300, y=205)

    _label_receita.config(text=f"R$ {receita_total:,.2f}")
    _label_despesa.config(text=f"R$ {despesas_total:,.2f}")
    _label_saldo.config(text=f"R$ {saldo_total:,.2f}", fg=cor_saldo)

#grafico pizza
def grafico_pizza():
    global _canvas_pizza

    categorias, valores = pie_valores()

    if not valores:
        return

    cores = ['#4e79a7', '#76b7b2', '#9cba5a']

    fig = Figure(figsize=(4.8, 4), dpi=75)
    ax = fig.add_subplot(111)

    wedges, _, _ = ax.pie(valores, autopct='%1.1f%%', startangle=90,
                          colors=cores, wedgeprops=dict(width=0.3))
    ax.axis('equal')
    fig.subplots_adjust(right=0.7)
    ax.legend(wedges, categorias, loc='center left',
              bbox_to_anchor=(1, 0.5), fontsize=10, frameon=False)

    if _canvas_pizza is not None:
        _canvas_pizza.get_tk_widget().destroy()

    _canvas_pizza = FigureCanvasTkAgg(fig, frameMeio)
    _canvas_pizza.get_tk_widget().place(x=540, y=20)


porcentagem()
grafico_bar()
resumo()
grafico_pizza()

#Criando frames dentro do FrameBaixo
frame_renda = Frame(frameBaixo, width=300, height=250, bg=cor1, relief="flat")
frame_renda.grid(row=0, column=0, sticky=NSEW)

frame_operacoes = Frame(frameBaixo, width=220, height=250, bg=cor1, relief="flat")
frame_operacoes.grid(row=0, column=1, padx=5, sticky=NSEW)

frame_configuracao = Frame(frameBaixo, width=220, height=250, bg=cor1, relief="flat")
frame_configuracao.grid(row=0, column=2, padx=5, sticky=NSEW)


#tabela renda mensal
app_tabela = Label(frameMeio, text=" Tabela Receitas e Despesas", anchor=NW, font=('Verdana 12'), bg=cor1, fg=cor4)
app_tabela.place(x=5, y=309)

#função para mostrar tabela
def mostrar_tabela():
    global tree

    if tree is not None:
        tree.destroy()

    tabela_head = ['#Id', 'Categoria', 'Data', 'Quantia']
    lista_itens = tabela()

    tree = ttk.Treeview(frame_renda, selectmode="extended", columns=tabela_head, show="headings")
    vsb = ttk.Scrollbar(frame_renda, orient="vertical", command=tree.yview)
    hsb = ttk.Scrollbar(frame_renda, orient="horizontal", command=tree.xview)

    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    tree.grid(column=0, row=0, sticky='nsew')
    vsb.grid(column=1, row=0, sticky='ns')
    hsb.grid(column=0, row=1, sticky='ew')

    hd = ["center", "center", "center", "center"]
    h = [30, 100, 100, 100]

    for n, col in enumerate(tabela_head):
        tree.heading(col, text=col.title(), anchor=CENTER)
        tree.column(col, width=h[n], anchor=hd[n])

    for item in lista_itens:
        tree.insert('', 'end', values=item)

mostrar_tabela()

#configuraçoes despesas
l_info = Label(frame_operacoes, text='Insira novas despesas', height=1, anchor=NW, font=('Verdana 10 bold'), bg=cor1, fg=cor4)
l_info.place(x=10, y=10)

#categoria
l_categoria = Label(frame_operacoes, text='Categoria', height=1, anchor=NW, font=('Ivy 10'), bg=cor1, fg=cor4)
l_categoria.place(x=10, y=40)

#pegando categorias
categoria_funcao = ver_categoria()
categoria = []

for i in categoria_funcao:
    categoria.append(i[1])

combo_categoria_despesas = ttk.Combobox(frame_operacoes, width=10, font=('Ivy 10'))
combo_categoria_despesas['values'] = (categoria)
combo_categoria_despesas.place(x=110, y=41)

#despesas
l_cal_despesas = Label(frame_operacoes, text='Data', height=1, anchor=NW, font=('Ivy 10'), bg=cor1, fg=cor4)
l_cal_despesas.place(x=10, y=70)
e_cal_despesas = DateEntry(frame_operacoes, width=12, background='darkblues', foreground='white', borderwidth=2, year=2026)
e_cal_despesas.place(x=110, y=71)

#valor
l_valor_despesas = Label(frame_operacoes, text='Quantia Total', height=1, anchor=NW, font=('Ivy 10'), bg=cor1, fg=cor4)
l_valor_despesas.place(x=10, y=100)
e_valor_despesas = Entry(frame_operacoes, width=14, justify='left', relief='solid')
e_valor_despesas.place(x=110, y=101)

#botao inserir
img_add_despesas = Image.open('add.png')
img_add_despesas = img_add_despesas.resize((17, 17))
img_add_despesas = ImageTk.PhotoImage(img_add_despesas)
botao_inserir_despesas = Button(frame_operacoes, command=adicionar_despesas, image=img_add_despesas, text=" Adicionar".upper(), width=80, compound=LEFT, anchor=NW, font=('Ivy 7 bold'), bg=cor1, fg=cor0, overrelief=RIDGE)
botao_inserir_despesas.place(x=110, y=131)

#botao excluir
l_excluir = Label(frame_operacoes, text='Excluir ação', height=1, anchor=NW, font=('Ivy 10'), bg=cor1, fg=cor4)
l_excluir.place(x=10, y=190)

img_delete = Image.open('delete.png')
img_delete = img_delete.resize((17, 17))
img_delete = ImageTk.PhotoImage(img_delete)
botao_deletar = Button(frame_operacoes, command= deletar_dados, image=img_delete, text=" Deletar".upper(), width=80, compound=LEFT, anchor=NW, font=('Ivy 7 bold'), bg=cor1, fg=cor0, overrelief=RIDGE)
botao_deletar.place(x=110, y=190)

#configurando receitas
l_info = Label(frame_configuracao, text='Insira novas receitas', height=1, anchor=NW, font=('Verdana 10 bold'), bg=cor1, fg=cor4)
l_info.place(x=10, y=10)

#calendario
l_cal_receitas = Label(frame_configuracao, text='Data', height=1, anchor=NW, font=('Ivy 10'), bg=cor1, fg=cor4)
l_cal_receitas.place(x=10, y=40)
e_cal_receitas = DateEntry(frame_configuracao, width=12, background='darkblues', foreground='white', borderwidth=2, year=2026)
e_cal_receitas.place(x=110, y=41)

#valor
l_valor_receitas = Label(frame_configuracao, text='Quantia Total', height=1, anchor=NW, font=('Ivy 10'), bg=cor1, fg=cor4)
l_valor_receitas.place(x=10, y=70)
e_valor_receitas = Entry(frame_configuracao, width=14, justify='left', relief='solid')
e_valor_receitas.place(x=110, y=71)

#botao inserir
img_add_receitas = Image.open('add.png')
img_add_receitas = img_add_receitas.resize((17, 17))
img_add_receitas = ImageTk.PhotoImage(img_add_receitas)
botao_inserir_receitas = Button(frame_configuracao,command=adicionar_receitas, image=img_add_receitas, text=" Adicionar".upper(), width=80, compound=LEFT, anchor=NW, font=('Ivy 7 bold'), bg=cor1, fg=cor0, overrelief=RIDGE)
botao_inserir_receitas.place(x=110, y=111)

#configurando nova categoria
l_info = Label(frame_configuracao, text='Categoria', height=1, anchor=NW, font=('Ivy 10 bold'), bg=cor1, fg=cor4)
l_info.place(x=10, y=160)

e_categoria = Entry(frame_configuracao, width=14, justify='left', relief='solid')
e_categoria.place(x=110, y=160)

#botao inserir
img_add_categoria = Image.open('add.png')
img_add_categoria = img_add_categoria.resize((17, 17))
img_add_categoria = ImageTk.PhotoImage(img_add_categoria)
botao_inserir_categoria = Button(frame_configuracao,command=adicionar_categoria, image=img_add_categoria, text=" Adicionar".upper(), width=80, compound=LEFT, anchor=NW, font=('Ivy 7 bold'), bg=cor1, fg=cor0, overrelief=RIDGE)
botao_inserir_categoria.place(x=110, y=190)

janela.mainloop()

