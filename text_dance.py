import json, random
from watson_developer_cloud import ToneAnalyzerV3

tone_analyzer = ToneAnalyzerV3(
	username='',
	password='',
	version='2017-09-26')

# 'database' of movements
fear_synonyms = ['Dreadfully', 'Uneasily', 'Nervously', 'Frightfully']
anger_synonyms = ['Forceful', 'Powerful', 'Authoritative', 'Vigorous']
confident_synonyms = ['Confidently', 'Calmly', 'Proudly']
sadness_synonyms = ['Lugubrious', 'Sulk', 'Mope', 'Sullen', 'Brood']
joy_synonyms = ['Ecstatically', 'Gleefully', 'Joyfully', 'Triumphant']

synonyms = {'fear': fear_synonyms, 'anger': anger_synonyms,
			'confident': confident_synonyms, 'sadness': sadness_synonyms,
			'joy': joy_synonyms, 'tentative': fear_synonyms, 'analytical': anger_synonyms}
body_parts = ['Head', 'Left Arm', 'Right Arm', 'Left Leg', 'Right Leg', 'Torso']
directions =['Left', 'Right', 'Up', 'Down', 'Forward', 'Backward']


def text_dance():
	#Take user input and store in JSON format. 
	user_input = raw_input('Welcome to Text2Dance!\nEnter some text: ')
	data = {"text": user_input}

	#Pass user's text in JSON format to Watson
	#Receive utf-8 encoded JSON from Watson, store in tone_json
	tone_json = tone_analyzer.tone(data)

	#initializes the list that stores tones associated with each sentence
	# ex. [[0, '', ''], [1, '', ''], [2, u'sadness', 0.772308], [3, u'joy', 0.500084], [3, u'confident', 0.849827]]
	# [[sentence_id, tone_id, score], [sentence_id, tone_id, score],[sentence_id, tone_id, score], ...]
	all_tones = []

	#returns tone_json's key-value pairs in the form of a list i.e.
	# [document_tone:'...', sentences_tone:'...']
	key_value_list = tone_json.items()

	#create a list from key_value_list where each item is a sentence
	#each sentence item also contains corresponding tones
	sentence_list = key_value_list[1][1]

	#overall_tone_list = key_value_list[0][1]

	#loop through sentences, extract the sentence id, tone id, and score
	#store each tone and associated values in all_tones list (even if the sentence doesn't have a tone!)
	for s in sentence_list:
		inner_list = []
		if s['tones'] != []:
			tones = s['tones']
			for i, item in enumerate(tones):
				inner_list.append(s['sentence_id'])
				inner_list.append(tones[i]['tone_id'])
				inner_list.append(tones[i]['score'])
				all_tones.append(inner_list)
				inner_list = []
		else:
			inner_list.append(s['sentence_id'])
			inner_list.append('')
			inner_list.append('')
			all_tones.append(inner_list)
	
	#TODO:
		# Choose body parts and directions in a non-random way
		# Possibly ignore sentences with a lower tone score?
		# Currently, this prints "just move around" for a sentence with an empty tone. 
		# We should either remove this or make it do something else

	#print dance moves in original sentence order with randomized movements/directions/body parts
	for i, tone in enumerate(all_tones):
		tone_id = tone[1]
		if tone_id:
			dance_move = random.choice(synonyms[tone_id]) + ' ' + random.choice(body_parts) + ' ' + random.choice(directions)
		else:
			dance_move = 'Just move around!'

		print '%s: %s' % (i, dance_move)


if __name__ == '__main__':
	text_dance()




