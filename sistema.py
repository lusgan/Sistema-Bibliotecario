# -*- coding: utf-8 -*-
"""
Created on Mon May 27 20:33:01 2024

@author: balbi
"""

class Livro():
    
    def __init__(self,titulo,autores,ano,cod = 1):
        self.titulo = titulo
        self.autores = autores
        self.ano = ano
        self.cod = cod
        self.emprestado = False
        
        
        
class Usuario():
    
    def __init__(self,Registro_Academico):
        self.nome
        self.email
        self.Registro_Academico = Registro_Academico
        

class Historico():
    def __init__(self,Registro_Academico):
        self.Registro_Academico = Registro_Academico
        self.lista_datas_livrosEmprestados  #dicionario contendo data do emprestimo, e livro {'2024-06-12':'quimica organica'}
        

class Biblioteca:
    def __init__(self):
        self.livros = []  #[Livro :: livros]
        self.exemplares = {}  # {titulo : [livros]}
    
    #adiciona um livro na biblioteca, e adiciona o mesmo na lista de exemplares
    def add_Livro(self,Livro):
        
        if not Livro in self.livros : 
            self.livros.append(Livro)
        
        self.add_exemplar(Livro)
        
    
    def add_exemplar(self,Livro):
        
        if not Livro.titulo in self.exemplares.keys() : self.exemplares[Livro.titulo] = [Livro]  
        
        elif Livro.titulo in self.exemplares.keys():
            lista = self.exemplares[Livro.titulo]
            if Livro.cod in [livro.cod for livro in lista]: 
                print("Livro ja cadastrado!")
                return
            
            lista.append(Livro)
        
    def get_Livros(self):
        return self.livros
        
    def get_exemplares(self,Livro):
        return self.exemplares[Livro.titulo]
    
    def listar_livros(self):
        print("Livros:")
        for livro in self.livros:
            print(f"titulo: {livro.titulo}  autores: {livro.autores}   ano: {livro.ano}")
            
        print(f"\nTotal de livros = {len(self.livros)}\n")
            
    
    def listar_exemplares(self,Livro):
        if Livro.titulo in self.exemplares.keys():
           print("exemplares:")
           for exemplar in self.exemplares[Livro.titulo]:
               print(f"titulo: {exemplar.titulo}  cod: {exemplar.cod}")
            
           print(f"\nquantidade de exemplares = {len(self.exemplares[Livro.titulo])}")
        
        else:
            print("Livro nao cadastrado!\n")
                
            
            
            
            
            
            
biblioteca = Biblioteca()
livro = Livro("quimica organica", "eu e mais 2", 2024)
livro2 = Livro("quimica radical", "eu e mais 2", 2022)
livro3 = Livro("quimica organica", "eu e mais 2", 2024,2)
biblioteca.add_Livro(livro)
biblioteca.add_Livro(livro2)
biblioteca.add_Livro(livro3)

biblioteca.listar_livros()
biblioteca.listar_exemplares(livro3)





    



