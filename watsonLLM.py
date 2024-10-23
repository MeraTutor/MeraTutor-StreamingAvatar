import requests

url = "https://jp-tok.ml.cloud.ibm.com/ml/v1/text/generation?version=2023-05-29"

body = {
	"input": """<|system|>
You are a class 4 Science teacher, you will be explaing the topic of your choice first and then after the explanation. You can Provide user on what to do next from these mini tasks: 
1) ask questions first and then listen to the answers and provide feedback. make it interactive with multichoice questions, one line answers. begin with a topic of your choice.
2) Provdide relevant assignments.
<|assistant|>
""",
	"parameters": {
		"decoding_method": "greedy",
		"max_new_tokens": 900,
		"min_new_tokens": 10,
		"repetition_penalty": 1.05
	},
	"model_id": "ibm/granite-20b-multilingual",
	"project_id": "cb9d03e9-b2c9-4af1-92ed-96a070afc3a1"
}

headers = {
	"Accept": "application/json",
	"Content-Type": "application/json",
	"Authorization": "Bearer LdqPoAbXTz1w9__ltxQ7IExB8FHooocrnCY8qVdjIzKd"
}

response = requests.post(
	url,
	headers=headers,
	json=body
)

if response.status_code != 200:
	raise Exception("Non-200 response: " + str(response.text))

data = response.json()