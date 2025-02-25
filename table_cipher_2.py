import string

# -------------------------------
# Шифр Віженера
# -------------------------------
def vigenere_encrypt(text, key):
    text = ''.join(filter(str.isalpha, text.upper()))
    key = ''.join(filter(str.isalpha, key.upper()))
    encrypted = []
    for i, char in enumerate(text):
        shift = ord(key[i % len(key)]) - ord('A')
        encrypted_char = chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
        encrypted.append(encrypted_char)
    return ''.join(encrypted)

def vigenere_decrypt(ciphertext, key):
    ciphertext = ''.join(filter(str.isalpha, ciphertext.upper()))
    key = ''.join(filter(str.isalpha, key.upper()))
    decrypted = []
    for i, char in enumerate(ciphertext):
        shift = ord(key[i % len(key)]) - ord('A')
        decrypted_char = chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
        decrypted.append(decrypted_char)
    return ''.join(decrypted)

# -------------------------------
# Табличний шифр з фразою-ключем "CRYPTO"
# -------------------------------
class TableCipher:
    def __init__(self, key):
        self.key = ''.join(filter(str.isalpha, key.upper()))

    def encrypt(self, plaintext):
        plaintext = ''.join(filter(str.isalpha, plaintext.upper()))
        columns = len(self.key)
        rows = -(-len(plaintext) // columns)

        # Заповнення таблиці рядками
        table = [['X' for _ in range(columns)] for _ in range(rows)]
        idx = 0
        for r in range(rows):
            for c in range(columns):
                if idx < len(plaintext):
                    table[r][c] = plaintext[idx]
                    idx += 1

        # Визначення порядку стовпців за відсортованим ключем
        sorted_key_indices = sorted(range(columns), key=lambda i: self.key[i])

        # Формування зашифрованого тексту стовпцями
        ciphertext = ''.join(table[r][c] for c in sorted_key_indices for r in range(rows))
        return ciphertext

    def decrypt(self, ciphertext):
        ciphertext = ''.join(filter(str.isalpha, ciphertext.upper()))
        columns = len(self.key)
        rows = -(-len(ciphertext) // columns)

        sorted_key_indices = sorted(range(columns), key=lambda i: self.key[i])
        base_col_len = len(ciphertext) // columns
        extra = len(ciphertext) % columns
        col_lengths = [base_col_len + (1 if i < extra else 0) for i in range(columns)]

        # Заповнення таблиці стовпцями
        table = [['' for _ in range(columns)] for _ in range(rows)]
        idx = 0
        for order, col_index in enumerate(sorted_key_indices):
            length = col_lengths[order]
            for r in range(length):
                table[r][col_index] = ciphertext[idx]
                idx += 1

        # Зчитування таблиці рядками для розшифрування
        plaintext = ''.join(table[r][c] for r in range(rows) for c in range(columns))
        return plaintext.rstrip('X')

# -------------------------------
# Демонстрація: спочатку шифр Віженера, потім табличний шифр з ключем "CRYPTO"
# -------------------------------
plaintext = (
    "The artist is the creator of beautiful things. To reveal art and conceal the artist is art's aim. "
    "The critic is he who can translate into another manner or a new material his impression of beautiful things. "
    "The highest, as the lowest, form of criticism is a mode of autobiography. "
    "Those who find ugly meanings in beautiful things are corrupt without being charming. This is a fault. "
    "Those who find beautiful meanings in beautiful things are the cultivated. For these there is hope. "
    "They are the elect to whom beautiful things mean only Beauty. There is no such thing as a moral or an immoral book. "
    "Books are well written, or badly written. That is all. The nineteenth-century dislike of realism is the rage of Caliban "
    "seeing his own face in a glass. The nineteenth-century dislike of Romanticism is the rage of Caliban not seeing his own face in a glass. "
    "The moral life of man forms part of the subject matter of the artist, but the morality of art consists in the perfect use of an imperfect medium. "
    "No artist desires to prove anything. Even things that are true can be proved. No artist has ethical sympathies. "
    "An ethical sympathy in an artist is an unpardonable mannerism of style. No artist is ever morbid. The artist can express everything. "
    "Thought and language are to the artist instruments of an art. Vice and virtue are to the artist materials for an art. "
    "From the point of view of form, the type of all the arts is the art of the musician. From the point of view of feeling, the actor's craft is the type. "
    "All art is at once surface and symbol. Those who go beneath the surface do so at their peril. Those who read the symbol do so at their peril. "
    "It is the spectator, and not life, that art really mirrors. Diversity of opinion about a work of art shows that the work is new, complex, vital. "
    "When critics disagree the artist is in accord with himself. We can forgive a man for making a useful thing as long as he does not admire it. "
    "The only excuse for making a useless thing is that one admires it intensely. All art is quite useless."
)

# Ключі
vigenere_key = "CRYPTO"
table_key = "CRYPTO"

# Крок 1: Шифрування за допомогою шифру Віженера
vigenere_encrypted = vigenere_encrypt(plaintext, vigenere_key)

# Крок 2: Шифрування за допомогою табличного шифра
table_cipher = TableCipher(table_key)
table_encrypted = table_cipher.encrypt(vigenere_encrypted)

# Розшифрування (у зворотньому порядку)
# Крок 1: Дешифрування табличного шифра
table_decrypted = table_cipher.decrypt(table_encrypted)

# Крок 2: Дешифрування шифра Віженера
vigenere_decrypted = vigenere_decrypt(table_decrypted, vigenere_key)

# Форматування для порівняння
formatted_original = ''.join(filter(str.isalpha, plaintext.upper()))
formatted_decrypted = ''.join(filter(str.isalpha, vigenere_decrypted.upper()))

# Результати
print("--- РЕЗУЛЬТАТИ ---")
print(f"Зашифрований (Віженер → Табличний) перші 300 символів:\n{table_encrypted[:300]}...")
print(f"Дешифрований текст (перші 300 символів):\n{vigenere_decrypted[:300]}...")
print(f"\nСпівпадіння з оригіналом: {'Так' if formatted_original == formatted_decrypted else 'Ні'}")
