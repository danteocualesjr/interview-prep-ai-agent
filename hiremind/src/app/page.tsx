'use client'

import { useState, useRef, useEffect } from 'react'
import { Send, Sparkles } from 'lucide-react'

type Message = {
  content: string
  sender: 'user' | 'ai'
}

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([
    { content: "Hello! I'm HireMind, your interview prep assistant. Please enter the Job Position you're applying for and we'll begin our interview prep session.", sender: 'ai' }
  ])
  const [input, setInput] = useState('')
  const [isTyping, setIsTyping] = useState(false)
  const [jobPosition, setJobPosition] = useState('')
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(scrollToBottom, [messages])

  const handleSend = async () => {
    if (input.trim()) {
      setMessages(prev => [...prev, { content: input, sender: 'user' }])
      setInput('')
      setIsTyping(true)
      
      // Simulating AI response
      setTimeout(() => {
        let aiResponse = ''
        if (!jobPosition) {
          setJobPosition(input)
          aiResponse = `Great! I see you're preparing for a ${input} role. Let's start our interview prep session. What specific area would you like to focus on? You can choose from: Work Experience, Technical Skills, Behavioral Questions, Company Knowledge, or Career Goals.`
        } else {
          aiResponse = `That's a great area to focus on for your ${jobPosition} interview. Here's a sample question: "Can you tell me about a challenging project you worked on and how you overcame obstacles?"`
        }
        setMessages(prev => [...prev, { content: aiResponse, sender: 'ai' }])
        setIsTyping(false)
      }, 1500)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-orange-50 to-amber-100 flex items-center justify-center p-4">
      <div className="w-full max-w-2xl mx-auto h-[600px] flex flex-col shadow-xl bg-white/80 backdrop-blur-sm rounded-lg">
        <div className="flex flex-row items-center gap-3 p-4 bg-gradient-to-r from-orange-400 to-amber-500 text-white rounded-t-lg">
          <div className="h-10 w-10 border-2 border-white rounded-full bg-white/20 flex items-center justify-center">
            AI
          </div>
          <h2 className="text-2xl font-bold">HireMind</h2>
          <Sparkles className="ml-auto h-5 w-5 text-yellow-200" />
        </div>
        
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.map((message, index) => (
            <div key={index} className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'} animate-fadeIn`}>
              <div 
                className={`max-w-[80%] rounded-lg p-3 ${
                  message.sender === 'user' 
                    ? 'bg-gradient-to-br from-orange-400 to-amber-500 text-white' 
                    : 'bg-gray-100 text-gray-800'
                } shadow-md`}
              >
                {message.content}
              </div>
            </div>
          ))}
          {isTyping && (
            <div className="flex justify-start animate-fadeIn">
              <div className="bg-gray-100 rounded-lg p-3 max-w-[80%] shadow-md">
                <div className="flex space-x-2">
                  <div className="w-3 h-3 bg-orange-400 rounded-full animate-bounce"></div>
                  <div className="w-3 h-3 bg-amber-500 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                  <div className="w-3 h-3 bg-orange-600 rounded-full animate-bounce" style={{ animationDelay: '0.4s' }}></div>
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>
        
        <div className="p-4 bg-white rounded-b-lg border-t border-gray-200">
          <form onSubmit={(e) => { e.preventDefault(); handleSend(); }} className="flex w-full gap-2">
            <input
              placeholder="Type your message here..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              className="flex-1 px-3 py-2 bg-gray-50 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-400 focus:border-transparent"
            />
            <button 
              type="submit" 
              className="p-2 bg-gradient-to-r from-orange-400 to-amber-500 text-white rounded-lg hover:from-orange-500 hover:to-amber-600 focus:ring-2 focus:ring-offset-2 focus:ring-orange-400"
            >
              <Send className="h-4 w-4" />
              <span className="sr-only">Send</span>
            </button>
          </form>
        </div>
      </div>
    </div>
  )
}