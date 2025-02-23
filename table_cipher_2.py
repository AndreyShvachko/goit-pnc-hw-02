import math
import string


def vigenere_cipher(text: str, key: str, encrypt: bool = True) -> str:
    alphabet = string.ascii_uppercase
    key = key.upper()
    text = text.upper()

    key_indices = [alphabet.index(k) for k in key if k in alphabet]
    result = []
    key_pos = 0

    for char in text:
        if char in alphabet:
            shift = key_indices[key_pos % len(key_indices)] * (1 if encrypt else -1)
            new_char = alphabet[(alphabet.index(char) + shift) % len(alphabet)]
            result.append(new_char)
            key_pos += 1
        else:
            result.append(char)  # Збереження розділових знаків та пробілів

    return "".join(result)


def create_column_order(key: str) -> list[int]:
    return [i for _, i in sorted(zip(key, range(len(key))))]

def inverse_order(order: list[int]) -> list[int]:
    inverse = [0] * len(order)
    for i, pos in enumerate(order):
        inverse[pos] = i
    return inverse

def table_cipher(text: str, key: str, encrypt: bool = True) -> str:
    order = create_column_order(key) if encrypt else inverse_order(create_column_order(key))
    num_cols = len(order)
    num_rows = math.ceil(len(text) / num_cols)

    padded_text = text.ljust(num_rows * num_cols)

    if encrypt:
        # Формуємо матрицю рядків
        matrix = [padded_text[i * num_cols:(i + 1) * num_cols] for i in range(num_rows)]
        # Зчитування за стовпцями у порядку order
        result = "".join(matrix[row][col] for col in order for row in range(num_rows))
    else:
        # Розбиття тексту на колонки
        col_length = num_rows
        columns = [list(padded_text[i * col_length:(i + 1) * col_length]) for i in range(num_cols)]

        # Перевпорядкування колонок за order
        reordered = [None] * num_cols
        for idx, col_idx in enumerate(order):
            reordered[col_idx] = columns[idx]

        # Об’єднання у рядки
        result = "".join(reordered[col][row] for row in range(num_rows) for col in range(num_cols))

    return result.strip()


def combined_encrypt(text: str, vigenere_key: str, table_key: str) -> str:
    encrypted_vigenere = vigenere_cipher(text, vigenere_key, True)
    return table_cipher(encrypted_vigenere, table_key, True)

def combined_decrypt(cipher_text: str, vigenere_key: str, table_key: str) -> str:
    decrypted_table = table_cipher(cipher_text, table_key, False)
    return vigenere_cipher(decrypted_table, vigenere_key, False)


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
        "All art is quite useless."
    )

    vigenere_key = "KEYWORD"
    table_key = "CRYPTO"

    print("Оригінальний текст:\n", text, "\n")
    encrypted = combined_encrypt(text, vigenere_key, table_key)
    print("🔒 Зашифрований текст:\n", encrypted, "\n")

    decrypted = combined_decrypt(encrypted, vigenere_key, table_key)
    print("🔓 Дешифрований текст:\n", decrypted, "\n")

    assert decrypted.strip() == text.upper().strip(), "❌ Помилка: дешифрування не збігається з оригіналом!"
    print("✅ Перевірка пройдена: текст відновлено.")