const express = require('express');
// const { WatsonxLLM } = require('langchain');
// const { WatsonxLLM } = require('langchain/llms/watsonx');
const { WatsonxAI } = require("@langchain/community/llms/watsonx_ai");


const path = require('path');
const { exit } = require('process');
// const app = express();
// app.use(express.json());

const llm = new WatsonxAI({
    ibmCloudApiKey: 'gopfcKupzvWPrQ-4lSef1Jp7EcltXXtJN5IriU4VoJ9g',
    projectId: 'cb9d03e9-b2c9-4af1-92ed-96a070afc3a1',
    modelId: 'ibm/granite-20b-multilingual',
    version: '2023-05-29',
    url: 'https://jp-tok.ml.cloud.ibm.com/ml/v1/text/generation?version=2023-05-29',
    headers: {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
    }
  });


  try {
    const prompt = "Write a short explanation about water cycle for grade 4";
    const input = `${prompt}`;
    // const response = llm.generate(input);
    const response = llm.generate(["Write a short explanation about water cycle for grade 4"]);
    console.log({ text: response });
  } catch (error) {
    console.error('Error calling LLM:', error);
    // res.status(500).send('Error processing your request');
  }

  //exit
  // function print(data) {
  //   console.log(JSON.stringify(data, null, 2));
  // }
exit
