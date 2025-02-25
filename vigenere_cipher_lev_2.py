import numpy as np

def vigenere_encrypt(text, key):
    """
    Шифрування Віженера
    """
    encrypted_text = []
    key = key.upper()
    key_index = 0
    for char in text:
        if char.isalpha():
            shift = ord(key[key_index % len(key)]) - ord('A')
            if char.isupper():
                encrypted_text.append(chr((ord(char) - ord('A') + shift) % 26 + ord('A')))
            else:
                encrypted_text.append(chr((ord(char) - ord('a') + shift) % 26 + ord('a')))
            key_index += 1
        else:
            encrypted_text.append(char)
    return ''.join(encrypted_text)

def vigenere_decrypt(text, key):
    """
    Розшифрування Віженера
    """
    decrypted_text = []
    key = key.upper()
    key_index = 0
    for char in text:
        if char.isalpha():
            shift = ord(key[key_index % len(key)]) - ord('A')
            if char.isupper():
                decrypted_text.append(chr((ord(char) - ord('A') - shift) % 26 + ord('A')))
            else:
                decrypted_text.append(chr((ord(char) - ord('a') - shift) % 26 + ord('a')))
            key_index += 1
        else:
            decrypted_text.append(char)
    return ''.join(decrypted_text)

def text_to_grid(text, key):
    """
    Перетворює текст у матрицю відповідно до ключа
    """
    key_order = sorted(range(len(key)), key=lambda x: key[x])  # Порядок сортування стовпців
    cols = len(key)
    rows = -(-len(text) // cols)  # округлення вгору для визначення кількості рядків
    grid = [[' ' for _ in range(cols)] for _ in range(rows)]
    
    idx = 0
    for r in range(rows):
        for c in range(cols):
            if idx < len(text):
                grid[r][c] = text[idx]
                idx += 1
    
    return grid, key_order  # Повертає сітку та порядок стовпців

def table_encrypt(text, key):
    """
    Табличне шифрування
    """
    grid, key_order = text_to_grid(text, key)
    return ''.join(''.join(grid[r][c] for r in range(len(grid))) for c in key_order)

def table_decrypt(text, key):
    """
    Табличне розшифрування
    """
    cols = len(key)
    rows = -(-len(text) // cols)
    grid = [[' ' for _ in range(cols)] for _ in range(rows)]
    
    key_order = sorted(range(len(key)), key=lambda x: key[x])
    idx = 0
    for c in key_order:
        for r in range(rows):
            if idx < len(text):
                grid[r][c] = text[idx]
                idx += 1
    
    decrypted_text = ''.join(''.join(row) for row in grid)
    return decrypted_text.strip()

def encrypt(text, key_table):
    """
    Спочатку шифрування Віженера, потім табличне шифрування
    """
    vigenere_encrypted = vigenere_encrypt(text, "CRYPTO")
    return table_encrypt(vigenere_encrypted, key_table)

def decrypt(text, key_table):
    """
    Спочатку табличне розшифрування, потім Віженера
    """
    table_decrypted = table_decrypt(text, key_table)
    return vigenere_decrypt(table_decrypted, "CRYPTO")

# Приклад використання
text = ("The artist is the creator of beautiful things. To reveal art and conceal the artist is art's aim. "
        "The critic is he who can translate into another manner or a new material his impression of beautiful things. "
        "The highest, as the lowest, form of criticism is a mode of autobiography. Those who find ugly meanings "
        "in beautiful things are corrupt without being charming. This is a fault. Those who find beautiful meanings "
        "in beautiful things are the cultivated. For these there is hope. They are the elect to whom beautiful things "
        "mean only Beauty. There is no such thing as a moral or an immoral book. Books are well written, or badly written. "
        "That is all. The nineteenth-century dislike of realism is the rage of Caliban seeing his own face in a glass. "
        "The nineteenth-century dislike of Romanticism is the rage of Caliban not seeing his own face in a glass. "
        "The moral life of man forms part of the subject matter of the artist, but the morality of art consists in the "
        "perfect use of an imperfect medium. No artist desires to prove anything. Even things that are true can be proved. "
        "No artist has ethical sympathies. An ethical sympathy in an artist is an unpardonable mannerism of style. "
        "No artist is ever morbid. The artist can express everything. Thought and language are to the artist instruments "
        "of an art. Vice and virtue are to the artist materials for an art. From the point of view of form, the type "
        "of all the arts is the art of the musician. From the point of view of feeling, the actor's craft is the type. "
        "All art is at once surface and symbol. Those who go beneath the surface do so at their peril. Those who read "
        "the symbol do so at their peril. It is the spectator, and not life, that art really mirrors. Diversity of opinion "
        "about a work of art shows that the work is new, complex, vital. When critics disagree the artist is in accord "
        "with himself. We can forgive a man for making a useful thing as long as he does not admire it. The only excuse "
        "for making a useless thing is that one admires it intensely. All art is quite useless.")

encrypted = encrypt(text, "CRYPTO")
decrypted = decrypt(encrypted, "CRYPTO")

print("Encrypted:", encrypted)
print("Decrypted:", decrypted)
