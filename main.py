from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
import sqlite3

global existe
existe = False

class Principal(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id_edicao = 0
    
    def buscar(self):
        self.id_edicao = self.ids.id_busca.text
        conn = sqlite3.connect('servidor.db')
        cursor = conn.cursor()
        cursor.execute('''SELECT nome, curso, idade FROM aluno WHERE id = {}'''.format(self.id_edicao))

        global existe

        if cursor.fetchall():

            self.ids.mensagem.text = 'FOUND'
            existe = True

            conn = sqlite3.connect('servidor.db')
            cursor = conn.cursor()
            cursor.execute('''SELECT nome FROM aluno WHERE id = {}'''.format(self.id_edicao))
            self.ids.nome_aluno.text = cursor.fetchone()[0]
            conn.close()

            conn = sqlite3.connect('servidor.db')
            cursor = conn.cursor()
            cursor.execute('''SELECT curso FROM aluno WHERE id = {}'''.format(self.id_edicao))
            self.ids.curso_aluno.text = cursor.fetchone()[0]
            conn.close()

            conn = sqlite3.connect('servidor.db')
            cursor = conn.cursor()
            cursor.execute('''SELECT idade FROM aluno WHERE id = {}'''.format(self.id_edicao))
            self.ids.idade_aluno.text = str(cursor.fetchone()[0])
            conn.close()

        else:
            self.ids.mensagem.text = 'ABSENT'
            existe = False
            self.ids.nome_aluno.text = ''
            self.ids.curso_aluno.text = ''
            self.ids.idade_aluno.text = ''
        

        conn.close()
    
    def salvar(self):
        global existe 

        if existe == True:
            conn = sqlite3.connect('servidor.db')
            cursor = conn.cursor()
            cursor.execute('''UPDATE aluno SET nome = ?, curso = ?, idade = ? WHERE id = ?''', (self.ids.nome_aluno.text, self.ids.curso_aluno.text, self.ids.idade_aluno.text, self.id_edicao))
            conn.commit()
            self.ids.mensagem.text = 'UPDATED'
            conn.close()

        if existe == False:
            conn = sqlite3.connect('servidor.db')
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO aluno(nome, curso, idade) VALUES (?, ?, ?)''', (self.ids.nome_aluno.text, self.ids.curso_aluno.text, self.ids.idade_aluno.text))
            conn.commit()
            self.ids.mensagem.text = 'SUCCESSFULLY REGISTERED'
            conn.close()
        
        
class InterfaceApp(App):
    def build(self):
        Window.size = (400,500)
        return Principal()
    
InterfaceApp().run()
