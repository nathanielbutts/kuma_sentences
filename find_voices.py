import pyttsx3

def get_available_voices():
    # Initialize the pyttsx3 engine
    engine = pyttsx3.init()

    # Retrieve the list of available voices
    voices = engine.getProperty('voices')

    # Print the details of each available voice
    i = 0
    for voice in voices:
        print("ID["+str(i)+"]")
        print(f"Voice ID: {voice.id}")
        print(f"Name: {voice.name}")
        print(f"Languages: {voice.languages}")
        print(f"Gender: {voice.gender}")
        print(f"Age: {voice.age}")
        print()
        i += 1

def main():
    get_available_voices()

if __name__ == '__main__':
    main()
