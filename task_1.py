import Levenshtein
from spellchecker import SpellChecker
from transformers import pipeline

class SmartAutoCorrector:
    def __init__(self):
        self.spell = SpellChecker()
        self.grammar_corrector = pipeline("text2text-generation", model="prithivida/grammar_error_correcter_v1")

    def correct_spelling(self, word):
        if word in self.spell:
            return word, []
        
        correction = self.spell.correction(word)
        suggestions = sorted(self.spell.candidates(word), key=lambda w: Levenshtein.distance(word, w))[:3]
        
        return correction, suggestions

    def correct_sentence(self, sentence):
        words = sentence.split()
        corrected_words = []
        suggestions_dict = {}

        for word in words:
            corrected_word, suggestions = self.correct_spelling(word)
            corrected_words.append(corrected_word)
            if suggestions:
                suggestions_dict[word] = suggestions

        corrected_sentence = " ".join(corrected_words)
        return corrected_sentence, suggestions_dict

    def correct_grammar(self, sentence):
        result = self.grammar_corrector(sentence, max_length=128)[0]['generated_text']
        return result

    def correct_text(self, sentence):
        corrected_spelling, suggestions = self.correct_sentence(sentence)
        corrected_grammar = self.correct_grammar(corrected_spelling)
        
        return corrected_grammar, suggestions

    def autocomplete(self, partial_word):
        word_list = list(self.spell.word_frequency.keys())
        suggestions = sorted(word_list, key=lambda w: Levenshtein.distance(partial_word, w))[:5]
        return suggestions


if __name__ == "__main__":
    auto_corrector = SmartAutoCorrector()

    while True:
        choice = input("\nChoose an option:\n1. Correct Sentence\n2. Autocomplete\n3. Exit\nEnter choice: ")

        if choice == "1":
            user_input = input("Enter a sentence: ")
            final_output, word_suggestions = auto_corrector.correct_text(user_input)

            print("\nCorrected Sentence:", final_output)
            if word_suggestions:
                print("\nWord Suggestions:")
                for word, suggestions in word_suggestions.items():
                    print(f"{word} -> {suggestions}")

        elif choice == "2":
            partial_word = input("Enter partial word: ")
            suggestions = auto_corrector.autocomplete(partial_word)
            print("\nAutocomplete Suggestions:", suggestions)

        elif choice == "3":
            print("Exiting program.")
            break

        else:
            print("Invalid choice! Please try again.")
