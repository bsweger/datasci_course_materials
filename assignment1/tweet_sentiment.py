import sys
import json

def load_sentiments(sent_file):
    with open(sent_file) as s:
        rows = (line.split('\t') for line in s)
        d = {row[0]:int(row[1].strip()) for row in rows}
    return d

def main(sent_file, tweet_file):
    sentiment_dict = load_sentiments(sent_file)
    with open(tweet_file) as t:
        for line in t:
            try:
                words = json.loads(line)['text'].split()
            except:
                #assume objects w/o 'text' attribute aren't tweets
                continue
            score = sum((
                sentiment_dict[w] if w in sentiment_dict else 0 for w in words))
            print (score)

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
