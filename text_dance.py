import json, random
from watson_developer_cloud import ToneAnalyzerV3

tone_analyzer = ToneAnalyzerV3(
	username='',
	password='',
	version='2017-09-26')

# 'database' of movements
fear_synonyms = ['hesitantly', 'uneasily', 'nervously', 'frightfully']
anger_synonyms = ['forcefully!', 'powerfully!', 'authoritatively', 'vigorously']
confident_synonyms = ['confidently!', 'calmly', 'proudly!', 'assertively!']
sadness_synonyms = ['mournfully', 'sulkily', 'slowly', 'sullenly']
joy_synonyms = ['ecstatically', 'gleefully', 'joyfully', 'triumphantly!']

synonyms = {'fear': fear_synonyms, 'anger': anger_synonyms,
			'confident': confident_synonyms, 'sadness': sadness_synonyms,
			'joy': joy_synonyms, 'tentative': ['nervously'], 'analytical': anger_synonyms}
body_parts = ['head', 'left arm', 'right arm', 'left leg', 'right leg', 'torso', 'body']
directions =['to the left', 'to the right', 'up', 'down', 'forward', 'backward']

movements = ['Just move around!', 'Spin!', 'Fall!', 'Jump!', 'Grab a friend!', 'Shimmy!']


def text_dance():
	#Take user input and store in JSON format.
	print '\nWelcome to Text2Dance!'
	print '\nAn interactive program that translates text to a list of dance movements.'
	print 'Please type a minimum of 1 sentence and up to 100 sentences to see how your story can be formed into a dance!'
	user_input = raw_input('\nEnter text: ')
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

	#check if sentence_tones exist -- if not, just use document-level tone.
	if len(key_value_list) > 1:
		#create a list from key_value_list where each item is a sentence
		#each sentence item also contains corresponding tones
		sentence_list = key_value_list[1][1]

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
	else: #case where there is no sentence-level tone, only document-level tone
		overall_list = key_value_list[0][1]['tones']
		inner_list = []
		if overall_list != []:
			for t in overall_list:
				inner_list = []
				inner_list.append('doc_tone')
				inner_list.append(t['tone_id'])
				inner_list.append(t['score'])
				all_tones.append(inner_list)
		else:
			inner_list.append('doc_tone')
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
			dance_move = 'Move your ' + random.choice(body_parts) + ' ' + random.choice(directions) + ' ' + random.choice(synonyms[tone_id])
		else:
			dance_move = random.choice(movements)
		print '\n%s: %s' %(i, dance_move)
	print '\nThis is your story interpreted as a dance. Now, add a song and record your dance!\n'

if __name__ == '__main__':
	text_dance()