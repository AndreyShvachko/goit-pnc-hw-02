def generate_key(text: str, key: str) -> str:
    """
    Генерує ключ такої ж довжини, як і текст, повторюючи ключове слово.
    Пропускає нелітерні символи в тексті, щоб ключ вирівнювався лише з літерами.
    """
    key = key.upper()
    filtered_text_length = len([char for char in text if char.isalpha()])
    expanded_key = (key * (filtered_text_length // len(key))) + key[:filtered_text_length % len(key)]
    return expanded_key

def vigenere_encrypt(text: str, key: str) -> str:
    """
    Шифрує текст за шифром Віженера.

    - text: текст для шифрування
    - key: ключове слово

    Повертає зашифрований текст.
    """
    encrypted_text = []
    key = generate_key(text, key)
    key_index = 0

    for char in text:
        if char.isalpha():
            offset = 65 if char.isupper() else 97
            shifted = (ord(char) - offset + (ord(key[key_index]) - 65)) % 26
            encrypted_text.append(chr(shifted + offset))
            key_index += 1
        else:
            encrypted_text.append(char)

    return ''.join(encrypted_text)

def vigenere_decrypt(cipher_text: str, key: str) -> str:
    """
    Дешифрує текст, зашифрований шифром Віженера.

    - cipher_text: зашифрований текст
    - key: ключове слово

    Повертає розшифрований текст.
    """
    decrypted_text = []
    key = generate_key(cipher_text, key)
    key_index = 0

    for char in cipher_text:
        if char.isalpha():
            offset = 65 if char.isupper() else 97
            shifted = (ord(char) - offset - (ord(key[key_index]) - 65)) % 26
            decrypted_text.append(chr(shifted + offset))
            key_index += 1
        else:
            decrypted_text.append(char)

    return ''.join(decrypted_text)


if __name__ == "__main__":
    text = (
        "The artist is the creator of beautiful things. To reveal art and conceal the artist is art's aim. "
        "The critic is he who can translate into another manner or a new material his impression of beautiful things. "
        "The highest, as the lowest, form of criticism is a mode of autobiography. "
        "Those who find ugly meanings in beautiful things are corrupt without being charming."
    )
    key = "CRYPTOGRAPHY"

    print("Оригінальний текст:\n")
    print(text)

    encrypted = vigenere_encrypt(text, key)
    print("\n Зашифрований текст:\n")
    print(encrypted)

    decrypted = vigenere_decrypt(encrypted, key)
    print("\n Розшифрований текст:\n")
    print(decrypted)