#pass prompt through tokenizer
#input string ~ prompt 
target_word_ids = tokenizer(target_word, add_special_tokens=False)['input_ids'] 
#you don't necessarily want the target word ids as a tensor now if you are passing 
#them into the model seperately to score them

input_ids = tokenizer(input_string, add_special_tokens=False, return_tensors='pt')['input_ids']

with torch.no_grad():
     #this is used to put the tokens tensor on the GPU when you use one
        #input_ids = input_ids.to("cuda")
    #use_cashe passes out the model state so you don't have to rerun the whole
     #input through the model to generate multiple consecutive tokens
      output = model(input_ids, use_cache=True)

#track model state after seeing next word and before we generate labels
model_state_cache = output['past_key_values']
logits = output['logits'].squeeze()
if logits.dim() > 1: logits = logits[-1]
#normalizing the raw model outputs (logits) into log probabilities
model_probs = F.log_softmax(logits, dim=-1)

target_word_subword_scores = []
for i, subword_id in enumerate(target_word_ids):

     #getting score of first subword from running the prompt through the model
   target_word_subword_scores.append(model_probs[subword_id].item())

   #keep running subword ids through if not last id for the target word
        if i+1 < len(target_word_ids):
         x = torch.LongTensor([[sbword_id]])
           #x = x.to("cuda")

               #pass the current subword in with the previous model state to get 
              #predictions for the output probabilities for the next subword conditioned
               #on the previous ones
         output = model(x, past_key_values=model_cache, use_cache=True)

            model_cache = output['past_key_values']
          logits = output['logits'].squeeze()
            model_probs = F.log_softmax(logits, dim=-1)

#get the average log probability across all subword tokens for single
#target word score
avg_score = sum(target_word_subword_scores)/len(target_word_subword_scores)