def decrypt(encrypted_text, n):
    if encrypted_text is None:
        return None
        
    new_text = encrypted_text
    ch_list = list(encrypted_text)
    for i in range(n):
        ch_list[1::2] = new_text[:len(encrypted_text)//2]
        ch_list[0::2] = new_text[len(encrypted_text)//2:]
        new_text = ''.join(ch_list)
    return new_text

def encrypt(text, n):
    new_text = text
    for i in range(n):
        new_text = new_text[1::2] + new_text[0::2]
    return new_text