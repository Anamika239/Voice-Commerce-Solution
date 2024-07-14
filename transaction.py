from cryptography.fernet import Fernet
key = Fernet.generate_key()
cipher_suite = Fernet(key)
encrypted_data = cipher_suite.encrypt(b"Sensitive Data")
decrypted_data = cipher_suite.decrypt(encrypted_data)

print("Encrypted:", encrypted_data)
print("Decrypted:", decrypted_data)
