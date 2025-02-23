# Шифр перестановки: проста перестановка 

import math


def create_permutation_order(key: str) -> list:
    """
    Створює порядок перестановки на основі відсортованого ключа.

     Повертає список індексів для перестановки.
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

def transpose_text(text: str, order: list, encrypt: bool = True) -> str:
    """
    Здійснює перестановку символів у тексті за заданим порядком.

    - Якщо encrypt=True: шифрування (переупорядкування стовпців).
    - Якщо encrypt=False: дешифрування (зворотна перестановка).
    """
    num_cols = len(order)
    num_rows = math.ceil(len(text) / num_cols)
    padded_text = text.ljust(num_rows * num_cols)  # Заповнюємо прогалини пробілами

    # Формуємо матрицю з тексту
    matrix = [list(padded_text[i * num_cols:(i + 1) * num_cols]) for i in range(num_rows)]

    if encrypt:
        # Перестановка стовпців відповідно до порядку
        transposed = [''.join(row[i] for row in matrix) for i in order]
    else:
        # Зворотна перестановка: знаходимо інверсний порядок
        inverse_order = [order.index(i) for i in range(num_cols)]
        transposed = [''.join(row[i] for row in matrix) for i in inverse_order]

    return ''.join(transposed)



def simple_transposition_encrypt(text: str, key: str) -> str:
    """Шифрування простою перестановкою."""
    order = create_permutation_order(key)
    return transpose_text(text, order, encrypt=True)

def simple_transposition_decrypt(cipher_text: str, key: str) -> str:
    """Дешифрування простої перестановки."""
    order = create_permutation_order(key)
    return transpose_text(cipher_text, order, encrypt=False)



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

    print("Оригінальний текст:")
    print(text, "\n")

    # Рівень 1: Проста перестановка
    key_simple = "SECRET"
    encrypted_simple = simple_transposition_encrypt(text, key_simple)
    decrypted_simple = simple_transposition_decrypt(encrypted_simple, key_simple)

    print("Проста перестановка (ключ: 'SECRET'):")
    print("Шифрований текст:")
    print(encrypted_simple, "\n")
    print("Дешифрований текст:")
    print(decrypted_simple)