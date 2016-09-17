# odpre pdf in sprinta tekst kot string
import slate

with open('cilensek_stanislav.pdf','rb') as f:
    doc = slate.PDF(f)

print(len(doc))
print(doc[1]) 
