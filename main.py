from tkinter import *
from tkinter import Tk, ttk
from PIL import Image, ImageTk
from tkinter.ttk import Progressbar
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.figure import Figure


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
janela.title()
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

# porcentagem
def porcentagem():
    l_nome = Label(frameMeio, text="Porcentagem da receita gasta", height=1, anchor=NW, font=('Verdana 12'), bg=cor1, fg=cor4)
    l_nome.place(x=7, y=5)

    style = ttk.Style()
    style.theme_use('default')
    style.configure("black.Horizontal.TProgressbar", background='#daed6b')
    style.configure("TProgressbar", thickness=25)
    bar = Progressbar(frameMeio, length=180, style='black.Horizontal.TProgressbar')
    bar.place(x=10, y=35)
    bar['value'] = 50

    valor = 50
    l_porcentagem = Label(frameMeio, text="{:,.2f}%".format(valor), anchor=NW, font=('Verdana 12'), bg=cor1, fg=cor4)
    l_porcentagem.place(x=200, y=35)

#função para o grafico
def grafico_bar():
    lista_categorias = ['Rendas', 'Despesas', 'Saldo']
    lista_valores = [3000, 2000, 6236]

    figura = plt.Figure(figsize=(4, 3.45), dpi=60)
    ax = figura.add_subplot(111)

    ax.bar(lista_categorias, lista_valores, color=colors[:3], width=0.9)

    c = 0

    for i in ax.patches:
        ax.text(i.get_x() + i.get_width()/2,
                i.get_height() + 100,
                str("{:,.0f}".format(lista_valores[c])), fontsize=17, fontstyle='italic', ha='center', va='bottom')              
        c += 1       

    ax.tick_params(axis='x', labelsize=12)

    ax.patch.set_facecolor('#ffffff')
    ax.spines['bottom'].set_color('#CCCCCC')
    ax.spines['bottom'].set_linewidth(1)
    ax.spines['right'].set_linewidth(0)
    ax.spines['top'].set_linewidth(0)
    ax.spines['left'].set_color('#CCCCCC')
    ax.spines['left'].set_linewidth(1)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.tick_params(bottom=False, left=False)
    ax.set_axisbelow(True)
    ax.yaxis.grid(True, color='#EEEEEE')
    ax.xaxis.grid(False)

    canva = FigureCanvasTkAgg(figura, frameMeio)
    canva.get_tk_widget().place(x=10, y=70)


porcentagem()
grafico_bar()
janela.mainloop()

