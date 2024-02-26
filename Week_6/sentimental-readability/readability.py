text = input("Text: ")
print(text)

num_letters = 0
for char in text:
      if char.isalpha():
            num_letters += 1

num_words = len(text.split())
num_sentences = text.count('.') + text.count('?') + text.count('!')

if num_words == 0:
    L = 0
    S = 0
else:
      L = num_letters / num_words * 100
      S = num_sentences / num_words * 100

index = 0.0588 * L - 0.296 * S - 15.8
grade = round(index)

if grade < 1:
        print("Before Grade 1")
elif grade >= 16:
        print("Grade 16+")
else:
        print("Grade", grade)