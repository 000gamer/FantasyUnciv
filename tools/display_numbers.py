"""Format signed native modifier parameters. Counts, turns and probabilities are unchanged."""
import re
_CACHE={}

def parts(text):
 values=[];chunks=[];start=None;depth=0;last=0
 for i,c in enumerate(text):
  if c=='[':
   if depth==0:start=i;chunks.append(text[last:i])
   depth+=1
  elif c==']':
   depth-=1
   if depth==0:
    values.append(text[start+1:i]);chunks.append('[]');last=i+1
 chunks.append(text[last:]);return ''.join(chunks),values

def signed(text,config):
 body,*tail=text.split(' <',1);shape,values=parts(body)
 if id(config)not in _CACHE:_CACHE[id(config)]={parts(t)[0]:v for t,v in config['rules'].items()}
 indices=_CACHE[id(config)].get(shape)
 if indices is None:return text
 for i in indices:
  if i<len(values)and re.fullmatch(r'\d+',values[i])and int(values[i])>0:values[i]='+'+values[i]
 # Rebuild outer parameters without altering nested filters or modifiers.
 out=[];depth=0;last=0;index=0
 for i,c in enumerate(body):
  if c=='[':
   if depth==0:out.append(body[last:i])
   depth+=1
  elif c==']':
   depth-=1
   if depth==0:out.append('['+values[index]+']');index+=1;last=i+1
 out.append(body[last:]);return ''.join(out)+(' <'+tail[0]if tail else'')

def normalize_tree(value,config):
 if isinstance(value,list):return [normalize_tree(v,config)for v in value]
 if isinstance(value,dict):return {k:([signed(v,config)for v in x]if k in ['uniques','friendBonusUniques','allyBonusUniques']else normalize_tree(x,config))for k,x in value.items()}
 return value
