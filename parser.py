import json
# prefix="/home/mooney/projects/your_activity_across_facebook/inbox/camillemoore_10161885047663975/"
prefix='/home/mooney/projects/crosswords/database/stew-facebook-history/messages/inbox/camillemoore_10161885047663975/'
# prefix="/home/mooney/projects/facebook_parser/"
filenames = [
    # "parser.py",
    'message_1.json',
    "message_2.json",
    "message_3.json",
    "message_4.json"
]

word_count = {}

for file in filenames:
    name = prefix + file
    f = open(name)    
    data = json.load(f)

    messages = data["messages"]
    for m in messages:
        if "content" in m:
            words = m["content"]
            words = words.split()
            for word in words:
                word = word.upper()
                if not word.isalnum():
                    continue
                if word in word_count:
                    word_count[word]+=1
                else:
                    word_count[word]=1
word_count = sorted((word_count[count], count) for count in word_count)
# print(word_count) 

word_count = word_count[::-1]
s = 0
for w in word_count:
    s+=w[0]
# print(s)
# word_count = word_count[:1000]
# print(top_1000)
from collections import OrderedDict
output = {}
for top in word_count:
    print(top)
    if any(char.isdigit() for char in  top[1]):
        continue
    if top[0] < 3:
        continue
    if len(top[1]) < 3:
        continue
    output[top[1]]=top[0]
filename="our_words"
with open(filename+".txt", "w") as output_file:
    for line in output:
        output_file.write(line + "\n")

output = json.dumps(output, indent=4)
print(output)
with open(filename+".json", "w") as outputfile:
    outputfile.write(output)








