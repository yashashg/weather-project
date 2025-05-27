// src/App.jsx
import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';

function App() {
  const [location, setLocation] = useState('');
  const [dateQueried, setDateQueried] = useState('');
  const [sessionId, setSessionId] = useState('');
  const [response, setResponse] = useState('');
  const [queries, setQueries] = useState([]);

  
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const chatEndRef = useRef(null);


  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMsg = { sender: 'user', text: input };
    setMessages(prev => [...prev, userMsg]);
    setInput('');

    try {
      const res = await axios.post('http://localhost:8000/response', {
        query: input,
      });
      const data = res.data;
      let botText = '';
      if (data.error) {
        botText = `Error: ${data.error}`;
      } else {
        botText = data;
      }

      setMessages(prev => [...prev, { sender: 'bot', text: botText }]);
    } catch (err) {
      console.error(err);
      setMessages(prev => [...prev, { sender: 'bot', text: 'Sorry, failed to fetch data.' }]);
    }
  };


  const fetchQueries = async () => {
    try {
      const res = await axios.get("http://localhost:8000/read/");
      setQueries(res.data);
    } catch (err) {
      console.error("Error fetching queries", err);
    }
  };

  const handleSubmit = async () => {
    try {
await axios.post("http://localhost:8000/create/", null, {
  params: {
    location,
    date_queried: dateQueried,
    session_id: sessionId,
    response
  }
});
      fetchQueries();  // refresh data
      setLocation('');
      setDateQueried('');
      setSessionId('');
      setResponse('');
    } catch (err) {
      console.error("Error submitting query", err);
    }
  };

  useEffect(() => {
    fetchQueries();
  }, []);


  return (
    <div>
    <link href="./index.css" rel="stylesheet" />
    <div className="min-h-screen bg-gray-100 flex flex-col items-center justify-center p-4">
      <div className="bg-white shadow-md rounded-xl w-full max-w-md flex flex-col h-[80vh]">
        <div className="p-4 font-bold text-indigo-700 text-xl border-b">Weather Assistant Chat</div>
        <div className="flex-1 overflow-y-auto p-4 space-y-3">
          {messages.map((msg, i) => (
            <div
              key={i}
              className={`max-w-xs px-4 py-2 rounded-xl text-sm ${
                msg.sender === 'user'
                  ? 'bg-indigo-200 self-end text-right'
                  : 'bg-gray-200 self-start text-left'
              }`}
            >
              {msg.text}
            </div>
          ))}
          <div ref={chatEndRef} />
        </div>
        <form onSubmit={handleSend} className="p-4 border-t flex gap-2">
          <input
            type="text"
            className="flex-1 p-2 border rounded-xl"
            placeholder="Ask about weather..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
          />
          <button
            type="submit"
            className="bg-indigo-600 text-white px-4 py-2 rounded-xl hover:bg-indigo-700"
          >
            Send
          </button>
        </form>
      </div>
    </div>
    <div className="p-4 max-w-xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">Weather Query Manager</h1>

      <div className="mb-4 space-y-2">
        <input type="text" placeholder="Location" value={location}
          onChange={(e) => setLocation(e.target.value)} className="border p-2 w-full" />

        <input type="date" value={dateQueried}
          onChange={(e) => setDateQueried(e.target.value)} className="border p-2 w-full" />

        <input type="text" placeholder="Session ID" value={sessionId}
          onChange={(e) => setSessionId(e.target.value)} className="border p-2 w-full" />

        <textarea placeholder="Weather Response" value={response}
          onChange={(e) => setResponse(e.target.value)} className="border p-2 w-full" />

        <button onClick={handleSubmit} className="bg-blue-600 text-white px-4 py-2 rounded">
          Submit
        </button>
      </div>

      <hr className="my-4" />

      <h2 className="text-xl font-semibold mb-2">Stored Weather Queries</h2>
      <ul className="space-y-2">
        {queries.map((q) => (
          <li key={q.id} className="border p-2 rounded">
            <strong>{q.location}</strong> | {q.date_queried} | Session: {q.session_id}<br />
            <span className="text-gray-600 text-sm">Response: {q.response}</span>
          </li>
        ))}
      </ul>
    </div>


    </div>
  );
}

export default App;
