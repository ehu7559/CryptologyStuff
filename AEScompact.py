ROUNDS = {128 : 10, 192 : 12, 256 : 14}
BLOCK_SIZE_BITS = 128
BLOCK_SIZE_BYTES = BLOCK_SIZE_BITS//8
NUM_ROUNDS = ROUNDS[BLOCK_SIZE_BITS]
SB_TABLE = bytes([99, 124, 119, 123, 242, 107, 111, 197, 48, 1, 103, 43, 254, 215, 171, 118, 202, 130, 201, 125, 250, 89, 71, 240, 173, 212, 162, 175, 156, 164, 114, 192, 183, 253, 147, 38, 54, 63, 247, 204, 52, 165, 229, 241, 113, 216, 49, 21, 4, 199, 35, 195, 24, 150, 5, 154, 7, 18, 128, 226, 235, 39, 178, 117, 9, 131, 44, 26, 27, 110, 90, 160, 82, 59, 214, 179, 41, 227, 47, 132, 83, 209, 0, 237, 32, 252, 177, 91, 106, 203, 190, 57, 74, 76, 88, 207, 208, 239, 170, 251, 67, 77, 51, 133, 69, 249, 2, 127, 80, 60, 159, 168, 81, 163, 64, 143, 146, 157, 56, 245, 188, 182, 218, 33, 16, 255, 243, 210, 205, 12, 19, 236, 95, 151, 68, 23, 196, 167, 126, 61, 100, 93, 25, 115, 96, 129, 79, 220, 34, 42, 144, 136, 70, 238, 184, 20, 222, 94, 11, 219, 224, 50, 58, 10, 73, 6, 36, 92, 194, 211, 172, 98, 145, 149, 228, 121, 231, 200, 55, 109, 141, 213, 78, 169, 108, 86, 244, 234, 101, 122, 174, 8, 186, 120, 37, 46, 28, 166, 180, 198, 232, 221, 116, 31, 75, 189, 139, 138, 112, 62, 181, 102, 72, 3, 246, 14, 97, 53, 87, 185, 134, 193, 29, 158, 225, 248, 152, 17, 105, 217, 142, 148, 155, 30, 135, 233, 206, 85, 40, 223, 140, 161, 137, 13, 191, 230, 66, 104, 65, 153, 45, 15, 176, 84, 187, 22])
INV_SB_TABLE = bytes([82, 9, 106, 213, 48, 54, 165, 56, 191, 64, 163, 158, 129, 243, 215, 251, 124, 227, 57, 130, 155, 47, 255, 135, 52, 142, 67, 68, 196, 222, 233, 203, 84, 123, 148, 50, 166, 194, 35, 61, 238, 76, 149, 11, 66, 250, 195, 78, 8, 46, 161, 102, 40, 217, 36, 178, 118, 91, 162, 73, 109, 139, 209, 37, 114, 248, 246, 100, 134, 104, 152, 22, 212, 164, 92, 204, 93, 101, 182, 146, 108, 112, 72, 80, 253, 237, 185, 218, 94, 21, 70, 87, 167, 141, 157, 132, 144, 216, 171, 0, 140, 188, 211, 10, 247, 228, 88, 5, 184, 179, 69, 6, 208, 44, 30, 143, 202, 63, 15, 2, 193, 175, 189, 3, 1, 19, 138, 107, 58, 145, 17, 65, 79, 103, 220, 234, 151, 242, 207, 206, 240, 180, 230, 115, 150, 172, 116, 34, 231, 173, 53, 133, 226, 249, 55, 232, 28, 117, 223, 110, 71, 241, 26, 113, 29, 41, 197, 137, 111, 183, 98, 14, 170, 24, 190, 27, 252, 86, 62, 75, 198, 210, 121, 32, 154, 219, 192, 254, 120, 205, 90, 244, 31, 221, 168, 51, 136, 7, 199, 49, 177, 18, 16, 89, 39, 128, 236, 95, 96, 81, 127, 169, 25, 181, 74, 13, 45, 229, 122, 159, 147, 201, 156, 239, 160, 224, 59, 77, 174, 42, 245, 176, 200, 235, 187, 60, 131, 83, 153, 97, 23, 43, 4, 126, 186, 119, 214, 38, 225, 105, 20, 99, 85, 33, 12, 125])
SR_TABLE = bytes([0, 5, 10, 15, 4, 9, 14, 3, 8, 13, 2, 7, 12, 1, 6, 11])
INV_SR_TABLE = bytes([0, 13, 10, 7, 4, 1, 14, 11, 8, 5, 2, 15, 12, 9, 6, 3])
ROUND_CONSTANTS = bytes([0x01,0x02,0x04,0x08,0x10,0x20,0x40,0x80,0x1B,0x36])  #PRELOADED CONSTANTS FTW
def sub_bytes(block: bytes) -> bytes:
    return bytes([(SB_TABLE[block[i]]) for i in range(16)])
