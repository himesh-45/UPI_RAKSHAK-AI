import React, { useState, useEffect } from 'react';
import { Mic, MicOff, Volume2, Globe } from 'lucide-react';

export default function VoiceInput({ onTranscript, selectedLang = 'en-IN', onLangChange }) {
  const [isListening, setIsListening] = useState(false);
  const [supported, setSupported] = useState(true);
  const [recognition, setRecognition] = useState(null);

  useEffect(() => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      setSupported(false);
      return;
    }

    const recog = new SpeechRecognition();
    recog.continuous = false;
    recog.interimResults = false;
    recog.lang = selectedLang;

    recog.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      if (transcript && onTranscript) {
        onTranscript(transcript);
      }
      setIsListening(false);
    };

    recog.onerror = (event) => {
      console.warn('Speech recognition error:', event.error);
      setIsListening(false);
    };

    recog.onend = () => {
      setIsListening(false);
    };

    setRecognition(recog);
  }, [selectedLang]);

  const toggleListening = () => {
    if (!supported || !recognition) {
      alert('Speech recognition is not supported in this browser. Please type your message.');
      return;
    }

    if (isListening) {
      recognition.stop();
      setIsListening(false);
    } else {
      try {
        recognition.lang = selectedLang;
        recognition.start();
        setIsListening(true);
      } catch (err) {
        console.warn('Failed to start speech recognition:', err);
      }
    }
  };

  return (
    <div className="flex items-center gap-1.5">
      {/* Speech language dropdown */}
      <select
        value={selectedLang}
        onChange={(e) => onLangChange && onLangChange(e.target.value)}
        className="text-[11px] font-semibold bg-navy text-ink border border-border rounded-lg px-2 py-1 focus:border-teal-400 focus:ring-1 focus:ring-teal-400 focus:outline-hidden"
      >
        <option value="en-IN">English (India)</option>
        <option value="hi-IN">हिंदी (India)</option>
        <option value="te-IN">తెలుగు (India)</option>
      </select>

      {/* Mic toggle button */}
      <button
        type="button"
        onClick={toggleListening}
        title={supported ? (isListening ? 'Stop listening' : 'Start voice input') : 'Voice input not supported'}
        className={`p-2 rounded-xl border transition flex items-center justify-center ${
          isListening
            ? 'bg-verdict-danger border-verdict-danger text-white animate-pulse shadow-lg ring-2 ring-verdict-danger/50'
            : 'bg-navy border-border text-ink-muted hover:text-ink hover:border-teal-400/50'
        }`}
      >
        {isListening ? <Mic className="w-4 h-4" /> : <MicOff className="w-4 h-4" />}
      </button>
    </div>
  );
}
