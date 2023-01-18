from happytransformer import HappyGeneration
from happytransformer import GENSettings

happy_gen = HappyGeneration("GPT-NEOX", "EleutherAI/gpt-neox-20b")
args = GENSettings(no_repeat_ngram_size=2)

#result = happy_gen.generate_text(s because of aftershocks . </t> <t> Pushpa Basnet and 45 children she cares for were forced to evacuate their residence . </t> <t> Seven other CNN Heroes and their organizations now assisting in relief efforts . </t>", args=args)

#print(result.text)

greedy_settings = GENSettings(no_repeat_ngram_size=2, max_length=10)
output_greedy = happy_gen.generate_text(
    "Input: 'A State Department official \"pressured\" the FBI to change the classification of a Hillary Clinton email in a \"quid pro quo\", according to FBI documents.' Output: 'An official \"pressured\" the FBI.',  'The official is from the State Department.',  'The official wanted to change the classification of an email.',  'The email is Hillary Clinton's.', 'An official and the FBI are in a \"quid pro quo\".',  'This information is from FBI documents.' Input: 'American Jason Dufner will take a five-shot lead into the third round of the Memorial Tournament after carding an eagle on the 18th hole on Friday.' Output: ",
    args=greedy_settings)

beam_settings = GENSettings(num_beams=5, max_length=10)
output_beam_search = happy_gen.generate_text(
    "Input: 'A State Department official \"pressured\" the FBI to change the classification of a Hillary Clinton email in a \"quid pro quo\", according to FBI documents.' Output: 'An official \"pressured\" the FBI.',  'The official is from the State Department.',  'The official wanted to change the classification of an email.',  'The email is Hillary Clinton's.', 'An official and the FBI are in a \"quid pro quo\".',  'This information is from FBI documents.' Input: 'American Jason Dufner will take a five-shot lead into the third round of the Memorial Tournament after carding an eagle on the 18th hole on Friday.' Output: ",
    args=beam_settings)

generic_sampling_settings = GENSettings(do_sample=True, top_k=0, temperature=0.7, max_length=10)
output_generic_sampling = happy_gen.generate_text(
    "Input: 'A State Department official \"pressured\" the FBI to change the classification of a Hillary Clinton email in a \"quid pro quo\", according to FBI documents.' Output: 'An official \"pressured\" the FBI.',  'The official is from the State Department.',  'The official wanted to change the classification of an email.',  'The email is Hillary Clinton's.', 'An official and the FBI are in a \"quid pro quo\".',  'This information is from FBI documents.' Input: 'American Jason Dufner will take a five-shot lead into the third round of the Memorial Tournament after carding an eagle on the 18th hole on Friday.' Output: ",
    args=generic_sampling_settings)

top_k_sampling_settings = GENSettings(do_sample=True, top_k=50, temperature=0.7, max_length=10)
output_top_k_sampling = happy_gen.generate_text(
    "Input: 'A State Department official \"pressured\" the FBI to change the classification of a Hillary Clinton email in a \"quid pro quo\", according to FBI documents.' Output: 'An official \"pressured\" the FBI.',  'The official is from the State Department.',  'The official wanted to change the classification of an email.',  'The email is Hillary Clinton's.', 'An official and the FBI are in a \"quid pro quo\".',  'This information is from FBI documents.' Input: 'American Jason Dufner will take a five-shot lead into the third round of the Memorial Tournament after carding an eagle on the 18th hole on Friday.' Output: ",
    args=top_k_sampling_settings)

top_p_sampling_settings = GENSettings(do_sample=True, top_k=0, top_p=0.8, temperature=0.7, max_length=10)
output_top_p_sampling = happy_gen.generate_text(
    "Input: 'A State Department official \"pressured\" the FBI to change the classification of a Hillary Clinton email in a \"quid pro quo\", according to FBI documents.' Output: 'An official \"pressured\" the FBI.',  'The official is from the State Department.',  'The official wanted to change the classification of an email.',  'The email is Hillary Clinton's.', 'An official and the FBI are in a \"quid pro quo\".',  'This information is from FBI documents.' Input: 'American Jason Dufner will take a five-shot lead into the third round of the Memorial Tournament after carding an eagle on the 18th hole on Friday.' Output: ",
    args=top_p_sampling_settings)

bad_words_settings = GENSettings(bad_words=["new form", "social"])
output_bad_words = happy_gen.generate_text(
    "Input: 'A State Department official \"pressured\" the FBI to change the classification of a Hillary Clinton email in a \"quid pro quo\", according to FBI documents.' Output: 'An official \"pressured\" the FBI.',  'The official is from the State Department.',  'The official wanted to change the classification of an email.',  'The email is Hillary Clinton's.', 'An official and the FBI are in a \"quid pro quo\".',  'This information is from FBI documents.' Input: 'American Jason Dufner will take a five-shot lead into the third round of the Memorial Tournament after carding an eagle on the 18th hole on Friday.' Output: ",
    args=bad_words_settings)

print("Greedy:", output_greedy.text)  # a new field of research that has been gaining
print("Beam:", output_beam_search.text)  # one of the most promising areas of research in
print("Generic Sampling:", output_generic_sampling.text)  # an area of highly promising research, and a
print("Top-k Sampling:", output_top_k_sampling.text)  # a new form of social engineering. In this
print("Top-p Sampling:", output_top_p_sampling.text)  # a new form of social engineering. In this
print("Bad Words:", output_bad_words.text)  # a technology that enables us to help people deal