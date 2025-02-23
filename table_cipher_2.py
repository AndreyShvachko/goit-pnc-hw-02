import math


def create_table_key_order(key: str) -> list[int]:
    """
    Створює порядок стовпців на основі ключа.

    Кроки:
    - Перетворює ключ у верхній регістр.
    - Сортує символи ключа для визначення порядку стовпців.

    Повертає:
        Список індексів, що вказують на порядок перестановки.
    """
    return sorted(range(len(key)), key=lambda i: key[i].upper())

def inverse_order(order: list[int]) -> list[int]:
    """
    Обчислює інверсний порядок для дешифрування.

    Повертає:
        Список індексів для відновлення початкового порядку стовпців.
    """
    result = [0] * len(order)
    for i, pos in enumerate(order):
        result[pos] = i
    return result


def table_cipher(text: str, key: str, encrypt: bool = True) -> str:
    """
    Табличний шифр із заданим ключем.

    Аргументи:
        text: Текст для обробки.
        key: Ключ шифрування.
        encrypt: True – шифрування, False – дешифрування.

    Повертає:
        Оброблений (зашифрований/дешифрований) текст.
    """
    order = create_table_key_order(key)
    if not encrypt:
        order = inverse_order(order)

    num_cols = len(order)
    num_rows = math.ceil(len(text) / num_cols)
    padded_text = text.ljust(num_rows * num_cols)  # Заповнення пробілами

    matrix = [list(padded_text[i * num_cols:(i + 1) * num_cols]) for i in range(num_rows)]
    
    # Перестановка стовпців
    transposed = ["".join(row[order[col]] for row in matrix) for col in range(num_cols)]

    return "".join(transposed)

def table_encrypt(text: str, key: str) -> str:
    """Шифрування табличним шифром."""
    return table_cipher(text, key, encrypt=True)

def table_decrypt(cipher_text: str, key: str) -> str:
    """Дешифрування табличним шифром."""
    return table_cipher(cipher_text, key, encrypt=False)


def double_table_encrypt(text: str, key1: str, key2: str) -> str:
    """Подвійне шифрування: спершу key1, потім key2."""
    return table_encrypt(table_encrypt(text, key1), key2)

def double_table_decrypt(cipher_text: str, key1: str, key2: str) -> str:
    """Подвійне дешифрування: спершу key2, потім key1."""
    return table_decrypt(table_decrypt(cipher_text, key2), key1)


if __name__ == "__main__":
    text = (
        "The artist is the creator of beautiful things. To reveal art and conceal the artist is art's aim. "
        "The critic is he who can translate into another manner or a new material his impression of beautiful things. "
        "The highest, as the lowest, form of criticism is a mode of autobiography. "
        "Those who find ugly meanings in beautiful things are corrupt without being charming. This is a fault. "
        "Those who find beautiful meanings in beautiful things are the cultivated. For these there is hope. "
        "They are the elect to whom beautiful things mean only Beauty. "
        "There is no such thing as a moral or an immoral book. Books are well written, or badly written. That is all. "
        "The nineteenth-century dislike of realism is the rage of Caliban seeing his own face in a glass. "
        "The nineteenth-century dislike of Romanticism is the rage of Caliban not seeing his own face in a glass. "
        "The moral life of man forms part of the subject matter of the artist, but the morality of art consists in the perfect use of an imperfect medium. "
        "No artist desires to prove anything. Even things that are true can be proved. "
        "No artist has ethical sympathies. An ethical sympathy in an artist is an unpardonable mannerism of style. "
        "No artist is ever morbid. The artist can express everything. "
        "Thought and language are to the artist instruments of an art. "
        "Vice and virtue are to the artist materials for an art. "
        "From the point of view of form, the type of all the arts is the art of the musician. "
        "From the point of view of feeling, the actor's craft is the type. "
        "All art is at once surface and symbol. Those who go beneath the surface do so at their peril. "
        "Those who read the symbol do so at their peril. "
        "It is the spectator, and not life, that art really mirrors. "
        "Diversity of opinion about a work of art shows that the work is new, complex, vital. "
        "When critics disagree the artist is in accord with himself. "
        "We can forgive a man for making a useful thing as long as he does not admire it. "
        "The only excuse for making a useless thing is that one admires it intensely. "
        "All art is quite useless."
    )

    key1 = "MATRIX"
    key2 = "CRYPTO"

    print("Оригінальний текст:\n", text, "\n")

    # Шифрування
    encrypted = double_table_encrypt(text, key1, key2)
    print("Зашифрований текст:\n", encrypted, "\n")

    # Дешифрування
    decrypted = double_table_decrypt(encrypted, key1, key2)
    print("Дешифрований текст:\n", decrypted, "\n")

    # Перевірка
    assert decrypted.strip() == text.strip(), "Помилка: дешифрування не збігається з оригіналом!"
    print("Перевірка пройдена: дешифрування відновлює текст.")