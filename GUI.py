import os
import PySimpleGUI as sg
# import the functions that encode and decode our files
from Encoder import decrypt_file, encrypt_file

sg.theme('DarkAmber')    
sg.set_options(font=("Times New Roman", 16))  

# The popup that takes in the paths for the key
def keyLocation(prompt, button_name):
    # Layout for building the window
    layoutKey = [[sg.Text(prompt)],      
            [sg.Input(key='-IN-')],      
            [sg.Button(button_name), sg.Exit()]]
    windowKey = sg.Window('Text file encoder by Ryan Munger', layoutKey, finalize=True)
    # Window loop, checks for events
    while True:
        event, valueKey = windowKey.read() 
        key_location = valueKey['-IN-']
        key_location = str(key_location)
        # changes format for code to understand path
        key_location = key_location.replace('\\', "/")
        key_location = key_location.replace("\"", "")
        if event == sg.WIN_CLOSED or event == 'Exit':
            windowKey.close()
            return 'Failed'
        elif event == button_name:
            # Sanitize inputs to avoid errors later
            if os.path.exists(key_location):
                break
            else:
                sg.popup('Not a valid path!', 'You entered:', key_location, 'Please try again.', background_color="DarkRed")
    windowKey.close()
    return key_location


# When user chooses encrypt this window opens
def Encrypt():   
    layoutFormEn = [[sg.Text('Please input the file path below:')],      
            [sg.Input(key='-IN-')],      
            [sg.Button('Submit'), sg.Exit()]]  
    windowEn = sg.Window('Text file encoder by Ryan Munger', layoutFormEn, finalize=True)      
    
    # Event loop
    while True:    
        event, values = windowEn.read() 
        path_input = values['-IN-']
        # print(event, path_input)
        path_input = str(path_input)
        # modifies input to be useful
        path_input = path_input.replace('\\', "/")
        path_input = path_input.replace("\"", "")

        if event == sg.WIN_CLOSED or event == 'Exit':
            break      
        elif event == 'Submit':
            if os.path.exists(path_input):
                if os.path.isfile(path_input):
                    # Sanitizes inputs to make sure path is valid and it is a file we can use
                    key_location = keyLocation('Please input the path location to store your key:', 'Save Key')
                    if key_location != 'Failed':
                        encrypt_file(path_input, key_location)
                        sg.popup('Success!', 'The file at:', path_input, 'Has been encrypted. Thank you!', background_color="DarkGreen")
                    break
            else:
                sg.popup('Not a valid path!', 'You entered:', path_input, 'Please try again.', background_color="DarkRed")

    windowEn.close()


def Decrypt():  
    layoutFormDe = [[sg.Text('Please input the file path below:')],      
            [sg.Input(key='-IN-')],      
            [sg.Button('Submit'), sg.Exit()]]  
    windowDe = sg.Window('Text file decoder by Ryan Munger', layoutFormDe, finalize=True)      

    # Window Event Loop
    while True:                             
        event, values = windowDe.read() 
        path_input = values['-IN-']
        # print(event, path_input)
        path_input = str(path_input)
        # modifies input to be useful
        path_input = path_input.replace('\\', "/")
        path_input = path_input.replace("\"", "")

        if event == sg.WIN_CLOSED or event == 'Exit':
            break 
        elif event == 'Submit':
            if os.path.exists(path_input):
                if os.path.isfile(path_input):
                    # sanitized input
                    key_location = keyLocation('Please input the path of your key:', 'Submit Path')
                    if key_location != 'Failed':
                        # checks to see if sanitized input is valid for storage
                        decrypt_file(path_input, key_location)
                        sg.popup('Success!', 'The file at:', path_input, 'Has been decrypted. Thank you!', background_color="DarkGreen")
                    break
            else:
                sg.popup('Not a valid path!', 'You entered:', path_input, 'Please try again.', background_color="DarkRed")

    windowDe.close()


def main():
    layout = [[sg.Text('Please select your desired mode:')], [sg.Button('Encrypt'), sg.Button('Decrypt'), sg.Exit()]]   
    windowMain = sg.Window('Text file encoder', layout, finalize=True)
    
    # Window Event Loop, handles which windows launch and button presses
    while True:                             
            event, values = windowMain.read() 
            if event == sg.WIN_CLOSED or event == 'Exit':
                break      
            elif event == 'Encrypt':
                Encrypt()
            elif event == 'Decrypt':
                Decrypt()

    windowMain.close()


main()
