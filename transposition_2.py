import numpy as np

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

def encrypt(text, key1, key2):
    """
    Виконує подвійне шифрування перестановкою
    """
    grid, key_order1 = text_to_grid(text, key1)
    transposed1 = ''.join(''.join(grid[r][c] for r in range(len(grid))) for c in key_order1)
    
    grid2, key_order2 = text_to_grid(transposed1, key2)
    transposed2 = ''.join(''.join(grid2[r][c] for r in range(len(grid2))) for c in key_order2)
    
    return transposed2

def decrypt(text, key1, key2):
    """
    Виконує дешифрування подвійної перестановки
    """
    cols2 = len(key2)
    rows2 = -(-len(text) // cols2)
    key_order2 = sorted(range(len(key2)), key=lambda x: key2[x])
    
    grid2 = [[' ' for _ in range(cols2)] for _ in range(rows2)]
    idx = 0
    for c in key_order2:
        for r in range(rows2):
            if idx < len(text):
                grid2[r][c] = text[idx]
                idx += 1
    text_stage1 = ''.join(''.join(row) for row in grid2)
    
    cols1 = len(key1)
    rows1 = -(-len(text_stage1) // cols1)
    key_order1 = sorted(range(len(key1)), key=lambda x: key1[x])
    
    grid1 = [[' ' for _ in range(cols1)] for _ in range(rows1)]
    idx = 0
    for c in key_order1:
        for r in range(rows1):
            if idx < len(text_stage1):
                grid1[r][c] = text_stage1[idx]
                idx += 1
    
    return ''.join(''.join(row) for row in grid1).strip()

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

encrypted = encrypt(text, "SECRET", "CRYPTO")
decrypted = decrypt(encrypted, "SECRET", "CRYPTO")

print("Encrypted:", encrypted)
print("Decrypted:", decrypted)
