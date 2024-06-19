from datetime import datetime, timedelta

class Livro:
    def __init__(self, id, titulo, autores, ano, ISBN):
        self.titulo = titulo
        self.autores = autores
        self.ano = ano
        self.id = id
        self.emprestado = False
        self.ISBN = ISBN



class Usuario:
    def __init__(self, Registro_Academico, nome, email):
        self.nome = nome
        self.email = email
        self.Registro_Academico = Registro_Academico
        


class Emprestimo:
    
    def __init__(self,dataInicial,dataFinal,Livro, Usuario):
        self.dataInicial = dataInicial
        self.dataFinal = dataFinal
        self.dia_que_foi_devolvido = None
        self.Livro = Livro
        self.Usuario = Usuario
        
    def devolvido(self,data):
        self.dia_que_foi_devolvido = data
        





class Historico:
    def __init__(self, Registro_Academico):
        self.Registro_Academico = Registro_Academico
        self.lista_datas_livrosEmprestados = {}  # dicionário contendo data do empréstimo e livro {'2024-06-12':'quimica organica'}





class Biblioteca:
    def __init__(self):
        self.livros = []  # [Livro :: livros]
        self.exemplares = {}  # {ISBN : [livros]}
        self.usuarios = []
        self.emprestimos = [] # todos os emprestimos realizados na biblioteca
    
    def add_Livro(self, Livro):
        if not Livro.ISBN in [liv.ISBN for liv in self.livros]:
            self.livros.append(Livro)
        
        self.add_exemplar(Livro)
        
    def add_exemplar(self, Livro):
        
        if Livro.ISBN not in self.exemplares.keys():
            self.exemplares[Livro.ISBN] = [Livro]
        
        else:
            if Livro not in self.exemplares[Livro.ISBN]:
                self.exemplares[Livro.ISBN].append(Livro)
            else:
                print("Livro já cadastrado!")
        
    def get_Livros(self):
        return self.livros
        
    def get_exemplares(self, Livro):
        return self.exemplares[Livro.titulo]
    
    def listar_livros(self):
        print("-" * 50)
        print("Livros:")
        for livro in self.livros:
            print(f"Título: {livro.titulo}  Autores: {livro.autores}   Ano: {livro.ano}   ISBN: {livro.ISBN}")
        print(f"\nTotal de livros = {len(self.livros)}")
        print("-" * 50)
    
    def listar_exemplares(self, Livro):
        if Livro.ISBN in self.exemplares:
            print(f"Exemplares do livro {Livro.titulo}:")
            for livro in self.exemplares[Livro.ISBN]:
                print(f"Título: {livro.titulo} | Exemplar ID: {livro.id} | Emprestado: {'Sim' if livro.emprestado else 'Não'}")
            print(f"\nTotal de exemplares = {len(self.exemplares[Livro.ISBN])}")
        else:
            print("Livro não cadastrado!\n")
            
    
    def cadastrarUsuario(self,Usuario):
        self.usuarios.append(Usuario)
    
    def emprestarLivro(self,dataInicial,Livro,Usuario):
        
        prazo = 7 #7 dias para devolver
        emprestimo = Emprestimo(dataInicial,dataInicial+timedelta(days=prazo),Livro,Usuario)
        self.emprestimos.append(emprestimo)
        Livro.emprestado = True
    
    def devolverLivro(self,Livro,dia):
        Livro.emprestado = False
        
        for emprestimo in self.emprestimos:
            if emprestimo.Livro == Livro:
                emprestimo.dia_que_foi_devolvido = dia
    
    

# Teste das funcionalidades
biblioteca = Biblioteca()

# Instanciando 15 livros diferentes
livros = [
    Livro(0, "quimica organica", "eu e mais 2", 2024, 1),
    Livro(0, "quimica radical", "eu e mais 2", 2022, 2),
    Livro(1, "quimica organica", "eu e mais 2", 2024, 3),
    Livro(0, "fisica basica", "autor X", 2021, 4),
    Livro(0, "matematica pura", "autor Y", 2020, 5),
    Livro(0, "biologia geral", "autor Z", 2019, 6),
    Livro(0, "historia do mundo", "autor A", 2018, 7),
    Livro(0, "geografia fisica", "autor B", 2017, 8),
    Livro(0, "programacao em Python", "autor C", 2023, 9),
    Livro(0, "inteligencia artificial", "autor D", 2023, 10),
    Livro(0, "algoritmos", "autor E", 2022, 11),
    Livro(0, "engenharia de software", "autor F", 2021, 12),
    Livro(0, "redes de computadores", "autor G", 2020, 13),
    Livro(0, "sistemas operacionais", "autor H", 2019, 14),
    Livro(0, "banco de dados", "autor I", 2018, 15)
]

# Adicionando 3 exemplares de cada livro na biblioteca
for livro in livros:
    
    for id in range(3):
        copia = Livro(id,livro.titulo,livro.autores,livro.ano,livro.ISBN)
        biblioteca.add_Livro(copia)
        

# Listar todos os livros na biblioteca
biblioteca.listar_livros()



usuario1 = Usuario(101,"Lucas","apapa")
biblioteca.cadastrarUsuario(usuario1)
biblioteca.emprestarLivro(datetime(2024,6,18), biblioteca.exemplares[6][0], usuario1)

# Listar exemplares de um dos livros
biblioteca.listar_exemplares(livros[5])
