import locale
locale.setlocale(locale.LC_ALL, "en_US")
import sys

def first_line(input_file, output_file):
    with open(input_file, "r") as f:
        first_line = f.readline()
    with open(output_file, "w") as g:
        g.write("Statistics about " + first_line)
def text_divided_into_words(input_file, output_file):
    words = []
    word = ""
    with open(input_file, "r") as f:
        for line in f:
            for letter in line:
                if letter.isalnum() or letter == "'" or letter == "_" or letter == "-":
                    word += letter
                else:
                    if word:
                        words.append(word.lower())
                        word = ""
            if word:
                words.append(word.lower())
                word = ""
    number_of_words = len(words)
    with open(output_file, "a") as g:
        g.write(f"Number of words: {number_of_words}\n")
    return words
def text_divided_into_sentences(input_file, output_file):
    sentences = []
    sentence = ""
    with open(input_file, "r") as f:
        for line in f:
            i = 0
            while i < len(line):
                if line[i:i + 3] == "...":
                    sentence += "..."
                    sentences.append(sentence)
                    sentence = ""
                    i += 3
                elif line[i].isalnum() or line[i] == "'" or line[i] == "_" or line[i] == "-" or line[i] == " ":
                    sentence += line[i]
                    i += 1
                elif line[i] == "." or line[i] == "?" or line[i] == "!":
                    sentence += line[i]
                    if sentence:
                        sentences.append(sentence)
                    sentence = ""
                    i += 1
                else:
                    sentence += line[i]
                    i += 1
            if sentence.strip():
                sentences.append(sentence.strip())
                sentence = ""
    number_of_sentences = len(sentences)
    with open(output_file, "a") as g:
        g.write(f"Number of sentences: {number_of_sentences}\n")
    return sentences
def words_per_sentences(input_file, output_file):
    words = []
    word = ""
    with open(input_file, "r") as f:
        for line in f:
            for letter in line:
                if letter.isalnum() or letter == "'" or letter == "_" or letter == "-":
                    word += letter
                else:
                    if word:
                        words.append(word.lower())
                        word = ""
            if word:
                words.append(word.lower())
                word = ""
    total_words = len(words)
    sentences = []
    sentence = ""
    with open(input_file, "r") as f:
        for line in f:
            i = 0
            while i < len(line):
                if line[i:i + 3] == "...":
                    sentence += "..."
                    sentences.append(sentence)
                    sentence = ""
                    i += 3
                elif line[i].isalnum() or line[i] == "'" or line[i] == "_" or line[i] == "-" or line[i] == " ":
                    sentence += line[i]
                    i += 1
                elif line[i] == "." or line[i] == "?" or line[i] == "!":
                    sentence += line[i]
                    if sentence:
                        sentences.append(sentence)
                    sentence = ""
                    i += 1
                else:
                    sentence += line[i]
                    i += 1
            if sentence.strip():
                sentences.append(sentence.strip())
                sentence = ""
    total_sentences = len(sentences)
    total_words = len(words)
    total_sentences = len(sentences)
    average = total_words/total_sentences
    with open(output_file, "a") as g:
        g.write(f"Words/Sentences: {average:.2f}\n")
def number_of_characters(input_file, output_file):
    with open(input_file, "r") as f:
        text = f.read()
    total_c = len(text)
    with open(output_file, "a") as g:
        g.write(f"Characters: {total_c}\n")
def characters_in_words(input_file, output_file):
    aa = []
    word = ""
    with open(input_file, "r") as f:
        for line in f:
            for letter in line:
                if letter.isalnum() or letter == "'" or letter == "_" or letter == "-":
                    word += letter
                else:
                    if word:
                        aa.append(word.lower())
                        word = ""
            if word:
                aa.append(word.lower())
                word = ""
    total_c = 0
    for word in aa:
        total_c += len(word)
    with open(output_file, "a") as g:
        g.write(f"Characters (Just words): {total_c}\n")
def shortest_and_longest_words(input_file, output_file):
    aa = []
    word = ""
    with open(input_file, "r") as f:
        for line in f:
            for letter in line:
                if letter.isalnum() or letter == "'" or letter == "_" or letter == "-":
                    word += letter
                else:
                    if word:
                        aa.append(word.lower())
                        word = ""
            if word:
                aa.append(word.lower())
                word = ""
        number_of_words = len(aa)
    word_counts = {}
    for word in aa:
        if word in word_counts:
            word_counts[word] += 1
        else:
            word_counts[word] = 1
    min_length = min(len(word) for word in aa)
    max_length = max(len(word) for word in aa)
    shortest = []
    longest = []
    for word, count in word_counts.items():
        if len(word) == min_length:
            shortest.append((word, count))
        elif len(word) == max_length:
            longest.append((word, count))
    shortest.sort(key=lambda x: (-x[1], x[0]))
    longest.sort(key=lambda x: (-x[1], x[0]))
    with open(output_file, "a") as g:
        for word, count in shortest:
            g.write(f"Shortest word: {word} ({count/number_of_words:.4f})\n")
        for word, count in longest:
            g.write(f"Longest word: {word} ({count/number_of_words:.4f})\n")
def frequencies_of_words(input_file, output_file):
    aa = []
    word = ""
    with open(input_file, "r") as f:
        for line in f:
            for letter in line:
                if letter.isalnum() or letter == "'" or letter == "_" or letter == "-":
                    word += letter
                else:
                    if word:
                        aa.append(word.lower())
                        word = ""
            if word:
                aa.append(word.lower())
                word = ""
    number_of_words = len(aa)
    word_counts = {}
    for word in aa:
        word_counts[word] = word_counts.get(word, 0) + 1
    word_frequencies = [(word, count / number_of_words) for word, count in word_counts.items()]
    word_frequencies.sort(key=lambda x: (-x[1], x[0]))
    with open(output_file, "a") as g:
        g.write("\nWords and Frequencies:\n")
        for word, frequency in word_frequencies:
            g.write(f"{word}: {frequency:.4f}\n")

def main():
    input_file = sys.argv[1]
    output_file = "output.txt"

    try:
        with open(input_file, "r") as f:
            content = f.read()
            print(f"Input file content:\n{content}")
        with open(output_file, "w") as f:
            f.write("Output file created successfully.\n")
            f.write(content)
        first_line(input_file, output_file)
        text_divided_into_words(input_file, output_file)
        text_divided_into_sentences(input_file, output_file)
        words_per_sentences(input_file, output_file)
        number_of_characters(input_file, output_file)
        characters_in_words(input_file, output_file)
        shortest_and_longest_words(input_file, output_file)
        frequencies_of_words(input_file, output_file)

    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    main()
