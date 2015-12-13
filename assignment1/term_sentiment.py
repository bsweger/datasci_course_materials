import sys
import json

def load_sentiments(sent_file):
    with open(sent_file) as s:
        rows = (line.split('\t') for line in s)
        d = {row[0]:int(row[1].strip()) for row in rows}
    return d

def main(sent_file, tweet_file):
    sentiment_dict = load_sentiments(sent_file)
    tweet_score_dict = {}
    new_words_dict = {}

    #calculate overall tweet sentiment scores
    with open(tweet_file) as t:
        for line in t:
            try:
                words = json.loads(line)['text'].split()
                tid = json.loads(line)['id']
            except:
                #assume objects w/o 'text' attribute aren't tweets
                continue
            score = 0
            for w in words:
                if w in sentiment_dict:
                    score += sentiment_dict[w]
                else:
                    #keep track of words that aren't in the AFINN list
                    if w in new_words_dict:
                        new_words_dict[w].append(tid)
                    else:
                        new_words_dict[w] = [tid]
            tweet_score_dict[tid] = score

    #for tweeted words w/o existing sentiment scores, do a rough estimation
    #of their sentiment based on whether they're used in positive or
    #negative tweets
    for key, val in new_words_dict.items():
        score = sum((tweet_score_dict[tid] for tid in val))
        print ('{} {}'.format(key, score))

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
