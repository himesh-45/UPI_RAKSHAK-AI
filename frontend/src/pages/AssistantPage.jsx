import React, { useState, useRef, useEffect } from 'react';
import {
  Send,
  User,
  ShieldCheck,
  ShieldAlert,
  AlertTriangle,
  PhoneCall,
  ExternalLink,
  HelpCircle,
  Paperclip,
  ClipboardPaste,
  ArrowDown,
  Sparkles,
  Info,
  Lock,
  BookOpen
} from 'lucide-react';
import { useTranslation } from '../i18n/useTranslation';
import VoiceInput from '../components/VoiceInput';
import MarkdownRenderer from '../components/MarkdownRenderer';
import GuardianAvatar from '../components/GuardianAvatar';
import AboutRakshakModal from '../components/AboutRakshakModal';
import PreFilled1930Modal from '../components/PreFilled1930Modal';
import LearnCarouselModal from '../components/LearnCarouselModal';
import VerdictCard from '../components/VerdictCard';
import CheckableStepsCard from '../components/CheckableStepsCard';
import EmergencyPlaybookCard from '../components/EmergencyPlaybookCard';
import CitationCard from '../components/CitationCard';
import SecurityTipCard from '../components/SecurityTipCard';
import FamilyElderMode from '../components/FamilyElderMode';
import { chatAssistant } from '../api/client';

