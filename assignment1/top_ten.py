import sys
import json
import collections

def main(tweet_file):

    hashtag_dict = {}
    hashtag_sorted = {}
    with open(tweet_file) as t:
        for line in t:
            try:
                tweet_obj = json.loads(line)
                words = tweet_obj['text'].split()
                hashtags = tweet_obj['entities']['hashtags']
            except:
                #skip non-tweets and tweets w/o entities data
                continue
            if hashtags and len(hashtags) > 0:
                for item in hashtags:
                    h = item['text']
                    if h in hashtag_dict:
                        hashtag_dict[h] = hashtag_dict[h] + 1
                    else:
                        hashtag_dict[h] = 1
    #reverse sort by hashtag counts
    for key, value in sorted(
        hashtag_dict.items(), key=lambda x: x[1], reverse=True):
        hashtag_sorted[key] = value
    c = collections.Counter(hashtag_sorted)
    for k, v in c.most_common(10):
        print ('{} {}'.format(k, v))

if __name__ == '__main__':
    main(sys.argv[1])
