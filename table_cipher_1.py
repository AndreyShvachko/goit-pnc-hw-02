import math


def create_table_key_order(key: str) -> list:
    """
    Створює порядок стовпців на основі ключа.

    Повертає список індексів для перестановки стовпців.
    """
    key = key.upper()
    sorted_key = sorted(list(key))

    order = []
    taken = [False] * len(key)

    for char in sorted_key:
        for i, k_char in enumerate(key):
            if k_char == char and not taken[i]:
                order.append(i)
                taken[i] = True
                break

    return order

def table_cipher(text: str, key: str, encrypt: bool = True) -> str:
    """
    Табличний шифр:

    - Якщо encrypt=True: шифрування.
    - Якщо encrypt=False: дешифрування.
    """
    order = create_table_key_order(key)
    num_cols = len(order)
    num_rows = math.ceil(len(text) / num_cols)

    # Доповнюємо текст пробілами, щоб заповнити матрицю
    padded_text = text.ljust(num_rows * num_cols)

    # Формуємо матрицю
    matrix = [list(padded_text[i * num_cols:(i + 1) * num_cols]) for i in range(num_rows)]

    if encrypt:
        # Шифрування: перестановка стовпців за порядком
        transposed = [''.join(row[i] for row in matrix) for i in order]
    else:
        # Дешифрування: знаходимо інверсний порядок стовпців
        inverse_order = [order.index(i) for i in range(num_cols)]
        transposed = [''.join(row[i] for row in matrix) for i in inverse_order]

    return ''.join(transposed)

# ---------------------- Табличний шифр ----------------------

def table_encrypt(text: str, key: str) -> str:
    """Шифрування табличним шифром."""
    return table_cipher(text, key, encrypt=True)

def table_decrypt(cipher_text: str, key: str) -> str:
    """Дешифрування табличним шифром."""
    return table_cipher(cipher_text, key, encrypt=False)

# ---------------------- Демонстрація ----------------------

if __name__ == "__main__":
    # Текст із завдання (передмова до "Портрета Доріана Ґрея")
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

    print("Оригінальний текст:")
    print(text, "\n")

    # Рівень 1: Табличний шифр із ключем "MATRIX"
    key = "MATRIX"
    encrypted_text = table_encrypt(text, key)
    decrypted_text = table_decrypt(encrypted_text, key)

    print("Табличний шифр (ключ: 'MATRIX'):")
    print("Шифрований текст:")
    print(encrypted_text, "\n")

    print("Дешифрований текст:")
    print(decrypted_text)