def inv_sub_bytes(block: bytes) -> bytes:
    return bytes([(INV_SB_TABLE[block[i]]) for i in range(16)])
def shift_rows(block: bytes) -> bytes:
    return bytes([(block[SR_TABLE[i]]) for i in range(16)])
def inv_shift_rows(block: bytes) -> bytes:
    return bytes([(block[INV_SR_TABLE[i]]) for i in range(16)])
def multiply(b, a):
    if b == 1:
        return a
    tmp = (a<<1) & 0xff
    if b == 2:
        return tmp if a < 128 else tmp^0x1b
    if b == 3:
        return tmp^a if a < 128 else (tmp^0x1b)^a
def mix_columns(block: bytes) -> bytes:
    output = bytearray(16)
    mar = [2, 1, 1, 3, 3, 2, 1, 1, 1, 3, 2, 1, 1, 1, 3, 2]
    for i in range(16):
        row = i % 4
        col = i // 4
        folder = bytearray([(multiply(mar[j * 4 + row], block[col * 4 + j])) for j in range(4)])
        output[i] = folder[0] ^ folder[1] ^ folder[2] ^ folder[3]
    return bytes(output)
def inv_mix_columns(block: bytes) -> bytes:
    return mix_columns(mix_columns(mix_columns(block)))
def add_round_key(block: bytes, round_key: bytes) -> bytes:
    return bytes([(block[i] ^ round_key[i]) for i in range(16)])
def inv_add_round_key(block: bytes, round_key: bytes) -> bytes:
    return add_round_key(block, inv_mix_columns(round_key))
def get_pad(length: int) -> bytes:
    pad_length = 16 - (length % 16)
    return bytes([(pad_length) for i in range(pad_length)])
def pad_block(data: bytes) -> bytes:
    data = bytearray(data)
    data.extend(get_pad(len(data)))
    return bytes(data)
