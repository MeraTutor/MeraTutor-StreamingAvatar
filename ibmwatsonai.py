from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import Model
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
from ibm_watsonx_ai.foundation_models.utils.enums import ModelTypes, DecodingMethods

from langchain import PromptTemplate
from langchain.chains import LLMChain
from ibm_watsonx_ai.foundation_models import Model
from ibm_watsonx_ai.foundation_models.utils.enums import ModelTypes


credentials = Credentials(
                   url = "https://jp-tok.ml.cloud.ibm.com",
                   api_key = "gopfcKupzvWPrQ-4lSef1Jp7EcltXXtJN5IriU4VoJ9g"
                  )

client = APIClient(credentials)

client.set.default_project("cb9d03e9-b2c9-4af1-92ed-96a070afc3a1")

# To display example params enter
GenParams().get_example_values()

generate_params = {
    GenParams.MAX_NEW_TOKENS: 25
}

model = Model(
    model_id=ModelTypes.FLAN_UL2,
    params=generate_params,
    credentials=Credentials(
        url = "https://jp-tok.ml.cloud.ibm.com",
        api_key = "gopfcKupzvWPrQ-4lSef1Jp7EcltXXtJN5IriU4VoJ9g"),
    project_id="cb9d03e9-b2c9-4af1-92ed-96a070afc3a1"
)

# q = "What is 1 + 1?"
# generated_response = model.generate(prompt=q)
# print(generated_response['results'][0]['generated_text'])

messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Who won the world series in 2020?"}
]
generated_response = model.chat_stream(messages=messages)

for chunk in generated_response:
    print(chunk['choices'][0]['delta'].get('content', ''), end='', flush=True)