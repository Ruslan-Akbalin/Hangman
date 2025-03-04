from random import choice

class GameWelcome:
    """Приветствие игрока"""
    __WELCOME = (
                 '''Добро пожаловать в игру "Виселица"!''', 
                 '''Правила просты:''', 
                 '''- Я загадаю слово и покажу количество букв в нем.''', 
                 '''- Ты будешь называть буквы, чтобы угадать слово.''', 
                 '''- Если буква есть в слове, я открою её позицию.''', 
                 '''- Если буквы нет, ты потеряешь одну попытку.''', 
                 '''- У тебя есть ограниченное количество попыток, чтобы угадать слово до того, как "человечек" будет повешен.\n''', 
                 '''Готов проверить свою удачу и словарный запас?'''
                )
    
    @classmethod
    def welcome(cls) -> None:
        """Метод для вывода приветствия игрока"""
        print(*cls.__WELCOME, sep="\n")

    @classmethod
    def start_over(cls) -> None:
        """Предложение сыгарь еще после победы/поражения"""
        print('''Не отчаивайся! Хочешь попробовать еще раз?''')

    @classmethod
    def end_game(cls) -> None:
        """Прощание с игроком"""
        print('''Если передумаешь - возвращайся!''') 


class GameStart:
    """Класс для создания игр"""
    __HANGMAN = (
        """
        ______
        |
        |
        |
        |
        |
        |
        |///////
        """,
        """
        ______
        |    |
        |
        |
        |
        |
        |
        |///////
        """,
        """
        ______
        |    |
        |    O
        |
        |
        |
        |
        |///////
        """,
        """
        ______
        |    |
        |    O
        |    |
        | 
        |   
        |   
        |/////// 
        """,
        """
        ______
        |    |
        |    O
        |   /|
        |   
        |   
        |
        |///////   
        """,
        """
        ______
        |    |
        |    O
        |   /|\\
        |   
        |   
        |
        |///////     
        """,
        """
        ______
        |    |
        |    O
        |   /|\\
        |   /
        |   
        |
        |///////    
        """,
        """
        ______
        |    |
        |    O
        |   /|\\
        |   / \\
        |   
        |
        |///////   
        """
    )
    __MAX_MISTAKES = len(__HANGMAN) - 1
 
    def __init__(self):
        with open(r"УКАЖИ ССЫЛКУ НА ФАЙЛ WORDS", encoding="utf-8") as file:
            self.__hidden_word = choice(file.readlines())[:-1]    # загаданное слово
        self.__guessed_letters = ()    # отгаданные буквы
        self.__incorrect_letters = ()    # неправильные буквы - их нет в загаданном слове
        self.__word = " ".join("_" * len(self.__hidden_word))    # слово для вывода на экран
        self.__mistakes = 0    # количество ошибок


    # объект-свойство mistakes
    @property
    def mistakes(self) -> int:
        return self.__mistakes
    
    @mistakes.setter
    def mistakes(self, mistake: int) -> None:
        self.__mistakes += mistake

    # объект-свойство word
    @property
    def word(self) -> str:
        return self.__word
        
    @word.setter
    def word(self, attempt: str) -> None:
        match attempt:
            case str(attempt) if attempt == self.__hidden_word:
                self.__word = attempt
            case str(attempt) if attempt in self.__hidden_word and attempt not in self.__guessed_letters:
                self.__guessed_letters += (attempt,)
                self.__word = " ".join(letter 
                                       if letter in self.__guessed_letters 
                                       else "_" 
                                       for letter in self.__hidden_word
                                      )
            case str(attempt) if attempt.isalpha() and attempt not in self.__incorrect_letters:
                self.__incorrect_letters += (attempt,)
                self.mistakes = 1             

    @classmethod
    def show_hangman(cls, mistake: int) -> None:
        """Выводит текущее изображение виселицы"""
        print(cls.__HANGMAN[mistake])
    
    @classmethod
    def check_mistakes(cls, mistake: int) -> bool:
        """Проверяет не превыщено лимит допущеных ошибок"""
        return mistake < cls.__MAX_MISTAKES


flag = True
GameWelcome.welcome()
start_game = input('''("да" - начать игру, "нет" - отказаться): ''')

while flag:
    # Проверка на корректность вводимых данных
    while start_game.lower() not in ("да", "нет"):
        start_game = input('''Введены некорректные значения!\n("да"/"нет"): ''')
    # Игрок решил сыграть в игру
    if start_game == "да":
        # Создаем новую игру
        game = GameStart()
        print(f'''Поехали!\nВот твоё слово: {game.word}''')
        victory = False
        # Цикл завершится, если игрок победит или количество
        # допущенных ошибок станет равно максимально возможным
        while game.check_mistakes(game.mistakes) or victory == False:
            # Условие победы - в слове не останется неизвестных букв
            if "_" not in game.word:                
                print(f'''Победа! Ты угадал слово!\nЗагаданное слово: "{game.word}"''')
                start_game = input('''Cыграем еще раз?\n("да"/"нет"): ''')
                victory = True
                break
            game.word = input("Введи букву или всё слово целиком: ")
            print(f'''Загаданное слово: "{game.word}"''')
            print(f"Количество допущенных ошибок: {game.mistakes}")
            game.show_hangman(game.mistakes)
        # Условие поражения - количество ощибок стало равно максимально возможным
        if victory == False:
            print(f"Поражение! Допущено максимальное количество ошибок!")
            GameWelcome.start_over()
            start_game = input('''("да"/"нет"): ''')
        # Игрок решил не продолжать игру
        if start_game != "да":
            flag = False  
    # Игрок передумал играть
    else:
        GameWelcome.end_game()
        flag = False
