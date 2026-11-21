import React, { useState, useRef, useEffect } from 'react';
import { Send, Bot, User, Sparkles, AlertCircle, PhoneCall, ShieldAlert } from 'lucide-react';
import { useTranslation } from '../i18n/useTranslation';
import VoiceInput from '../components/VoiceInput';
import { chatAssistant } from '../api/client';

export default function AssistantPage() {
  const { language, setLanguage, t } = useTranslation();
  const [messages, setMessages] = useState([
    {
      sender: 'assistant',
      text: language === 'hi'
        ? "नमस्ते! मैं यूपीआई रक्षक सुरक्षा सहायक हूँ। आप मुझसे किसी भी संदिग्ध एसएमएस, लिंक, क्यूआर कोड या कॉल के बारे में हिंदी, अंग्रेजी या तेलुगु में पूछ सकते हैं।"
        : (language === 'te'
          ? "నమస్కారం! నేను యూపీఐ రక్షక్ ఏఐ సహాయకుడిని. మీకు వచ్చిన ఏదైనా అనుమానాస్పద సందేశం, ఫోన్ కాల్ లేదా లింక్ గురించి నన్ను తెలుగు, ఇంగ్లీష్ లేదా హిందీలో అడగండి."
          : "Hello! I am UPI Rakshak Safety Assistant. Paste any suspicious payment message, link, or question in English, Hindi, or Telugu to verify safety."),
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async (queryText) => {
    const textToSend = queryText || input;
    if (!textToSend.trim()) return;

    const userMsg = {
      sender: 'user',
      text: textToSend,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };

    setMessages((prev) => [...prev, userMsg]);
    setInput('');
    setLoading(true);

    try {
      const res = await chatAssistant(textToSend, language);
      const assistantMsg = {
        sender: 'assistant',
        text: res.reply,
        verdict: res.verdict,
        score: res.risk_score,
        citations: res.citations,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      };
      setMessages((prev) => [...prev, assistantMsg]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        {
          sender: 'assistant',
          text: `⚠️ Request failed: ${err.message || 'Please check your connection.'}`,
          timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        }
      ]);
    } finally {
      setLoading(false);
    }
  };

  const samplePrompts = [
    { label: "Telugu KYC check", text: "నాకు ఈ మెసేజ్ వచ్చింది. ఇది నిజమా? మీ SBI ఖాతా కేవైసీ పెండింగ్ ఉన్నందున ఈ రాత్రి బ్లాక్ చేయబడుతుంది. వెంటనే లింక్ క్లిక్ చేయండి." },
    { label: "Hindi Bijli Cut check", text: "मेरा बिजली बिल नहीं भरा है, आज रात 9:30 बजे बिजली कट जाएगी। क्या यह असली है?" },
    { label: "Cashback Collect check", text: "Someone sent a Google Pay collect request for Rs 2999 cashback. Should I enter my UPI PIN?" },
    { label: "AnyDesk download check", text: "Customer care asked me to install AnyDesk app to process my failed transaction refund." }
  ];

  return (
    <div className="max-w-4xl mx-auto px-4 py-8 space-y-6 animate-fade-in">
      
      {/* Title */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-slate-200 dark:border-slate-800">
        <div>
          <h1 className="text-2xl font-extrabold text-slate-900 dark:text-white flex items-center gap-2">
            <Bot className="w-6 h-6 text-indigo-600 dark:text-indigo-400" />
            {t('assistant.title')}
          </h1>
          <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">
            {t('assistant.subtitle')}
          </p>
        </div>

        {/* 1930 quick badge */}
        <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-xl bg-rose-50 dark:bg-rose-950/40 text-rose-700 dark:text-rose-300 border border-rose-200 dark:border-rose-800 text-xs font-bold">
          <PhoneCall className="w-3.5 h-3.5" />
          <span>Helpline: 1930</span>
        </div>
      </div>

      {/* Chat Messages Container */}
      <div className="h-[480px] bg-slate-50/70 dark:bg-slate-900/40 rounded-3xl border border-slate-200 dark:border-slate-800 p-4 sm:p-6 overflow-y-auto space-y-4">
        {messages.map((m, idx) => {
          const isUser = m.sender === 'user';
          return (
            <div
              key={idx}
              className={`flex gap-3 max-w-[85%] sm:max-w-[80%] ${isUser ? 'ml-auto flex-row-reverse' : 'mr-auto'}`}
            >
              {/* Avatar */}
              <div
                className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 ${
                  isUser
                    ? 'bg-indigo-600 text-white'
                    : 'bg-white dark:bg-slate-800 text-indigo-600 dark:text-indigo-400 border border-slate-200 dark:border-slate-700 shadow-xs'
                }`}
              >
                {isUser ? <User className="w-4 h-4" /> : <Bot className="w-4 h-4" />}
              </div>

              {/* Message Bubble */}
              <div
                className={`p-4 rounded-2xl text-xs sm:text-sm leading-relaxed whitespace-pre-line shadow-xs ${
                  isUser
                    ? 'bg-indigo-600 text-white rounded-tr-none'
                    : 'bg-white dark:bg-slate-900 text-slate-800 dark:text-slate-100 border border-slate-200 dark:border-slate-800 rounded-tl-none'
                }`}
              >
                {m.text}

                {/* Optional verdict pill if returned */}
                {m.verdict && (
                  <div className="mt-3 pt-3 border-t border-slate-100 dark:border-slate-800 flex items-center gap-2">
                    <span
                      className={`px-2 py-0.5 rounded text-[10px] font-bold tracking-wider uppercase ${
                        m.verdict === 'HIGH RISK'
                          ? 'bg-rose-100 text-rose-800 dark:bg-rose-950 dark:text-rose-300'
                          : m.verdict === 'SUSPICIOUS'
                          ? 'bg-amber-100 text-amber-800 dark:bg-amber-950 dark:text-amber-300'
                          : 'bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300'
                      }`}
                    >
                      {m.verdict} ({m.score}/100)
                    </span>
                  </div>
                )}

                <div className={`text-[10px] mt-1.5 text-right ${isUser ? 'text-indigo-200' : 'text-slate-400'}`}>
                  {m.timestamp}
                </div>
              </div>
            </div>
          );
        })}

        {loading && (
          <div className="flex gap-3 mr-auto max-w-[80%]">
            <div className="w-8 h-8 rounded-full bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 flex items-center justify-center text-indigo-600">
              <Bot className="w-4 h-4" />
            </div>
            <div className="p-4 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 text-xs text-slate-500 flex items-center gap-2">
              <div className="w-2 h-2 rounded-full bg-indigo-600 animate-ping" />
              <span>Analyzing threat evidence in {language.toUpperCase()}...</span>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Quick Prompts Bar */}
      <div className="flex items-center gap-2 overflow-x-auto pb-1 scrollbar-none">
        {samplePrompts.map((p, i) => (
          <button
            key={i}
            onClick={() => handleSend(p.text)}
            className="px-3 py-1.5 rounded-full text-xs font-semibold whitespace-nowrap bg-slate-100 dark:bg-slate-800 hover:bg-indigo-50 dark:hover:bg-indigo-950 hover:text-indigo-600 dark:hover:text-indigo-400 text-slate-600 dark:text-slate-300 border border-slate-200 dark:border-slate-700 transition"
          >
            {p.label}
          </button>
        ))}
      </div>

      {/* Input Form with Voice Button */}
      <form
        onSubmit={(e) => {
          e.preventDefault();
          handleSend();
        }}
        className="flex items-center gap-2 p-2 bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-md"
      >
        <VoiceInput
          onTranscript={(txt) => setInput((prev) => (prev ? prev + ' ' + txt : txt))}
          selectedLang={language === 'hi' ? 'hi-IN' : (language === 'te' ? 'te-IN' : 'en-IN')}
        />

        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder={t('assistant.placeholder')}
          className="flex-1 px-3 py-2 text-xs sm:text-sm bg-transparent text-slate-900 dark:text-white placeholder:text-slate-400 focus:outline-hidden"
        />

        <button
          type="submit"
          disabled={loading || !input.trim()}
          className="p-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white disabled:opacity-40 transition shadow-sm"
        >
          <Send className="w-4 h-4" />
        </button>
      </form>
    </div>
  );
}
