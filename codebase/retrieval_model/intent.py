import json

intent = {'intents': [
			{
				'tag': 'left',
				'patterns': [],
				'responses': []
			},
			{
				'tag': 'right',
				'patterns': [],
				'responses': []
			}]
		}

position_map = {"left": 0, "right": 1}

def generate_intent(file_handle, position):
	global intent
	data = file_handle.readlines()

	for row in data:
		temp = row.split('\t')
		intent['intents'][position]['patterns'].append(temp[0])
		intent['intents'][position]['responses'].append(temp[1].strip())

left_tweet_dataset = open('right_tweet_dataset.tsv', 'r')
generate_intent(left_tweet_dataset)
right_tweet = open('left_tweet_dataset.tsv', 'r')
generate_intent(right_tweet_dataset)

intent_file = open('intent.json', 'w')
json.dump(intent, intent_file)