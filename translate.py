import csv
import openai
import pyttsx3
import json

#############
# Setup items
#############

make_audio = True # True synthesizes speech, False does not and only gives text response
save_audio = True # True will save the synthesized speech as mp3, false does not
create_or_translate = "translate" # Set to create to make a target language sentence from a vocab, set to translate to just do a one for one translation
audio_path = "audio\\" # Path to save the audio files
anki_path = "anki\\" # Path to save anki files (future improvement)
target_lang = "Japanese" # Set this as the language you wish to return (i.e. Japanese, Russian, English, etc.)

try:  # Set up your OpenAI API key
    with open('secrets.json') as f:
        data = json.load(f)
        openai.api_key = data["openai"]["api_key"]
except Exception as e:
    print("Error: ", e)

#Run find_voices.py to see which voices are available on your machine
#Choose list id which corresponds to Japanese
language_id = 2

#Setup rate of speed 0-1 (0-100%) of normal speaking rate
rate = 0.85

############
# Functions
############

def generate_target_sentence(input_text):
    # Set the parameters for the ChatGPT completion
    prompt = f"Create a beginner-level {target_lang} sentence using the following vocabulary word:\n{input_text}\nTranslation:"
    temperature = 0.8
    max_tokens = 50

    # Generate a response from ChatGPT
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=prompt,
        temperature=temperature,
        max_tokens=max_tokens,
        n=1,
        stop=None,
        #temperature_decay=0.6
    )

    # Extract the generated sentence from the response
    generated_sentence = response.choices[0].text.strip()

    return generated_sentence

def one_to_one_translation(input_text):
    # Set the parameters for the ChatGPT completion
    prompt = f"Translate {input_text} into {target_lang}:"
    temperature = 0.8
    max_tokens = 50

    # Generate a response from ChatGPT
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=prompt,
        temperature=temperature,
        max_tokens=max_tokens,
        n=1,
        stop=None,
        #temperature_decay=0.6
    )

    # Extract the generated sentence from the response
    generated_sentence = response.choices[0].text.strip()

    return generated_sentence

def save_output_file(input_word, generated_sentence):
    output_file = 'output.csv'
    with open(output_file, 'a', encoding='utf-8', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([input_word, generated_sentence])

def text_to_speech(text): #Synthesizes the speech into the chosen target language
    # Initialize the pyttsx3 engine
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    # for voice in voices:
    #     print(f"Voice: {voice.name}")
    engine.setProperty("voice", voices[language_id].id)
    engine.setProperty('rate', 150*rate)
    # Synthesize speech from the provided text
    engine.say(text)
    engine.runAndWait()

def save_speech_file(text,filename):
    engine = pyttsx3.init()
    engine.save_to_file(text, filename)
    engine.runAndWait()

def main():
    # Read the input text from the CSV file
    with open('input.csv', 'r', encoding='utf-8') as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            input_text = row[0]
            # Generate a beginner-level sentence
            if create_or_translate == "create":
                beginner_sentence = generate_target_sentence(input_text)
                print(f"Input: {input_text}")
                print(f"Generated Beginner-level Sentence: {beginner_sentence}")
            else:
                beginner_sentence = one_to_one_translation(input_text)
                print(f"Input: {input_text}")
                print(f"Translation: {beginner_sentence}")

            if make_audio: # synthesize text to speech
                text_to_speech(beginner_sentence)
            if save_audio and make_audio: # Save the speech file to mp3
                mp3File = audio_path + input_text + ".mp3"
                save_speech_file(beginner_sentence, mp3File)
            print()
            save_output_file(input_text, beginner_sentence)

##########
# Program 
##########

if __name__ == '__main__':
    main()
