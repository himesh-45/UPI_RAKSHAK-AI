import React, { useState, useRef, useEffect } from 'react';
import { Send, Bot, User, Sparkles, AlertCircle, PhoneCall, ShieldAlert, ArrowRight, ExternalLink, HelpCircle, ShieldCheck } from 'lucide-react';
import { useTranslation } from '../i18n/useTranslation';
import VoiceInput from '../components/VoiceInput';
import MarkdownRenderer from '../components/MarkdownRenderer';
import { chatAssistant } from '../api/client';

export default function AssistantPage() {
  const { language, t } = useTranslation();
  const [messages, setMessages] = useState([
    {
      sender: 'assistant',
      text: language === 'hi'
        ? "**नमस्ते! मैं यूपीआई रक्षक सुरक्षा सहायक हूँ।**\n\nआप मुझसे किसी भी संदिग्ध एसएमएस, लिंक, क्यूआर कोड, या साइबर शिकायत दर्ज करने के नियमों (जैसे 1930 पर रिपोर्ट) के बारे में हिंदी, अंग्रेजी या तेलुगु में पूछ सकते हैं।"
        : (language === 'te'
          ? "**నమస్కారం! నేను యూపీఐ రక్షక్ ఏఐ సహాయకుడిని.**\n\nమీకు వచ్చిన ఏదైనా అనుమానాస్పద సందేశం, ఫోన్ కాల్, లింక్ లేదా 1930 కు ఫిర్యాదు చేయడం గురించి నన్ను తెలుగు, ఇంగ్లీష్ లేదా హిందీలో అడగండి."
          : "**Hello! I am UPI Rakshak Safety Assistant.**\n\nAsk me how to report to the 1930 helpline, what to do if you lost money, or paste any suspicious message/link to check for fraud in English, Hindi, or Telugu."),
      quick_replies: language === 'hi'
        ? ["1930 पर शिकायत कैसे करें?", "पैसे कट गए क्या करें?", "संदिग्ध मैसेज चेक करें"]
        : (language === 'te'
          ? ["1930 కు ఎలా ఫిర్యాదు చేయాలి?", "డబ్బులు పోయాయి ఏం చేయాలి?", "అనుమానాస్పద మెసేజ్ చూడండి"]
          : ["How to complain to 1930?", "I lost money what now?", "What is digital arrest?"]),
      action_buttons: [
        { label: "💡 How-To Guides", action: "prompt_help" },
        { label: "🚨 Emergency Steps", action: "trigger_emergency" }
      ],
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const inputRef = useRef(null);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, loading]);

  const handleSend = async (queryText) => {
    const textToSend = (queryText || input).trim();
    if (!textToSend) return;

    const userMsg = {
      sender: 'user',
      text: textToSend,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };

    // Prepare small conversation context (last 4 messages) for follow-up resolution
    const historyPayload = messages.slice(-4).map(m => ({
      role: m.sender === 'user' ? 'user' : 'assistant',
      content: m.text
    }));

    setMessages((prev) => [...prev, userMsg]);
    setInput('');
    setLoading(true);

    try {
      const res = await chatAssistant(textToSend, language, historyPayload);
      const assistantMsg = {
        sender: 'assistant',
        text: res.reply,
        verdict: res.verdict,       // null for HOW_TO, SMALL_TALK, EMERGENCY, UNCLEAR
        score: res.risk_score,      // null for non-ANALYZE
        intent: res.intent,
        citations: res.citations || [],
        quick_replies: res.quick_replies || [],
        action_buttons: res.action_buttons || [],
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

  const handleActionButton = (btn) => {
    if (btn.url) {
      window.open(btn.url, '_blank', 'noopener,noreferrer');
      return;
    }
    if (btn.action === 'dial_1930') {
      window.open('tel:1930', '_self');
      return;
    }
    if (btn.action === 'trigger_emergency') {
      handleSend("I lost money in a scam what should I do");
      return;
    }
    if (btn.action === 'prompt_help') {
      handleSend("How to complain to 1930 and cybercrime portal");
      return;
    }
    if (btn.action === 'prompt_analyze') {
      inputRef.current?.focus();
      setInput("Check this message: ");
      return;
    }
    if (btn.action === 'report_scam') {
      window.location.href = '/#report';
      return;
    }
  };

  const samplePrompts = [
    { label: "1930 Complaint Steps", text: "how to complain to 1930" },
    { label: "Money Lost Emergency", text: "I lost 5000 rupees to a scammer just now" },
    { label: "What is Digital Arrest?", text: "what is digital arrest" },
    { label: "How to Block UPI ID", text: "how to block my upi id" },
    { label: "Telugu: 1930 ఫిర్యాదు", text: "1930 lo complaint ela ivvali" },
    { label: "Hindi: बिजली कट SMS", text: "मेरा बिजली बिल नहीं भरा है, आज रात 9:30 बजे बिजली कट जाएगी। क्या यह असली है?" }
  ];

  return (
    <div className="max-w-4xl mx-auto px-4 py-8 space-y-6 animate-fade-in">
      
      {/* Top Banner & Title */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-slate-200 dark:border-slate-800">
        <div>
          <h1 className="text-2xl font-extrabold text-slate-900 dark:text-white flex items-center gap-2">
            <Bot className="w-6 h-6 text-indigo-600 dark:text-indigo-400" />
            {t('assistant.title')}
          </h1>
          <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">
            Intent-routed cybercrime helper & evidence-based threat scanner in English, Hindi, and Telugu.
          </p>
        </div>

        {/* 1930 Quick Dial Badge */}
        <a
          href="tel:1930"
          className="inline-flex items-center gap-2 px-3 py-1.5 rounded-xl bg-rose-50 dark:bg-rose-950/40 text-rose-700 dark:text-rose-300 border border-rose-200 dark:border-rose-800 text-xs font-bold hover:scale-105 transition"
        >
          <PhoneCall className="w-3.5 h-3.5 text-rose-500 animate-pulse" />
          <span>Emergency Helpline: 1930</span>
        </a>
      </div>

      {/* Chat Messages Container */}
      <div className="h-[520px] bg-slate-50/70 dark:bg-slate-900/40 rounded-3xl border border-slate-200 dark:border-slate-800 p-4 sm:p-6 overflow-y-auto space-y-4">
        {messages.map((m, idx) => {
          const isUser = m.sender === 'user';
          return (
            <div
              key={idx}
              className={`flex gap-3 max-w-[90%] sm:max-w-[85%] ${isUser ? 'ml-auto flex-row-reverse' : 'mr-auto'}`}
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
                className={`p-4 sm:p-5 rounded-2xl text-xs sm:text-sm leading-relaxed shadow-xs space-y-3 ${
                  isUser
                    ? 'bg-indigo-600 text-white rounded-tr-none'
                    : 'bg-white dark:bg-slate-900 text-slate-800 dark:text-slate-100 border border-slate-200 dark:border-slate-800 rounded-tl-none'
                }`}
              >
                {/* Clean markdown typography */}
                {isUser ? (
                  <p className="whitespace-pre-wrap">{m.text}</p>
                ) : (
                  <MarkdownRenderer content={m.text} />
                )}

                {/* Verdict Pill: Only for ANALYZE intent with a real verdict */}
                {m.verdict && (
                  <div className="pt-2 border-t border-slate-100 dark:border-slate-800 flex items-center gap-2">
                    <span
                      className={`px-2.5 py-0.5 rounded-full text-[10px] font-extrabold tracking-wider uppercase ${
                        m.verdict === 'HIGH RISK'
                          ? 'bg-rose-100 text-rose-800 dark:bg-rose-950 dark:text-rose-300 border border-rose-300 dark:border-rose-800'
                          : m.verdict === 'SUSPICIOUS'
                          ? 'bg-amber-100 text-amber-800 dark:bg-amber-950 dark:text-amber-300 border border-amber-300 dark:border-amber-800'
                          : 'bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300 border border-emerald-300 dark:border-emerald-800'
                      }`}
                    >
                      {m.verdict} ({m.score}/100)
                    </span>
                    <span className="text-[10px] text-slate-400">Deterministic Threat Fusion</span>
                  </div>
                )}

                {/* Optional Action Buttons (Report, Emergency, Check Message, Portal) */}
                {m.action_buttons && m.action_buttons.length > 0 && !isUser && (
                  <div className="flex flex-wrap items-center gap-2 pt-1">
                    {m.action_buttons.map((btn, bIdx) => (
                      <button
                        key={bIdx}
                        onClick={() => handleActionButton(btn)}
                        className="px-3 py-1 rounded-xl text-[11px] font-bold bg-slate-100 dark:bg-slate-800 hover:bg-indigo-50 dark:hover:bg-indigo-950 text-slate-700 dark:text-slate-300 hover:text-indigo-600 dark:hover:text-indigo-400 border border-slate-200 dark:border-slate-700 transition flex items-center gap-1 active:scale-95"
                      >
                        <span>{btn.label}</span>
                        {btn.url && <ExternalLink className="w-3 h-3 opacity-60" />}
                      </button>
                    ))}
                  </div>
                )}

                {/* Quick-Reply Chips for Immediate Follow-Up */}
                {m.quick_replies && m.quick_replies.length > 0 && idx === messages.length - 1 && !isUser && (
                  <div className="pt-2 border-t border-slate-100 dark:border-slate-800/80 space-y-1.5">
                    <span className="text-[10px] font-bold uppercase tracking-wider text-slate-400 block">
                      Suggested Follow-Ups:
                    </span>
                    <div className="flex flex-wrap gap-1.5">
                      {m.quick_replies.map((chip, cIdx) => (
                        <button
                          key={cIdx}
                          onClick={() => handleSend(chip)}
                          className="px-2.5 py-1 rounded-full text-[11px] font-medium bg-indigo-50 dark:bg-indigo-950/60 hover:bg-indigo-100 dark:hover:bg-indigo-900 text-indigo-700 dark:text-indigo-300 border border-indigo-200 dark:border-indigo-800 transition"
                        >
                          {chip} →
                        </button>
                      ))}
                    </div>
                  </div>
                )}

                <div className={`text-[10px] text-right ${isUser ? 'text-indigo-200' : 'text-slate-400'}`}>
                  {m.timestamp}
                </div>
              </div>
            </div>
          );
        })}

        {loading && (
          <div className="flex gap-3 mr-auto max-w-[85%]">
            <div className="w-8 h-8 rounded-full bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 flex items-center justify-center text-indigo-600">
              <Bot className="w-4 h-4" />
            </div>
            <div className="p-4 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 text-xs text-slate-500 flex items-center gap-2">
              <div className="w-2 h-2 rounded-full bg-indigo-600 animate-ping" />
              <span>Routing intent and retrieving verified safety guidance...</span>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Sample Question Chips Bar */}
      <div className="flex items-center gap-2 overflow-x-auto pb-1 scrollbar-none">
        <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider shrink-0 mr-1">
          Try asking:
        </span>
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
          ref={inputRef}
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder={t('assistant.placeholder') || "Ask how to report to 1930, what is digital arrest, or paste a message..."}
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
