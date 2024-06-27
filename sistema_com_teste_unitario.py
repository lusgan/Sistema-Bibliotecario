import unittest
from datetime import datetime, timedelta

# Classes da Biblioteca
class Livro:
    def __init__(self, id, titulo, autores, ano, ISBN):
        self.id = id
        self.titulo = titulo
        self.autores = autores
        self.ano = ano
        self.ISBN = ISBN
        self.emprestado = False

    def esta_emprestado(self):
        return self.emprestado

class Usuario:
    def __init__(self, Registro_Academico, nome, email):
        self.Registro_Academico = Registro_Academico
        self.nome = nome
        self.email = email
        self.data_ultima_penalidade = None
        self.historico_de_emprestimos = []
        self.historico_de_penalidades = []

    def penalizar(self, data_de_hoje, emprestimo):
        self.data_ultima_penalidade = data_de_hoje + timedelta(days=15)
        self.historico_de_penalidades.append(emprestimo)
        print(f"Usuário penalizado até {self.data_ultima_penalidade}")

    def possui_penalidade(self, data):
        return self.data_ultima_penalidade is not None and data <= self.data_ultima_penalidade

class Emprestimo:
    def __init__(self, id_emprestimo, data_hoje, livro, usuario):
        self.id = id_emprestimo
        self.dataInicial = data_hoje
        self.dataFinal = data_hoje + timedelta(days=7)
        self.dia_que_foi_devolvido = None
        self.livro = livro
        self.usuario = usuario

    def devolver(self, data):
        self.livro.emprestado = False
        self.dia_que_foi_devolvido = data
        if data > self.dataFinal:
            self.usuario.penalizar(data, self)

class Biblioteca:
    def __init__(self):
        self.catalogo = {}
        self.usuarios = []
        self.emprestimos = []

    def adicionar_livro(self, livro):
        if livro.ISBN not in self.catalogo:
            self.catalogo[livro.ISBN] = [livro]
        else:
            self.catalogo[livro.ISBN].append(livro)

    def listar_livros(self):
        print("-" * 50)
        print("Catálogo de Livros:")
        for isbn, livros in self.catalogo.items():
            for livro in livros:
                print(f"Título: {livro.titulo}  Autores: {livro.autores}   Ano: {livro.ano}   ISBN: {livro.ISBN}")
        print(f"\nTotal de livros = {sum(len(livros) for livros in self.catalogo.values())}")
        print("-" * 50)

    def cadastrar_usuario(self, usuario):
        self.usuarios.append(usuario)

    def emprestar_livro(self, livro, usuario, data_hoje):
        if usuario.possui_penalidade(data_hoje):
            print(f"Usuário {usuario.nome} está sob penalidade. Empréstimo não realizado.")
            return False

        exemplares_disponiveis = self.catalogo.get(livro.ISBN, [])
        exemplar_emprestado = None

        for exemplar in exemplares_disponiveis:
            if not exemplar.emprestado:
                exemplar_emprestado = exemplar
                break

        if exemplar_emprestado:
            emprestimo = Emprestimo(len(self.emprestimos), data_hoje, exemplar_emprestado, usuario)
            self.emprestimos.append(emprestimo)
            exemplar_emprestado.emprestado = True
            usuario.historico_de_emprestimos.append(emprestimo)
            print(f"Livro '{livro.titulo}' emprestado para {usuario.nome}. Devolução até {emprestimo.dataFinal}.")
            return True
        else:
            print(f"Não há exemplares disponíveis do livro '{livro.titulo}'. Empréstimo não realizado.")
            return False

    def devolver_livro(self, livro, data):
        for emprestimo in self.emprestimos:
            if emprestimo.livro == livro:
                emprestimo.devolver(data)
                print(f"Livro '{livro.titulo}' devolvido.")

# Testes unitários
class TestBiblioteca(unittest.TestCase):

    def setUp(self):
        self.biblioteca = Biblioteca()

        # Criação de alguns livros para o catálogo
        self.livro1 = Livro(0, "Química Orgânica", "Eu e mais 2", 2024, 1)
        self.livro2 = Livro(1, "Química Radical", "Eu e mais 2", 2022, 2)
        self.livro3 = Livro(2, "Física Básica", "Autor X", 2021, 3)

        # Adicionando exemplares ao catálogo
        for livro in [self.livro1, self.livro2, self.livro3]:
            for id in range(3):
                copia = Livro(id, livro.titulo, livro.autores, livro.ano, livro.ISBN)
                self.biblioteca.adicionar_livro(copia)

        # Criação de um usuário para os testes
        self.usuario = Usuario(101, "Lucas", "apapa@example.com")
        self.biblioteca.cadastrar_usuario(self.usuario)

    def test_adicionar_livro(self):
        novo_livro = Livro(3, "Introdução à Biologia", "Autor Z", 2023, 4)
        self.biblioteca.adicionar_livro(novo_livro)
        self.assertIn(novo_livro, self.biblioteca.catalogo[novo_livro.ISBN])

    def test_emprestar_livro_sucesso(self):
        livro_emprestado = self.livro1
        self.assertTrue(self.biblioteca.emprestar_livro(livro_emprestado, self.usuario, datetime(2024, 6, 18)))
        self.assertTrue(livro_emprestado.esta_emprestado())

    def test_emprestar_livro_sem_exemplares(self):
        livro_sem_exemplares = Livro(3, "Livro Inexistente", "Autor Y", 2023, 4)
        self.assertFalse(self.biblioteca.emprestar_livro(livro_sem_exemplares, self.usuario, datetime(2024, 6, 18)))

    def test_emprestar_livro_com_penalidade(self):
        self.usuario.data_ultima_penalidade = datetime(2024, 6, 10)
        self.assertFalse(self.biblioteca.emprestar_livro(self.livro2, self.usuario, datetime(2024, 6, 18)))

    def test_devolver_livro(self):
        livro_emprestado = self.livro1
        self.biblioteca.emprestar_livro(livro_emprestado, self.usuario, datetime(2024, 6, 18))
        self.biblioteca.devolver_livro(livro_emprestado, datetime(2024, 6, 25))
        self.assertFalse(livro_emprestado.esta_emprestado())
        self.assertIsNone(self.usuario.data_ultima_penalidade)

    def test_devolver_livro_com_atraso(self):
        livro_emprestado = self.livro1
        self.biblioteca.emprestar_livro(livro_emprestado, self.usuario, datetime(2024, 6, 18))
        self.biblioteca.devolver_livro(livro_emprestado, datetime(2024, 7, 2))
        self.assertTrue(self.usuario.possui_penalidade(datetime(2024, 7, 2)))

if __name__ == '__main__':
    unittest.main()
