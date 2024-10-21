import codecs
import os
import csv
import re
import numpy as np
import argparse
import random

random.seed(42)

from transformers import RobertaTokenizer

tokenizer = RobertaTokenizer.from_pretrained('roberta-base', do_lower_case=True)

parser = argparse.ArgumentParser("process_data")
parser.add_argument("--input_path", type=str, help="path to input data")
parser.add_argument("--output_path", type=str, help="path to output data")
args = parser.parse_args()

input_file = codecs.open(args.input_path, 'r', 'utf-8')
output_file = codecs.open(args.output_path, 'w', 'utf-8')
output_file2 = codecs.open(args.output_path.split(".csv")[0] + "-test.csv",'w','utf-8')

csv_reader = [row for row in csv.reader(input_file, delimiter = ',', quotechar='"')]
csv_reader = csv_reader[1:]

csv_writer = csv.writer(output_file, delimiter = ',',quotechar='"') 
csv_writer2 = csv.writer(output_file2, delimiter = ',',quotechar='"')

csv_writer.writerow(["id","seeker_post","response_post","level","rationale_labels","rationale_labels_trimmed","response_post_masked"])
csv_writer2.writerow(["id","seeker_post","response_post","level","rationale_labels","rationale_labels_trimmed","response_post_masked"])
test_idx = random.sample(range(len(csv_reader)),int(len(csv_reader)*.10))

for i,row in enumerate(csv_reader):
        # sp_id,rp_id,seeker_post,response_post,level,rationales
        seeker_post = row[2].strip()
        response = row[3].strip()
        response_masked = response
        response_tokenized = tokenizer.decode(tokenizer.encode_plus(response, add_special_tokens = True, max_length = 64, pad_to_max_length = True)['input_ids'], clean_up_tokenization_spaces=False)
        response_tokenized_non_padded = tokenizer.decode(tokenizer.encode_plus(response, add_special_tokens = True, max_length = 64, pad_to_max_length = False)['input_ids'], clean_up_tokenization_spaces=False)
        response_words = tokenizer.tokenize(response_tokenized)
        response_non_padded_words = tokenizer.tokenize(response_tokenized_non_padded)
        if len(response_words) != 64:
           continue
        response_words_position = np.zeros((len(response),), dtype=np.int32)
        rationales = row[5].strip().split('|')
        rationale_labels = np.zeros((len(response_words),), dtype=np.int32)
        curr_position = 0
        for idx in range(len(response_words)):
            curr_word = response_words[idx]
            if curr_word.startswith('Ġ'):
               curr_word = curr_word[1:]
               response_words_position[curr_position: curr_position+len(curr_word)+1] = idx
               curr_position += len(curr_word)+1

        if len(rationales) == 0 or row[5].strip() == '':
            rationale_labels[1:len(response_non_padded_words)] = 1
            response_masked = ''

        for r in rationales:
            if r == '':
               continue
            try:
               r_tokenizer = tokenizer.decode(tokenizer.encode(r, add_special_tokens = False))
               match = re.search(r_tokenizer , response_tokenized)
               curr_match = response_words_position[match.start(0):match.start(0)+len(r_tokenizer)]
               curr_match = list(set(curr_match))
               curr_match.sort()
               response_masked = response_masked.replace(r, ' ')
               response_masked = re.sub(r' +', ' ', response_masked)
               rationale_labels[curr_match] = 1
            except:
               continue
        rationale_labels_str = ','.join(str(x) for x in rationale_labels)
        rationale_labels_str_trimmed = ','.join(str(x) for x in rationale_labels[1:len(response_non_padded_words)])
        if i in test_idx:
            csv_writer2.writerow([row[0] + '_' + row[1], seeker_post, response, row[4], rationale_labels_str, len(rationale_labels_str_trimmed), response_masked])
        else:
            csv_writer.writerow([row[0] + '_' + row[1], seeker_post, response, row[4], rationale_labels_str, len(rationale_labels_str_trimmed), response_masked])

input_file.close()
output_file.close()
