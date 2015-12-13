import sys
import json

STATES = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
}

def load_sentiments(sent_file):
    with open(sent_file) as s:
        rows = (line.split('\t') for line in s)
        d = {row[0]:int(row[1].strip()) for row in rows}
    return d

def main(sent_file, tweet_file):
    sentiment_dict = load_sentiments(sent_file)
    states = {v:k for k, v in STATES.items()}
    high_score = None
    high_state = ''
    with open(tweet_file) as t:
        for line in t:
            jsontweet = json.loads(line)
            try:
                words = jsontweet['text'].split()
            except:
                #assume objects w/o 'text' attribute aren't tweets
                continue
            place = jsontweet['place']
            if place and place['country_code'] == 'US':
                #not-too-thorough parsing out of state abbreviation
                full_name = place['full_name']
                if full_name.split(', ')[-1] in STATES:
                    state_abbr = full_name.split(', ')[-1]
                elif full_name.split(', ')[0] in states:
                    state_abbr = states.get(full_name.split(', ')[0])
            else:
                #skip non-US tweets
                continue
            #calculate tweet sentiment
            score = sum((
                sentiment_dict[w] if w in sentiment_dict else 0 for w in words))
            if (high_score and score > high_score) or not high_score:
                high_score = score
                high_state = state_abbr
        print (high_state)

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
