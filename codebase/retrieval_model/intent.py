import json
import numpy as np

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
	np.random.shuffle(data)

	training_data = data[0:int(0.8*len(data))]
	testing_data = data[int(0.8*len(data)):]

	for row in training_data:
		temp = row.split('\t')
		intent['intents'][position]['patterns'].append(temp[0])
		intent['intents'][position]['responses'].append(temp[1].strip())

	test_file = open("test_" + file_handle.name.split("/")[-1], "w")
	for row in testing_data:
		test_file.write(row)

left_tweet_dataset = open('../../dataset/right_tweet_dataset.tsv', 'r')
generate_intent(left_tweet_dataset, 1)
right_tweet_dataset = open('../../dataset/left_tweet_dataset.tsv', 'r')
generate_intent(right_tweet_dataset, 0)

intent_file = open('intent.json', 'w')
json.dump(intent, intent_file)