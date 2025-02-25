def create_permutation_key(phrase):
    # Створення ключа перестановки на основі алфавітного порядку символів фрази
    sorted_chars = sorted(list(phrase))
    return [sorted_chars.index(char) for char in phrase]


def encrypt(text, phrase):
    # Підготовка тексту: видалення пробілів та перетворення в верхній регістр
    text = text.replace(" ", "").replace("\n", "").upper()
    key = create_permutation_key(phrase)
    cols = len(phrase)
    # Додати 'X', щоб текст був кратний довжині фрази
    while len(text) % cols != 0:
        text += 'X'
    
    rows = len(text) // cols
    # Формування таблиці
    table = [list(text[i*cols:(i+1)*cols]) for i in range(rows)]

    # Шифрування: збір символів за перестановкою колонок
    encrypted_text = ""
    for col in sorted(range(cols), key=lambda x: key[x]):
        for row in range(rows):
            encrypted_text += table[row][col]
    return encrypted_text


def decrypt(encrypted_text, phrase):
    key = create_permutation_key(phrase)
    cols = len(phrase)
    rows = len(encrypted_text) // cols

    # Ініціалізуємо таблицю порожніми рядками
    table = [[''] * cols for _ in range(rows)]

    # Дешифрування: заповнюємо таблицю по колонках у порядку перестановки
    index = 0
    for col in sorted(range(cols), key=lambda x: key[x]):
        for row in range(rows):
            table[row][col] = encrypted_text[index]
            index += 1

    # Зчитування таблиці по рядках
    decrypted_text = "".join(["".join(row) for row in table])
    return decrypted_text.rstrip('X')  # Видалення зайвих 'X' у кінці


# Текст для тестування
text = """The artist is the creator of beautiful things. To reveal art and conceal the artist is art's aim. The critic is he who can translate into another manner or a new material his impression of beautiful things. The highest, as the lowest, form of criticism is a mode of autobiography. Those who find ugly meanings in beautiful things are corrupt without being charming. This is a fault. Those who find beautiful meanings in beautiful things are the cultivated. For these there is hope. They are the elect to whom beautiful things mean only Beauty. There is no such thing as a moral or an immoral book. Books are well written, or badly written. That is all. The nineteenth-century dislike of realism is the rage of Caliban seeing his own face in a glass. The nineteenth-century dislike of Romanticism is the rage of Caliban not seeing his own face in a glass. The moral life of man forms part of the subject matter of the artist, but the morality of art consists in the perfect use of an imperfect medium. No artist desires to prove anything. Even things that are true can be proved. No artist has ethical sympathies. An ethical sympathy in an artist is an unpardonable mannerism of style. No artist is ever morbid. The artist can express everything. Thought and language are to the artist instruments of an art. Vice and virtue are to the artist materials for an art. From the point of view of form, the type of all the arts is the art of the musician. From the point of view of feeling, the actor's craft is the type. All art is at once surface and symbol. Those who go beneath the surface do so at their peril. Those who read the symbol do so at their peril. It is the spectator, and not life, that art really mirrors. Diversity of opinion about a work of art shows that the work is new, complex, vital. When critics disagree the artist is in accord with himself. We can forgive a man for making a useful thing as long as he does not admire it. The only excuse for making a useless thing is that one admires it intensely. All art is quite useless."""

phrase = "SECRET"

# Шифрування
encrypted_text = encrypt(text, phrase)
print("Зашифрований текст:")
print(encrypted_text[:500] + "...\n")  # Виводимо лише перші 500 символів для зручності

# Дешифрування
decrypted_text = decrypt(encrypted_text, phrase)
print("Дешифрований текст:")
print(decrypted_text[:500] + "...\n")  # Виводимо лише перші 500 символів для перевірки

# Перевірка збігу
if decrypted_text == text.replace(" ", "").replace("\n", "").upper():
    print("Дешифрований текст повністю співпадає з оригіналом!")
else:
    print("Дешифрований текст не співпадає з оригіналом.")