def run_key_schedule(keybytes: bytes) -> list[bytes]:
    key_columns = [(keybytes[i * 4: (i + 1) * 4]) for i in range(4)]
    for i in range(4, 4 * (ROUNDS[BLOCK_SIZE_BITS]) + 4):
        new_column = bytearray(key_columns[i-4])
        prev_column = bytearray(key_columns[i-1])
        if i%4 == 0:
            shifted_column = bytearray([prev_column[(i + 1) % 4] for i in range(4)])
            subbed_column = bytearray([(SB_TABLE[shifted_column[i]]) for i in range(4)])
            t_column = bytearray([subbed_column[0] ^ ROUND_CONSTANTS[(i-4)//4], subbed_column[1], subbed_column[2], subbed_column[3]])
            prev_column = bytearray(t_column)
        key_columns.append(bytes([(new_column[j] ^ prev_column[j]) for j in range(4)]))  
    return key_columns
def get_round_keys(initial_key: bytes) -> list[bytes]:
    key_table = run_key_schedule(initial_key)
    round_key_list = []
    for i in range(ROUNDS[BLOCK_SIZE_BITS] + 1):
        arkey = bytearray()
        for j in range(4):
            arkey.extend(key_table[4 * i + j])
        round_key_list.append(bytes(arkey))
    return round_key_list
def encrypt_round(block: bytes, round_key: bytes) -> bytes:
    return add_round_key(mix_columns(shift_rows(sub_bytes(block))),round_key)
def decrypt_round(block: bytes, round_key: bytes) -> bytes:
    return inv_add_round_key(inv_mix_columns(inv_shift_rows(inv_sub_bytes(block))),round_key)
def encrypt_final_round(block: bytes, round_key: bytes) -> bytes:
    return add_round_key(shift_rows(sub_bytes(block)),round_key)
def decrypt_final_round(block: bytes, round_key: bytes) -> bytes:
    return add_round_key(inv_shift_rows(inv_sub_bytes(block)),round_key)
def encrypt_block_128(block: bytes, aes_key: bytes) -> bytes:
    round_keys = get_round_keys(aes_key)
    output = add_round_key(block, round_keys[0])
    for i in range(1,10):
        output = encrypt_round(output, round_keys[i])
    return encrypt_final_round(output, round_keys[10])
def decrypt_block_128(block: bytes, aes_key: bytes) -> bytes:
    round_keys = get_round_keys(aes_key)
    output = add_round_key(block, round_keys[10])
    for i in range(9,0,-1):
        output = decrypt_round(output, round_keys[i])
    return decrypt_final_round(output,round_keys[0])
def trim_padding(block: bytes) -> bytes:
    if len(block) == 0:
        raise Exception("Trying to trim an empty AES ciphertext!")
    if len(block) % 16 > 0:
        raise Exception(f"Expected AES ciphertext with length multiple of 16\nGot ciphertext with length {len(block)} instead!")
    padding_length = block[-1]
    if padding_length == 0 or padding_length > 16:
        raise Exception(f"Expected Padding Length in interval [1,16], found {padding_length} instead!")
    for i in range(padding_length):
        if block[-1] != padding_length:
            raise Exception("Padding Not Compliant with PKCS#7")
        block = block[:-1]
    return bytes(block)
def ctr_gen_block(aes_key: bytes, nonce: int, ctr: int) -> bytes:
    nonce_bytes = bytearray(8)
    non = int(nonce)
    for i in range(8):
        nonce_bytes[i] = non%256
        non = non // 256
    counter_bytes = bytearray(8)
    count = int(ctr)
    for i in range(8):
        counter_bytes[i] = count%256
        count = count // 256
    block = bytearray(nonce_bytes)
    block.extend(counter_bytes)
    return encrypt_AES_ECB_128(bytes(block), aes_key)
def aes_ctr_keystream(aes_key: bytes, nonce: int) -> int:
    counter = 0
    while True:
        output = ctr_gen_block(aes_key, nonce, counter)
        for i in range(16):
            yield output[i]
        counter += 1
def is_valid_data(data):
    return type(data) in [bytes, bytearray]
def is_valid_key(key):
    return is_valid_data(key) and len(key) == 16
def is_valid_iv(iv):
    return is_valid_key(iv)
def is_valid_pad(plaintext: bytes) -> bool:
    if len(plaintext) % 16 > 0 or len(plaintext) < 16:
        return False
    plaintext = bytearray(plaintext[-16:])
    pad_len = plaintext[-1]
    if pad_len > 16 or pad_len == 0:
        return False
    for i in range(pad_len):
        if plaintext.pop() != pad_len:
            return False
    return True
def is_valid_ECB_padding(data, key):
    if not (is_valid_data(data) and len(data) == 16 and is_valid_key()):
        return False
    data = data[-16:]
    data = decrypt_block_128(data, key)
    return is_valid_pad(data)
def is_valid_CBC_padding(data, key, iv):
    if not (is_valid_data(data) and len(data) == 16 and is_valid_key()):
        return False
    while len(data) > 16:
        iv, data = data[:16], data[16:]
    data = decrypt_block_128(data, key)
    data = bytes([data[i] ^ iv[i] for i in range(16)])
    return is_valid_pad(data)
def encrypt_AES_ECB_128(data: bytes, aes_key: bytes) -> bytes:
    assert(is_valid_data(data))
    assert(is_valid_key(aes_key))
    output = bytearray()
    padded = False
    while not padded:
        if len(data) < 16:
            data = pad_block(data)
            padded = True
        output.extend(encrypt_block_128(bytes(data[:16]), aes_key))
        data = data[16:]
    return bytes(output)
def decrypt_AES_ECB_128(data: bytes, aes_key: bytes) -> bytes:
    assert(is_valid_data(data))
    assert(len(data) % 16 == 0)
    assert(is_valid_key(aes_key))
    output = bytearray()
    while len(data) > 0:
        new_block = decrypt_block_128(data[:16], aes_key)
        data = data[16:]
        if len(data) == 0:
            new_block = trim_padding(new_block)
        output.extend(new_block)
    return bytes(output)
def encrypt_AES_CBC_128(data: bytes, aes_key: bytes, iv: bytes) -> bytes:
    assert(is_valid_data(data))
    assert(is_valid_key(aes_key))
    assert(is_valid_iv(iv))
    output = bytearray()
    padded = False
    while not padded:
        if len(data) < 16:
            data = pad_block(data)
            padded = True
        new_block = bytes([data[:16] ^ iv[i] for i in range(16)])
        iv = encrypt_block_128(new_block, aes_key)
        output.extend(iv)
        data = data[16:]
    return bytes(output)
def decrypt_AES_CBC_128(data: bytes, aes_key: bytes, iv: bytes) -> bytes:
    assert(is_valid_data(data))
    assert(len(data) % 16 == 0)
    assert(is_valid_key(aes_key))
    assert(is_valid_iv(iv))
    output = bytearray()
    while len(data) > 0:
        plain_block = decrypt_block_128(data[:16], aes_key)
        plain_block = (bytes([iv[i] ^ plain_block[i] for i in range(16)]))
        iv = data[:16]
        data = data[16:]
        if len(data) == 0:
            plain_block = trim_padding(plain_block)
        output.extend(plain_block)
    return bytes(output)
def encrypt_AES_CTR(data: bytes, key: bytes, nonce: int) -> bytes:
    assert(is_valid_data(data))
    assert(is_valid_key(key))
    assert(type(nonce) == int)
    stream = aes_ctr_keystream(key, nonce)
    return bytes([i ^ next(stream) for i in data])
def decrypt_AES_CTR(data: bytes, key: bytes, nonce: int) -> bytes:
    return encrypt_AES_CTR(data, key, nonce)
