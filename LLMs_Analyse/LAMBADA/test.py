from openai import OpenAI
client = OpenAI()

files = client.files.list(purpose="fine-tune")
for f in files.data[:10]:
    print(f.id, f.filename, f.created_at)




