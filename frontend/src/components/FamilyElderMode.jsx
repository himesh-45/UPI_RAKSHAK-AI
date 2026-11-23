import React, { useState, useEffect } from 'react';
import { Volume2, VolumeX, Eye, PhoneCall, ShieldCheck, HelpCircle, CheckCircle2 } from 'lucide-react';

export default function FamilyElderMode({
  isElderMode,
  setIsElderMode,
  language = 'en',
  onCheckMessage = null,
  onEmergency = null,
  onHelp = null,
  activeVerdict = null,
  activeAdvice = null
}) {
  const [isPlaying, setIsPlaying] = useState(false);
  const [speechSupported, setSpeechSupported] = useState(false);

  useEffect(() => {
    if (typeof window !== 'undefined' && 'speechSynthesis' in window) {
      setSpeechSupported(true);
    }
  }, []);

  const speakText = (textToRead) => {
    if (!speechSupported || !textToRead) return;

    if (isPlaying) {
      window.speechSynthesis.cancel();
      setIsPlaying(false);
      return;
    }

    window.speechSynthesis.cancel();

    const utterance = new SpeechSynthesisUtterance(textToRead);
    utterance.rate = 0.85; // Extra slow and distinct for elderly citizens
    utterance.pitch = 1.0;

    if (language === 'hi') {
      utterance.lang = 'hi-IN';
    } else if (language === 'te') {
      utterance.lang = 'te-IN';
    } else {
      utterance.lang = 'en-IN';
    }

    const voices = window.speechSynthesis.getVoices();
    const matching = voices.find((v) => v.lang === utterance.lang || v.lang.startsWith(utterance.lang.slice(0, 2)));
    if (matching) {
      utterance.voice = matching;
    }

    utterance.onend = () => setIsPlaying(false);
    utterance.onerror = () => setIsPlaying(false);

    window.speechSynthesis.speak(utterance);
    setIsPlaying(true);
  };

  // Auto read-aloud when a new verdict is generated in Elder Mode
  useEffect(() => {
    if (isElderMode && activeVerdict) {
      const readout = language === 'hi'
        ? `सावधान: परिणाम है ${activeVerdict}. ${activeAdvice || 'कोई भी पिन दर्ज न करें।'}`
        : (language === 'te'
          ? `హెచ్చరిక: విశ్లేషణ ఫలితం ${activeVerdict}. ${activeAdvice || 'పిన్ ఎంటర్ చేయవద్దు.'}`
          : `Warning: Verdict is ${activeVerdict}. ${activeAdvice || 'Never enter your UPI PIN.'}`);
      speakText(readout);
    }
  }, [activeVerdict, isElderMode]);

  useEffect(() => {
    return () => {
      if (typeof window !== 'undefined' && 'speechSynthesis' in window) {
        window.speechSynthesis.cancel();
      }
    };
  }, []);

  const labels = {
    en: {
      toggle: "Elder Mode",
      btn1: "Check a Message",
      btn2: "Call 1930 Helpline",
      btn3: "Is This Safe?",
      listen: "Read Aloud",
      stop: "Stop Voice",
      sub: "Simplified high-contrast view for elders"
    },
    hi: {
      toggle: "बुजुर्ग मोड (Elder Mode)",
      btn1: "संदेश की जांच करें",
      btn2: "1930 पर तुरंत कॉल करें",
      btn3: "क्या यह सुरक्षित है?",
      listen: "आवाज़ में सुनें",
      stop: "आवाज़ रोकें",
      sub: "बुजुर्गों के लिए सरल और बड़ा डिस्प्ले"
    },
    te: {
      toggle: "ఎల్డర్ మోడ్ (Elder Mode)",
      btn1: "మెసేజ్ తనిఖీ చేయండి",
      btn2: "1930 కు కాల్ చేయండి",
      btn3: "ఇది సురక్షితమేనా?",
      listen: "వాయిస్ వినండి",
      stop: "ఆపండి",
      sub: "పెద్దవారి కోసం సరళమైన డిస్ప్లే"
    }
  };

  const l = labels[language] || labels.en;

  return (
    <div className="w-full select-none">
      {/* Top Elder Mode Bar */}
      <div className="flex items-center justify-between p-2 rounded-xl bg-slate-900 border border-amber-500/30">
        <div className="flex items-center gap-2">
          <button
            onClick={() => setIsElderMode(!isElderMode)}
            className={`flex items-center gap-2 px-3 py-1.5 rounded-lg text-xs font-bold transition-all min-h-[44px] ${
              isElderMode
                ? 'bg-amber-400 text-slate-950 shadow-md font-mono'
                : 'bg-slate-800 text-slate-300 hover:bg-slate-700'
            }`}
          >
            <Eye className="w-4 h-4" />
            <span>{l.toggle}: {isElderMode ? 'ON' : 'OFF'}</span>
          </button>
          <span className="text-[11px] text-slate-400 hidden sm:inline">{l.sub}</span>
        </div>

        {speechSupported && (
          <button
            onClick={() => speakText(activeAdvice || (language === 'hi' ? "नमस्ते। मैं रक्षक हूँ। मदद के लिए 1930 डायल करें।" : "Hello. I am Rakshak. Dial 1930 for cyber fraud help."))}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-bold border transition-all min-h-[44px] ${
              isPlaying
                ? 'bg-rose-500 text-white border-rose-400 animate-pulse'
                : 'bg-slate-800 text-amber-300 border-amber-500/40 hover:bg-slate-700'
            }`}
          >
            {isPlaying ? <VolumeX className="w-4 h-4" /> : <Volume2 className="w-4 h-4" />}
            <span>{isPlaying ? l.stop : l.listen}</span>
          </button>
        )}
      </div>

      {/* Simplified 3-Button Elder Home Grid (Active when Elder Mode is ON) */}
      {isElderMode && (
        <div className="mt-3 p-3 bg-amber-950/20 border-2 border-amber-400 rounded-2xl animate-fadeIn space-y-3">
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-2.5">
            {/* Big Action 1: Check Message */}
            <button
              onClick={onCheckMessage}
              className="p-3.5 rounded-xl bg-slate-900 border-2 border-cyan-400 text-slate-100 font-bold text-sm sm:text-base flex items-center justify-center gap-2 hover:bg-slate-800 transition-all min-h-[48px] shadow-lg shadow-cyan-950/40"
            >
              <ShieldCheck className="w-5 h-5 text-cyan-400 shrink-0" />
              <span>{l.btn1}</span>
            </button>

            {/* Big Action 2: Call 1930 */}
            <a
              href="tel:1930"
              className="p-3.5 rounded-xl bg-red-600 hover:bg-red-500 text-white font-bold text-sm sm:text-base flex items-center justify-center gap-2 transition-all min-h-[48px] shadow-lg shadow-red-950/50"
            >
              <PhoneCall className="w-5 h-5 shrink-0" />
              <span>{l.btn2}</span>
            </a>

            {/* Big Action 3: Is This Safe */}
            <button
              onClick={onHelp}
              className="p-3.5 rounded-xl bg-slate-900 border-2 border-amber-400 text-slate-100 font-bold text-sm sm:text-base flex items-center justify-center gap-2 hover:bg-slate-800 transition-all min-h-[48px] shadow-lg shadow-amber-950/40"
            >
              <HelpCircle className="w-5 h-5 text-amber-400 shrink-0" />
              <span>{l.btn3}</span>
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