export default function AssistantPage() {
  const { language, setLanguage, t } = useTranslation();

  // Mode: 'help' (Ask a question) vs 'analyze' (Check a message)
  const [mode, setMode] = useState('help');
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [guardianState, setGuardianState] = useState('idle');
  const [showScrollBottom, setShowScrollBottom] = useState(false);
  const [isElderMode, setIsElderMode] = useState(false);

  // Modals
  const [aboutOpen, setAboutOpen] = useState(false);
  const [learnOpen, setLearnOpen] = useState(false);
  const [prefilledModalOpen, setPrefilledModalOpen] = useState(false);
  const [prefilledData, setPrefilledData] = useState(null);

  const messagesEndRef = useRef(null);
  const chatContainerRef = useRef(null);
  const inputRef = useRef(null);
  const fileInputRef = useRef(null);

  // Global Keyboard Shortcuts (Ctrl+K, Escape, Alt+1/2/3)
  useEffect(() => {
    const handleKeyDown = (e) => {
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
        e.preventDefault();
        inputRef.current?.focus();
      }
      if (e.key === 'Escape') {
        setAboutOpen(false);
        setLearnOpen(false);
        setPrefilledModalOpen(false);
      }
      if (e.altKey && e.key === '1') {
        e.preventDefault();
        setLanguage('en');
      } else if (e.altKey && e.key === '2') {
        e.preventDefault();
        setLanguage('hi');
      } else if (e.altKey && e.key === '3') {
        e.preventDefault();
        setLanguage('te');
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [setLanguage]);

  const taglines = {
    en: "Your AI Digital Guardian",
    hi: "आपका एआई डिजिटल रक्षक",
    te: "మీ ఏఐ డిజిటల్ రక్షకుడు"
  };

  const statusLines = {
    en: "Encrypted & masked session • Offline capable",
    hi: "एन्क्रिप्टेड व सुरक्षित सत्र • ऑफलाइन सक्षम",
    te: "ఎన్‌క్రిప్ట్ చేయబడిన సెషన్ • ఆఫ్‌లైన్ సామర్థ్యం"
  };

  const emptyHeaders = {
    en: "I'm Rakshak. How can I help you stay safe today?",
    hi: "मैं रक्षक हूँ। आज मैं आपकी सुरक्षा में कैसे मदद करूँ?",
    te: "నేను రక్షక్. నేడు మీ భద్రతకు ఎలా సహాయపడగలను?"
  };

  const suggestedChips = {
    en: [
      "How to complain to 1930?",
      "I shared my OTP what now?",
      "How to block my UPI ID?",
      "What is digital arrest?",
      "How do collect requests work?"
    ],
    hi: [
      "1930 पर शिकायत कैसे करें?",
      "मैंने OTP शेयर कर दिया अब क्या करूँ?",
      "UPI ID कैसे ब्लॉक करें?",
      "डिजिटल अरेस्ट क्या है?",
      "कलेक्ट रिक्वेस्ट कैसे काम करती है?"
    ],
    te: [
      "1930 కు ఎలా ఫిర్యాదు చేయాలి?",
      "నేను OTP చెప్పేశాను ఇప్పుడు ఏమి చేయాలి?",
      "UPI ID ఎలా బ్లాక్ చేయాలి?",
      "డిజిటల్ అరెస్ట్ అంటే ఏమిటి?",
      "కలెక్ట్ రిక్వెస్ట్ ఎలా పనిచేస్తుంది?"
    ]
  };

  // Scroll to bottom smoothly
  const scrollToBottom = (behavior = 'smooth') => {
    messagesEndRef.current?.scrollIntoView({ behavior });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, loading]);

  // Handle scroll detection for "Scroll to bottom" button
  const handleScroll = () => {
    if (!chatContainerRef.current) return;
    const { scrollTop, scrollHeight, clientHeight } = chatContainerRef.current;
    const isUp = scrollHeight - scrollTop - clientHeight > 180;
    setShowScrollBottom(isUp);
  };

  // Core Send Handler
  const handleSend = async (queryText) => {
    const textToSend = (queryText || input).trim();
    if (!textToSend || loading) return;

    const userMsg = {
      id: `usr_${Date.now()}`,
      sender: 'user',
      text: textToSend,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };

    // Keep context window (last 6 turns)
    const historyPayload = messages.slice(-6).map((m) => ({
      role: m.sender === 'user' ? 'user' : 'assistant',
      content: m.text
    }));

    setMessages((prev) => [...prev, userMsg]);
    setInput('');
    setLoading(true);
    setGuardianState('scanning');

    try {
      const res = await chatAssistant(textToSend, language, historyPayload);

      // Determine reactive avatar state based on outcome
      let nextState = 'idle';
      if (res.verdict === 'HIGH RISK' || res.verdict === 'DANGER' || (res.risk_score && res.risk_score >= 70)) {
        nextState = 'alert';
      } else if (res.verdict === 'SUSPICIOUS' || res.verdict === 'WARNING') {
        nextState = 'alert';
      } else if (res.verdict === 'SAFE') {
        nextState = 'safe';
      } else {
        nextState = 'idle';
      }
      setGuardianState(nextState);

      const assistantMsg = {
        id: `ast_${Date.now()}`,
        sender: 'assistant',
        text: res.reply,
        verdict: res.verdict,
        score: res.risk_score,
        intent: res.intent,
        citations: res.citations || [],
        recommended_actions: res.recommended_actions || [],
        quick_replies: res.quick_replies || [],
        action_buttons: res.action_buttons || [],
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      };

      setMessages((prev) => [...prev, assistantMsg]);
    } catch (err) {
      setGuardianState('idle');
      const errorMsg = {
        id: `err_${Date.now()}`,
        sender: 'assistant',
        text: language === 'hi'
          ? "माफ़ करें, उत्तर प्राप्त करने में समस्या आई। यदि यह कोई आपातकालीन साइबर धोखाधड़ी है, तो तुरंत 1930 डायल करें।"
          : (language === 'te'
            ? "సమాధానం పొందడంలో సమస్య ఎదురైంది. సైబర్ అత్యవసర పరిస్థితి అయితే వెంటనే 1930 కు కాల్ చేయండి."
            : "Sorry, I encountered an issue. If you experienced financial fraud, please dial 1930 immediately or visit https://cybercrime.gov.in."),
        verdict: null,
        score: null,
        citations: [],
        recommended_actions: ["Call 1930 Cyber Helpline", "Visit cybercrime.gov.in"],
        quick_replies: ["Call 1930", "Visit cybercrime.gov.in"],
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      };
      setMessages((prev) => [...prev, errorMsg]);
    } finally {
      setLoading(false);
    }
  };

  // One-Tap Clipboard Paste
  const handlePasteClipboard = async () => {
    try {
      if (navigator.clipboard && navigator.clipboard.readText) {
        const text = await navigator.clipboard.readText();
        if (text) {
          setInput(text);
          setMode('analyze');
          inputRef.current?.focus();
        }
      }
    } catch {
      inputRef.current?.focus();
    }
  };

  // File Upload Attachment Handler
  const handleFileAttach = (e) => {
    const file = e.target.files?.[0];
    if (!file) return;

    if (file.type.startsWith('image/')) {
      setInput(`[Screenshot Attached: ${file.name}] Suspicious QR or transaction payment request.`);
      setMode('analyze');
    } else {
      const reader = new FileReader();
      reader.onload = (event) => {
        const content = event.target?.result;
        if (typeof content === 'string') {
          setInput(content.slice(0, 1500));
          setMode('analyze');
        }
      };
      reader.readAsText(file);
    }
  };

  // Handle Quick Actions
  const handleActionClick = (action) => {
    if (action.action === 'open_url' && action.url) {
      window.open(action.url, '_blank', 'noopener,noreferrer');
    } else if (action.action === 'dial_1930') {
      window.location.href = 'tel:1930';
    } else if (action.action === 'trigger_emergency') {
      handleSend(
        language === 'hi'
          ? "मैंने पैसे खो दिए हैं, तुरंत आपातकालीन मदद चाहिए"
          : (language === 'te'
            ? "నేను డబ్బులు కోల్పోయాను, వెంటనే సహాయం కావాలి"
            : "I lost money to a scammer, trigger emergency steps immediately")
      );
    } else if (action.action === 'prompt_analyze') {
      setMode('analyze');
      inputRef.current?.focus();
    } else if (action.action === 'prompt_help') {
      setMode('help');
      inputRef.current?.focus();
    }
  };

  const handleOpen1930ModalForMessage = (msg) => {
    setPrefilledData({
      text: msg.text,
      verdict: msg.verdict,
      score: msg.score
    });
    setPrefilledModalOpen(true);
  };

  return (
    <div className="flex flex-col h-[calc(100vh-4rem)] max-w-5xl mx-auto w-full px-2 sm:px-4 py-2 font-sans select-none">
      {/* ------------------------------------------------------------- */}
      {/* 1. HEADER BAR                                                 */}
      {/* ------------------------------------------------------------- */}
      <header className="flex items-center justify-between px-3 sm:px-4 py-2.5 bg-slate-900/90 border border-slate-800 rounded-2xl shadow-xl backdrop-blur-md mb-2">
        <div className="flex items-center gap-3">
          <GuardianAvatar
            state={loading ? 'scanning' : guardianState}
            size={42}
            onClick={() => setAboutOpen(true)}
            className="hover:scale-105 transition-transform"
          />
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-sm sm:text-base font-bold text-slate-100 tracking-wide font-sans">
                Rakshak Assistant
              </h1>
              <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-cyan-500/20 text-cyan-300 border border-cyan-500/30">
                PROD
              </span>
            </div>
            <p className="text-[11px] text-cyan-400 font-mono hidden sm:block">
              {taglines[language] || taglines.en} • <span className="text-slate-400">{statusLines[language] || statusLines.en}</span>
            </p>
          </div>
        </div>

        {/* Right Header Actions */}
        <div className="flex items-center gap-1.5 sm:gap-2">
          {/* Secure Session Pill */}
          <button
            onClick={() => setAboutOpen(true)}
            className="hidden md:flex items-center gap-1 px-2.5 py-1 rounded-lg bg-slate-800/80 hover:bg-slate-800 text-[11px] text-slate-300 border border-slate-700/60 transition-colors"
            title="Privacy and data protection details"
          >
            <Lock className="w-3 h-3 text-emerald-400" />
            <span>Secure Session</span>
          </button>

          {/* Learn Red Flags Carousel Shortcut */}
          <button
            onClick={() => setLearnOpen(true)}
            className="flex items-center gap-1 px-2.5 py-1 rounded-lg bg-cyan-950/40 hover:bg-cyan-900/40 text-[11px] text-cyan-300 border border-cyan-500/30 transition-colors font-medium"
          >
            <BookOpen className="w-3.5 h-3.5" />
            <span className="hidden sm:inline">Learn Scams</span>
          </button>

          {/* Language Switcher */}
          <div className="flex items-center bg-slate-800/90 rounded-lg p-0.5 border border-slate-700">
            <button
              onClick={() => setLanguage('en')}
              className={`px-2 py-0.5 text-xs font-semibold rounded ${
                language === 'en' ? 'bg-cyan-500 text-slate-950 shadow-sm' : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              EN
            </button>
            <button
              onClick={() => setLanguage('hi')}
              className={`px-2 py-0.5 text-xs font-semibold rounded ${
                language === 'hi' ? 'bg-cyan-500 text-slate-950 shadow-sm' : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              हिंदी
            </button>
            <button
              onClick={() => setLanguage('te')}
              className={`px-2 py-0.5 text-xs font-semibold rounded ${
                language === 'te' ? 'bg-cyan-500 text-slate-950 shadow-sm' : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              తెలుగు
            </button>
          </div>
        </div>
      </header>

      {/* Elder Mode Accessibility & Read-Aloud Bar */}
      <div className="mb-2">
        <FamilyElderMode
          isElderMode={isElderMode}
          setIsElderMode={setIsElderMode}
          language={language}
          onCheckMessage={() => {
            setMode('analyze');
            inputRef.current?.focus();
          }}
          onEmergency={() =>
            handleSend(
              language === 'hi'
                ? "पैसे कट गए क्या करें?"
                : (language === 'te' ? "డబ్బులు పోయాయి ఏం చేయాలి?" : "I lost money to a scammer")
            )
          }
          onHelp={() =>
            handleSend(
              language === 'hi'
                ? "1930 पर शिकायत कैसे करें?"
                : (language === 'te' ? "1930 కు ఎలా ఫిర్యాదు చేయాలి?" : "How to report to 1930 helpline?")
            )
          }
          activeVerdict={messages.filter(m => m.sender === 'assistant' && m.verdict).slice(-1)[0]?.verdict}
          activeAdvice={messages.filter(m => m.sender === 'assistant' && m.text).slice(-1)[0]?.text?.slice(0, 180)}
        />
      </div>

      {/* ------------------------------------------------------------- */}
      {/* 2. CHAT MESSAGES CONTAINER                                    */}
      {/* ------------------------------------------------------------- */}
      <div
        ref={chatContainerRef}
        onScroll={handleScroll}
        aria-live="polite"
        aria-atomic="false"
        role="log"
        className={`flex-1 overflow-y-auto px-2 sm:px-3 py-3 space-y-4 rounded-2xl bg-slate-950/60 border border-slate-900/80 shadow-inner relative ${
          isElderMode ? 'text-base sm:text-lg font-medium' : ''
        }`}
      >
        {/* EMPTY STATE */}
        {messages.length === 0 && (
          <div className="max-w-xl mx-auto py-6 sm:py-8 flex flex-col items-center text-center animate-fadeIn select-none">
            <GuardianAvatar state="idle" size={96} className="mb-4" />
            <h2 className="text-lg sm:text-xl font-bold text-slate-100 font-sans tracking-wide">
              {emptyHeaders[language] || emptyHeaders.en}
            </h2>
            <p className="text-xs text-slate-400 mt-1.5 max-w-md font-mono">
              Grounded guidance on 1930 reporting, bank freezing, and instant detection of suspicious UPI requests and links.
            </p>

            {/* 4 Starter Action Cards */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 w-full mt-6 text-left">
              <div
                onClick={() => {
                  setMode('analyze');
                  inputRef.current?.focus();
                }}
                className="p-3 bg-slate-900/90 hover:bg-slate-800/90 border border-slate-800 hover:border-cyan-500/40 rounded-xl cursor-pointer transition-all flex items-start gap-3 shadow-md"
              >
                <div className="p-2 rounded-lg bg-cyan-950/50 text-cyan-400 shrink-0">
                  <ShieldCheck className="w-5 h-5" />
                </div>
                <div>
                  <h3 className="text-xs font-bold text-slate-200">Check a message or link</h3>
                  <p className="text-[11px] text-slate-400 mt-0.5">Paste suspicious SMS, UPI ID, or URL</p>
                </div>
              </div>

              <div
                onClick={() =>
                  handleSend(
                    language === 'hi'
                      ? "पैसे कट गए क्या करें?"
                      : (language === 'te' ? "డబ్బులు పోయాయి ఏం చేయాలి?" : "I lost money to a scammer what should I do?")
                  )
                }
                className="p-3 bg-red-950/20 hover:bg-red-950/30 border border-red-500/30 rounded-xl cursor-pointer transition-all flex items-start gap-3 shadow-md"
              >
                <div className="p-2 rounded-lg bg-red-950/60 text-red-400 shrink-0">
                  <PhoneCall className="w-5 h-5" />
                </div>
                <div>
                  <h3 className="text-xs font-bold text-red-200">I lost money (Emergency)</h3>
                  <p className="text-[11px] text-red-300/80 mt-0.5">Golden hour freezing & 1930 steps</p>
                </div>
              </div>

              <div
                onClick={() =>
                  handleSend(
                    language === 'hi'
                      ? "1930 पर शिकायत कैसे करें?"
                      : (language === 'te' ? "1930 కు ఎలా ఫిర్యాదు చేయాలి?" : "How to report to 1930 helpline?")
                  )
                }
                className="p-3 bg-slate-900/90 hover:bg-slate-800/90 border border-slate-800 hover:border-cyan-500/40 rounded-xl cursor-pointer transition-all flex items-start gap-3 shadow-md"
              >
                <div className="p-2 rounded-lg bg-blue-950/50 text-blue-400 shrink-0">
                  <HelpCircle className="w-5 h-5" />
                </div>
                <div>
                  <h3 className="text-xs font-bold text-slate-200">How to report to 1930</h3>
                  <p className="text-[11px] text-slate-400 mt-0.5">Required documents & preparation</p>
                </div>
              </div>

              <div
                onClick={() => setLearnOpen(true)}
                className="p-3 bg-slate-900/90 hover:bg-slate-800/90 border border-slate-800 hover:border-cyan-500/40 rounded-xl cursor-pointer transition-all flex items-start gap-3 shadow-md"
              >
                <div className="p-2 rounded-lg bg-indigo-950/50 text-indigo-400 shrink-0">
                  <BookOpen className="w-5 h-5" />
                </div>
                <div>
                  <h3 className="text-xs font-bold text-slate-200">Learn common UPI scams</h3>
                  <p className="text-[11px] text-slate-400 mt-0.5">5-card interactive red flag carousel</p>
                </div>
              </div>
            </div>

            {/* Rotating Security Tip Card */}
            <div className="w-full mt-4">
              <SecurityTipCard language={language} onOpenLearn={() => setLearnOpen(true)} />
            </div>
          </div>
        )}

        {/* MESSAGE LIST */}
        {messages.map((msg, index) => {
          const isUser = msg.sender === 'user';
          const isEmergency = msg.intent === 'EMERGENCY';
          const isAnalyze = msg.intent === 'ANALYZE' || !!msg.verdict;

          let avatarState = 'idle';
          if (msg.verdict === 'HIGH RISK' || msg.verdict === 'DANGER' || (msg.score && msg.score >= 70)) {
            avatarState = 'alert';
          } else if (msg.verdict === 'SUSPICIOUS' || msg.verdict === 'WARNING') {
            avatarState = 'alert';
          } else if (msg.verdict === 'SAFE') {
            avatarState = 'safe';
          }

          return (
            <div
              key={msg.id || index}
              className={`flex flex-col ${isUser ? 'items-end' : 'items-start'} animate-fadeIn`}
            >
              <div className={`flex items-start gap-2 max-w-[90%] sm:max-w-[80%] ${isUser ? 'flex-row-reverse' : 'flex-row'}`}>
                {/* Avatar Icon */}
                {!isUser ? (
                  <GuardianAvatar state={avatarState} size={32} className="shrink-0 mt-1" />
                ) : (
                  <div className="w-8 h-8 rounded-full bg-slate-800 border border-slate-700 flex items-center justify-center shrink-0 mt-1 text-slate-300">
                    <User className="w-4 h-4" />
                  </div>
                )}

                {/* Message Bubble */}
                <div
                  className={`p-3.5 rounded-2xl text-xs sm:text-sm leading-relaxed shadow-md ${
                    isUser
                      ? 'bg-slate-900 border border-cyan-500/30 text-slate-100 rounded-tr-none'
                      : 'bg-slate-900/90 border border-slate-800 text-slate-200 rounded-tl-none'
                  }`}
                >
                  {/* Clean Markdown Rendering without raw hashes */}
                  <MarkdownRenderer content={msg.text} />

                  {/* C1. Verdict Reveal Card (for ANALYZE intent only) */}
                  {isAnalyze && msg.verdict && (
                    <VerdictCard
                      verdict={msg.verdict}
                      score={msg.score || 0}
                      reasons={msg.recommended_actions || []}
                      category={msg.category || ''}
                      language={language}
                      onOpenReport={() => handleOpen1930ModalForMessage(msg)}
                      onEmergency={() =>
                        handleSend(
                          language === 'hi'
                            ? "पैसे कट गए क्या करें?"
                            : (language === 'te' ? "డబ్బులు పోయాయి ఏం చేయాలి?" : "I lost money to a scammer")
                        )
                      }
                      onShare={() => {
                        if (navigator.share) {
                          navigator.share({
                            title: 'UPI Rakshak Scam Alert',
                            text: `Verified safety notice: ${msg.text.slice(0, 150)}`
                          });
                        }
                      }}
                    />
                  )}

                  {/* C2. Checkable Action Steps Checklist */}
                  {msg.recommended_actions && msg.recommended_actions.length > 0 && !isEmergency && (
                    <CheckableStepsCard
                      steps={msg.recommended_actions}
                      language={language}
                      messageId={msg.id}
                    />
                  )}

                  {/* C3. Emergency Playbook Card */}
                  {isEmergency && (
                    <EmergencyPlaybookCard
                      language={language}
                      onOpen1930Modal={() => handleOpen1930ModalForMessage(msg)}
                    />
                  )}

                  {/* C4. Statutory Citations */}
                  {msg.citations && msg.citations.length > 0 && (
                    <div className="space-y-1.5 mt-2">
                      {msg.citations.map((c, citIdx) => (
                        <CitationCard key={citIdx} citation={c} language={language} />
                      ))}
                    </div>
                  )}

                  {/* Action Buttons */}
                  {msg.action_buttons && msg.action_buttons.length > 0 && (
                    <div className="mt-3 flex flex-wrap gap-2 pt-2 border-t border-slate-800/80">
                      {msg.action_buttons.map((btn, btnIdx) => (
                        <button
                          key={btnIdx}
                          onClick={() => handleActionClick(btn)}
                          className="px-2.5 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-medium border border-slate-700 transition-colors flex items-center gap-1.5"
                        >
                          {btn.label}
                        </button>
                      ))}
                    </div>
                  )}

                  {/* Timestamp */}
                  <div className="mt-2 text-[10px] text-slate-400 font-mono text-right">
                    {msg.timestamp}
                  </div>
                </div>
              </div>

              {/* Quick Reply Chips below assistant message */}
              {!isUser && msg.quick_replies && msg.quick_replies.length > 0 && (
                <div className="mt-2 ml-10 flex flex-wrap gap-1.5">
                  {msg.quick_replies.map((chip, chipIdx) => (
                    <button
                      key={chipIdx}
                      onClick={() => handleSend(chip)}
                      className="px-2.5 py-1 rounded-full bg-slate-900/90 hover:bg-slate-800 text-cyan-300 hover:text-cyan-200 border border-cyan-500/30 text-[11px] font-medium transition-all shadow-sm"
                    >
                      {chip}
                    </button>
                  ))}
                </div>
              )}
            </div>
          );
        })}

        {/* LOADING INDICATOR */}
        {loading && (
          <div className="flex items-center gap-2.5 text-slate-400 animate-fadeIn">
            <GuardianAvatar state="scanning" size={28} />
            <div className="px-3 py-2 rounded-2xl bg-slate-900 border border-slate-800 text-xs font-mono text-cyan-400 flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-cyan-400 animate-ping" />
              <span>Rakshak is analyzing safety guidance...</span>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />

        {/* Floating Scroll to Bottom Button */}
        {showScrollBottom && (
          <button
            onClick={() => scrollToBottom('smooth')}
            className="sticky bottom-2 right-4 ml-auto p-2 rounded-full bg-cyan-500 text-slate-950 shadow-xl hover:bg-cyan-400 transition-all z-10 flex items-center justify-center animate-bounce"
            title="Scroll to bottom"
          >
            <ArrowDown className="w-4 h-4" />
          </button>
        )}
      </div>

      {/* ------------------------------------------------------------- */}
      {/* 3. COMPOSER & SUGGESTED CHIPS                                 */}
      {/* ------------------------------------------------------------- */}
      <footer className="mt-2 space-y-2">
        {/* Horizontal Suggested Questions Chips */}
        <div className="flex items-center gap-1.5 overflow-x-auto no-scrollbar py-1">
          {(suggestedChips[language] || suggestedChips.en).map((chip, i) => (
            <button
              key={i}
              onClick={() => handleSend(chip)}
              className="whitespace-nowrap px-2.5 py-1 rounded-full bg-slate-900/90 hover:bg-slate-800 text-slate-300 hover:text-cyan-300 border border-slate-800 hover:border-cyan-500/40 text-[11px] font-mono transition-all shrink-0"
            >
              {chip}
            </button>
          ))}
        </div>

        {/* Segmented Mode Switcher */}
        <div className="flex items-center justify-between px-1">
          <div className="inline-flex bg-slate-900 rounded-lg p-0.5 border border-slate-800 text-xs">
            <button
              onClick={() => setMode('help')}
              className={`px-3 py-1 rounded-md font-semibold transition-all ${
                mode === 'help' ? 'bg-cyan-500 text-slate-950 shadow-sm' : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              Ask a Question
            </button>
            <button
              onClick={() => setMode('analyze')}
              className={`px-3 py-1 rounded-md font-semibold transition-all ${
                mode === 'analyze' ? 'bg-cyan-500 text-slate-950 shadow-sm' : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              Check a Message
            </button>
          </div>

          {/* Quick Paste Button */}
          <button
            onClick={handlePasteClipboard}
            className="flex items-center gap-1 text-[11px] font-mono text-cyan-400 hover:text-cyan-300 transition-colors"
            title="Paste suspicious text from clipboard"
          >
            <ClipboardPaste className="w-3.5 h-3.5" />
            <span>Paste Message</span>
          </button>
        </div>

        {/* Input Box */}
        <div className="relative flex items-center gap-2 p-1.5 bg-slate-900/95 border border-cyan-500/30 rounded-2xl shadow-xl backdrop-blur-md">
          {/* File Attachment */}
          <input
            type="file"
            ref={fileInputRef}
            onChange={handleFileAttach}
            className="hidden"
            accept="image/*,.txt,.eml"
          />
          <button
            onClick={() => fileInputRef.current?.click()}
            className="p-2 text-slate-400 hover:text-cyan-400 hover:bg-slate-800 rounded-xl transition-colors"
            title="Attach screenshot or message text"
          >
            <Paperclip className="w-4 h-4" />
          </button>

          {/* Text Input */}
          <textarea
            ref={inputRef}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                handleSend();
              }
            }}
            rows={1}
            placeholder={
              mode === 'analyze'
                ? (language === 'hi' ? 'सत्यापन के लिए कोई संदिग्ध संदेश, लिंक या यूपीआई आईडी यहाँ पेस्ट करें...' : 'Paste a suspicious message, link, or UPI ID to scan for fraud...')
                : (language === 'hi' ? 'साइबर सुरक्षा या 1930 रिपोर्टिंग के बारे में कुछ भी पूछें...' : 'Ask how to report to 1930, block UPI, or recover lost funds...')
            }
            className="flex-1 bg-transparent border-0 text-slate-100 text-xs sm:text-sm placeholder-slate-500 focus:outline-none focus:ring-0 resize-none py-1.5 max-h-32"
          />

          {/* Voice Input with Web Speech API */}
          <VoiceInput
            language={language}
            onTranscript={(trans) => {
              setInput((prev) => (prev ? `${prev} ${trans}` : trans));
              setGuardianState('listening');
            }}
          />

          {/* Send Button */}
          <button
            onClick={() => handleSend()}
            disabled={!input.trim() || loading}
            className={`p-2.5 rounded-xl flex items-center justify-center transition-all ${
              input.trim() && !loading
                ? 'bg-cyan-500 hover:bg-cyan-400 text-slate-950 shadow-lg shadow-cyan-500/30'
                : 'bg-slate-800 text-slate-600 cursor-not-allowed'
            }`}
            aria-label="Send message"
          >
            <Send className="w-4 h-4" />
          </button>
        </div>
      </footer>

      {/* ------------------------------------------------------------- */}
      {/* 4. MODALS                                                     */}
      {/* ------------------------------------------------------------- */}
      <AboutRakshakModal
        isOpen={aboutOpen}
        onClose={() => setAboutOpen(false)}
        language={language}
      />

      <LearnCarouselModal
        isOpen={learnOpen}
        onClose={() => setLearnOpen(false)}
        language={language}
      />

      <PreFilled1930Modal
        isOpen={prefilledModalOpen}
        onClose={() => setPrefilledModalOpen(false)}
        prefillData={prefilledData}
      />
    </div>
  );
}
