# Шифр Віженера: дешифрування без відомого ключа (метод Касіскі та тест Фрідмана)

import re
from collections import Counter
from math import gcd

ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

# ---------------------- Допоміжні функції ----------------------

def kasiski_examination(cipher_text: str, min_seq_len: int = 3) -> int:
    """
    Метод Касіскі: знаходить повторювані послідовності в шифротексті та аналізує відстані між ними.
    
    Повертає найбільш ймовірну довжину ключа.
    """
    # Виділяємо лише літери у верхньому регістрі для аналізу
    filtered_text = re.sub(r'[^A-Z]', '', cipher_text.upper())
    
    # Знаходимо повторювані послідовності та їхні позиції
    seq_positions = {}
    for i in range(len(filtered_text) - min_seq_len + 1):
        seq = filtered_text[i:i + min_seq_len]
        positions = seq_positions.setdefault(seq, [])
        positions.append(i)

    # Обчислюємо відстані між повторами
    distances = []
    for positions in seq_positions.values():
        if len(positions) > 1:
            for i in range(len(positions) - 1):
                distances.append(positions[i + 1] - positions[i])

    if not distances:
        return 1  # Якщо повторів не знайдено

    # Знаходимо НСД (найбільший спільний дільник) відстаней
    key_length = distances[0]
    for distance in distances[1:]:
        key_length = gcd(key_length, distance)

    return key_length

def friedman_test(cipher_text: str) -> float:
    """
    Тест Фрідмана: оцінює довжину ключа на основі індексу відповідності.

     Повертає оціночну довжину ключа.
    """
    filtered_text = re.sub(r'[^A-Z]', '', cipher_text.upper())
    N = len(filtered_text)
    freqs = Counter(filtered_text)

    IC = sum(f * (f - 1) for f in freqs.values()) / (N * (N - 1)) if N > 1 else 0

    if IC == 0:
        return 1

    K = 0.027 * N / ((N - 1) * IC - 0.038 * N + 0.065)
    return round(K)

def recover_key(cipher_text: str, key_length: int) -> str:
    """
    Відновлює ключ, виходячи з довжини ключа та аналізу частотності.

     Повертає відновлений ключ у верхньому регістрі.
    """
    filtered_text = re.sub(r'[^A-Z]', '', cipher_text.upper())
    key = ''

    for i in range(key_length):
        # Витягуємо кожну n-ту літеру, де n = key_length
        segment = filtered_text[i::key_length]
        freqs = Counter(segment)
        
        # Найчастіше зустрічається літера, що припускається як 'E'
        most_common_letter = freqs.most_common(1)[0][0]
        shift = (ALPHABET.index(most_common_letter) - ALPHABET.index('E')) % 26
        key += ALPHABET[shift]

    return key

def vigenere_decrypt(cipher_text: str, key: str) -> str:
    """
    Дешифрує текст за допомогою знайденого або відомого ключа.

    Повертає розшифрований текст.
    """
    decrypted_text = []
    key = key.upper()
    key_index = 0

    for char in cipher_text:
        if char.isalpha():
            offset = 65 if char.isupper() else 97
            shifted = (ord(char) - offset - (ord(key[key_index % len(key)]) - 65)) % 26
            decrypted_text.append(chr(shifted + offset))
            key_index += 1
        else:
            decrypted_text.append(char)

    return ''.join(decrypted_text)


if __name__ == "__main__":
    # Зашифрований текст (отриманий на 1-му кроці)
    encrypted_text = (
        "Vsl rnkiikb vc vho flbyxhv kn ohfqvjmqk sytpav. Zs skxyjl mda mfk ylxnflj "
        "cye rqnxzkc yx wvbfxsl. Ylt xayqtv vl ys ezu wcy lyj zmx grtlrqrhgf nq rkzx."
    )

    print("Зашифрований текст:\n")
    print(encrypted_text)

    # Визначення довжини ключа методом Касіскі
    kasiski_length = kasiski_examination(encrypted_text)
    print(f"\n Ймовірна довжина ключа (Касіскі): {kasiski_length}")

    # Оцінка довжини ключа тестом Фрідмана
    friedman_length = friedman_test(encrypted_text)
    print(f" Оціночна довжина ключа (Фрідман): {friedman_length}")

    # Відновлення ключа
    estimated_key = recover_key(encrypted_text, kasiski_length)
    print(f"\n Відновлений ключ: {estimated_key}")

    #  Дешифрування тексту
    decrypted_text = vigenere_decrypt(encrypted_text, estimated_key)
    print("\n Розшифрований текст:\n")
    print(decrypted_text)