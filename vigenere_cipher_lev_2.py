import string
from collections import Counter
from math import gcd


class VigenereCipher:
    def __init__(self):
        self.alphabet = string.ascii_uppercase
        self.alphabet_len = len(self.alphabet)

    def _format_text(self, text):
        return ''.join(filter(str.isalpha, text.upper()))

    def decrypt_with_key(self, ciphertext, key):
        ciphertext = self._format_text(ciphertext)
        extended_key = (key * (len(ciphertext) // len(key) + 1))[:len(ciphertext)]
        return ''.join(
            self.alphabet[(self.alphabet.index(c) - self.alphabet.index(k)) % self.alphabet_len]
            for c, k in zip(ciphertext, extended_key)
        )

# Метод Касіскі для визначення довжини ключа
def kasiski_examination(ciphertext, min_len=3, max_len=5):
    ciphertext = ''.join(filter(str.isalpha, ciphertext.upper()))
    spacings = []
    for seq_len in range(min_len, max_len + 1):
        positions = {}
        for i in range(len(ciphertext) - seq_len + 1):
            seq = ciphertext[i:i + seq_len]
            if seq in positions:
                spacings.append(i - positions[seq])
            positions[seq] = i

    if not spacings:
        return None

    gcd_values = [gcd(a, b) for i, a in enumerate(spacings) for b in spacings[i + 1:]]
    gcd_values = [val for val in gcd_values if val > 1]

    return Counter(gcd_values).most_common(1)[0][0] if gcd_values else None

# Тест Фрідмана для оцінки довжини ключа
def friedman_test(ciphertext):
    ciphertext = ''.join(filter(str.isalpha, ciphertext.upper()))
    N = len(ciphertext)
    freqs = Counter(ciphertext)
    ic = sum(f * (f - 1) for f in freqs.values()) / (N * (N - 1)) if N > 1 else 0

    expected_ic = 0.065  # Для англійської мови
    random_ic = 1 / 26

    denominator = ic - random_ic
    if denominator == 0:
        return None

    k = (expected_ic - random_ic) / denominator
    return round(k) if k > 0 else None

# Частотний аналіз з покращеним визначенням ключа
def recover_key(ciphertext, key_length):
    alphabet = string.ascii_uppercase
    ciphertext = ''.join(filter(str.isalpha, ciphertext.upper()))
    english_freq = [0.082, 0.015, 0.028, 0.043, 0.13, 0.022, 0.02, 0.061, 0.07, 0.0015, 0.0077, 0.04,
                    0.024, 0.067, 0.075, 0.019, 0.00095, 0.06, 0.063, 0.091, 0.028, 0.0098, 0.024, 0.0015,
                    0.02, 0.00074]
    key = ""

    for i in range(key_length):
        segment = ciphertext[i::key_length]
        segment_len = len(segment)
        min_diff = float('inf')
        best_shift = 0

        for shift in range(26):
            shifted_segment = [(alphabet.index(char) - shift) % 26 for char in segment]
            freqs = [shifted_segment.count(j) / segment_len for j in range(26)]
            diff = sum((f - ef) ** 2 for f, ef in zip(freqs, english_freq))

            if diff < min_diff:
                min_diff = diff
                best_shift = shift

        key += alphabet[best_shift]

    return key

# Вивід результатів для рівня 2
def show_results():
    cipher = VigenereCipher()

    plaintext = (
        "The artist is the creator of beautiful things. To reveal art and conceal the artist is art's aim. "
        "The critic is he who can translate into another manner or a new material his impression of beautiful things. "
        "The highest, as the lowest, form of criticism is a mode of autobiography. Those who find ugly meanings in "
        "beautiful things are corrupt without being charming. This is a fault. Those who find beautiful meanings in "
        "beautiful things are the cultivated. For these there is hope. They are the elect to whom beautiful things "
        "mean only Beauty. There is no such thing as a moral or an immoral book. Books are well written, or badly "
        "written. That is all. The nineteenth-century dislike of realism is the rage of Caliban seeing his own face in "
        "a glass. The nineteenth-century dislike of Romanticism is the rage of Caliban not seeing his own face in a "
        "glass. The moral life of man forms part of the subject matter of the artist, but the morality of art consists "
        "in the perfect use of an imperfect medium. No artist desires to prove anything. Even things that are true can "
        "be proved. No artist has ethical sympathies. An ethical sympathy in an artist is an unpardonable mannerism of "
        "style. No artist is ever morbid. The artist can express everything. Thought and language are to the artist "
        "instruments of an art. Vice and virtue are to the artist materials for an art. From the point of view of form, "
        "the type of all the arts is the art of the musician. From the point of view of feeling, the actor's craft is "
        "the type. All art is at once surface and symbol. Those who go beneath the surface do so at their peril. "
        "Those who read the symbol do so at their peril. It is the spectator, and not life, that art really mirrors. "
        "Diversity of opinion about a work of art shows that the work is new, complex, vital. When critics disagree the "
        "artist is in accord with himself. We can forgive a man for making a useful thing as long as he does not admire "
        "it. The only excuse for making a useless thing is that one admires it intensely. All art is quite useless."
    )

    key = "CRYPTOGRAPHY"
    formatted_plaintext = cipher._format_text(plaintext)

    # Шифрування
    extended_key = (key * (len(formatted_plaintext) // len(key) + 1))[:len(formatted_plaintext)]
    encrypted = ''.join(
        cipher.alphabet[(cipher.alphabet.index(p) + cipher.alphabet.index(k)) % 26]
        for p, k in zip(formatted_plaintext, extended_key)
    )

    print("ЗАВДАННЯ 2: ВИЗНАЧЕННЯ ДОВЖИНИ КЛЮЧА")
    guessed_length_kasiski = kasiski_examination(encrypted)
    guessed_length_friedman = friedman_test(encrypted)

    print(f"Метод Касіскі: довжина ключа ≈ {guessed_length_kasiski if guessed_length_kasiski else 'Не визначена'}")
    print(f"Тест Фрідмана: довжина ключа ≈ {guessed_length_friedman if guessed_length_friedman else 'Не визначена'}")

    key_length = guessed_length_kasiski or guessed_length_friedman
    if not key_length:
        print("Не вдалося визначити довжину ключа.")
        return

    recovered_key = recover_key(encrypted, key_length)
    print(f"Відновлений ключ: {recovered_key}")

    decrypted = cipher.decrypt_with_key(encrypted, recovered_key)
    match = decrypted == formatted_plaintext

    print(f"\nПЕРШІ 200 СИМВОЛІВ РОЗШИФРОВАНОГО ТЕКСТУ: {decrypted[:200]}...")
    print(f"Співпадіння з оригіналом: {'Так' if match else 'Ні'}")

if __name__ == "__main__":
    show_results()
