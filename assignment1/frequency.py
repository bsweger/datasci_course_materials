import sys
import json

def load_sentiments(sent_file):
    with open(sent_file) as s:
        rows = (line.split('\t') for line in s)
        d = {row[0]:int(row[1].strip()) for row in rows}
    return d

def main(tweet_file):

    term_count = 0
    term_dict = {}
    with open(tweet_file) as t:
        for line in t:
            try:
                words = json.loads(line)['text'].split()
                tid = json.loads(line)['id']
            except:
                #assume objects w/o 'text' attribute aren't tweets
                continue
            for w in words:
                term_count += 1
                if w in term_dict:
                    term_dict[w] = term_dict[w] + 1
                else:
                    term_dict[w] = 1

    #calcuate term frequency
    for key, val in term_dict.items():
        print ('{} {}'.format(key, val/term_count))

if __name__ == '__main__':
    main(sys.argv[1])
