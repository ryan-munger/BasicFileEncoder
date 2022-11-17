import os
from datetime import datetime
# Grabbing the conversion lists from a different file bc they are long
from Conversions import letter_num_convert
from Conversions import num_letter_convert


def create_key(decode, key_path, name):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    current_time = current_time.replace(':', '_')
    # Makes the new file's path and names it including the current time and name of the file the key is for
    key_final = os.path.join(key_path, "Key_" + name + '_' + current_time + ".txt")
    # print(key_final)
    create = open(key_final, 'w+')
    # populates the key file with the elements needed to decode
    for x in range(len(decode)):
        create.write(str(decode[x]))
    create.close()


# simple, replaces letters with numbers
def encrypt_file(msg_path, key_path):
    msg = open(msg_path, 'r+') #opening the file in read + mode so we can make changes
    msg_txt = msg.read()
    msg_list = list(msg_txt) # breaks up each character into a list element 
    decode = [] # holds the key needed to decode the new message
    
    for x in range(len(msg_list)): # changes each letter to a number and logs the length of each number so we can decode later
        msg_list[x] = letter_num_convert[msg_list[x]] # example: 11 can be aa or f, we must store a key
        decode.append(len(msg_list[x]))
    
    msg_txt = "".join(msg_list)
    msg.seek(0, os.SEEK_SET) # moves cursor to the start of the file such that writing will replace the old msg
    
    msg.write(msg_txt)
    print("Successfully Encrypted")

    #Builds a name for the key from the name of the encrypted file
    name_start = msg_path.rfind('/') + 1
    name_end = msg_path.rfind('.') 
    name = msg_path[name_start: name_end]
    create_key(decode, key_path, name)
    msg.close()
    return decode # returns the key 
    

def decrypt_file(msg_path, key_path):
    msg = open(msg_path, 'r+') #opening the file in read + mode so we can make changes
    msg_txt = msg.read()
    msg_list = list(msg_txt) # breaks up each character into a list element

    key = open(key_path, 'r+')
    decode = key.read()
    decode = list(decode)

    decoded_msg = ""
    count = 0
    # Breaks the encoded message into chunks of size depicted by the decode list
    # Converts the chunks back into text
    for x in range(len(decode)):
        current = ""
        for i in range(int(decode[x])):
            current += msg_list[count]
            count+=1
        decoded_msg += num_letter_convert[current]
    
    msg.truncate(0) # deletes the current stuff stored in the file by setting its size to 0 bytes
    msg.seek(0, os.SEEK_SET) # moves cursor to the start of the file
    msg.write(decoded_msg)
    print('Successfully Decrypted')

    msg.close()
    key.close()
    # Deletes the key as you no longer need it
    os.unlink(key_path)
    print("Deleted the key")
    