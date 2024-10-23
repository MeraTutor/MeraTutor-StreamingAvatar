const express = require('express');
// const { WatsonxLLM } = require('langchain');
// const { WatsonxLLM } = require('langchain/llms/watsonx');
const { WatsonxAI } = require("@langchain/community/llms/watsonx_ai");

const path = require('path');
const app = express();
app.use(express.json());

const llm = new WatsonxAI({
    ibmCloudApiKey: 'gopfcKupzvWPrQ-4lSef1Jp7EcltXXtJN5IriU4VoJ9g',
    projectId: 'cb9d03e9-b2c9-4af1-92ed-96a070afc3a1',
    modelId: 'ibm/granite-20b-multilingual',
    version: '2023-05-29',
    url: 'https://jp-tok.ml.cloud.ibm.com/ml/v1/text/generation?version=2023-05-29',
    headers: {
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    }
  });

  
const systemSetup = "You are an friendly AI teacher responsible for teaching concepts and helping students understand difficult topics. Be friendly with kids and answer to all greeting initially. You have helped students understand complex topics by using available study materials. Explain in 3-4 sentences and format the output in html "

app.use(express.static(path.join(__dirname, '.')));

app.post('/openai/complete', async (req, res) => {
  try {
    const prompt = req.body.prompt;
    const input = `${systemSetup}\n${prompt}`;
    //const response = await llm.generate(input);
    const result = await llm.generate(input);
    console.log(result.response.text())
    res.json({ text: result.response.text() });
  } catch (error) {
    console.error('Error calling LLM:', error);
    res.status(500).send('Error processing your request');
  }
});

app.listen(3000, function () {
  // document.getElementById("notes").innerHTML += "<p> Welcome!</p>";
  console.log('App is listening on port 3000!');
});