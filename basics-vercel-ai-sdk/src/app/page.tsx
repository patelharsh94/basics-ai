'use client';

import { useChat } from '@ai-sdk/react';
import { use, useState } from 'react';

export default function Home() {

  const [input, setInput] = useState('');
  const {messages, sendMessage} = useChat();

  async function submitMessage(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const response = await fetch('http://localhost:8000/prompt/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'accept': 'application/json'
      },
      body: JSON.stringify({
        request_prompt: input,
      })
    })
    const resVal = await response.json()
    // messages.push(resVal)
    console.log('GOT RESPONSE: ', resVal)
    setInput('')
  }


  return (
    <div className="flex flex-col min-h-full w-full max-w-md py-24 mx-auto stretch">
      {
        messages.map(message => (
          <div key={message.id} className="whitespace-pre-wrap">
            {message.role === 'user' ? 'User: ' : 'AI: '}
            {message.parts.map((part, i) => {
              switch (part.type) {
                case 'text':
                  return <div key={`${message.id}-${i}`}>{part.text}</div>;
              }
            })}
          </div>
        ))
      }

      <form
        onSubmit={submitMessage}
      >
        <input
          className="fixed dark:bg-zinc-900 bottom-0 w-full max-w-md p-2 mb-8 border border-zinc-300 dark:border-zinc-800 rounded shadow-xl"
          value={input}
          placeholder="Say something..."
          onChange={e => setInput(e.currentTarget.value)} />
      </form>
    </div>
  );
}
