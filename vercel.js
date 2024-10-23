import { openai } from '@ai-sdk/openai';
import { streamText } from 'ai';

const { textStream } = await streamText({
  model: openai('gpt-4-turbo'),
  prompt: 'Write a poem about embedding models.',
});

for await (const textPart of textStream) {
  console.log(textPart);
}