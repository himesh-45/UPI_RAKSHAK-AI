import React, { useState, useEffect } from 'react';
import { Volume2, VolumeX, Eye, UserCheck, Play, Square } from 'lucide-react';

export default function FamilyElderMode({
  explanationText,
  language = 'en',
  isElderMode,
  setIsElderMode
}) {
  const [isPlaying, setIsPlaying] = useState(false);
  const [speechSupported, setSpeechSupported] = useState(false);

  useEffect(() => {
    if (typeof window !== 'undefined' && 'speechSynthesis' in window) {
      setSpeechSupported(true);
    }
  }, []);

  const handleSpeak = () => {
    if (!speechSupported || !explanationText) return;

    if (isPlaying) {
      window.speechSynthesis.cancel();
      setIsPlaying(false);
      return;
    }

    window.speechSynthesis.cancel(); // Stop any pending speech

    const utterance = new SpeechSynthesisUtterance(explanationText);
    utterance.rate = 0.9; // Slightly slower for clarity
    utterance.pitch = 1.0;

    // Set voice language code
    if (language === 'hi') {
      utterance.lang = 'hi-IN';
    } else if (language === 'te') {
      utterance.lang = 'te-IN';
    } else {
      utterance.lang = 'en-IN';
    }

    // Try finding matched system voice if available
    const voices = window.speechSynthesis.getVoices();
    const matchingVoice = voices.find((v) => v.lang === utterance.lang || v.lang.startsWith(utterance.lang.slice(0, 2)));
    if (matchingVoice) {
      utterance.voice = matchingVoice;
    }

    utterance.onend = () => setIsPlaying(false);
    utterance.onerror = () => setIsPlaying(false);

    window.speechSynthesis.speak(utterance);
    setIsPlaying(true);
  };

  useEffect(() => {
    return () => {
      if (typeof window !== 'undefined' && 'speechSynthesis' in window) {
        window.speechSynthesis.cancel();
      }
    };
  }, []);

  return (
    <div className="flex items-center gap-2 flex-wrap">
      {/* Elder Mode Toggle */}
      <button
        onClick={() => setIsElderMode(!isElderMode)}
        className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold border transition-all ${
          isElderMode
            ? 'bg-amber-500/20 text-amber-300 border-amber-500/40 shadow-sm'
            : 'bg-slate-800/80 text-slate-400 border-slate-700 hover:text-slate-200'
        }`}
        title="Toggle High-Contrast Large Text Mode for Elders"
      >
        <Eye className="w-3.5 h-3.5" />
        <span>Elder Mode {isElderMode ? 'ON' : 'OFF'}</span>
      </button>

      {/* Audio Readout Button */}
      {speechSupported && explanationText && (
        <button
          onClick={handleSpeak}
          className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold border transition-all ${
            isPlaying
              ? 'bg-rose-500/20 text-rose-300 border-rose-500/40 animate-pulse'
              : 'bg-indigo-600/20 text-indigo-300 border-indigo-500/30 hover:bg-indigo-600/30'
          }`}
          title="Read Plain Language Verdict Out Loud"
        >
          {isPlaying ? <Square className="w-3.5 h-3.5 fill-current" /> : <Volume2 className="w-3.5 h-3.5" />}
          <span>{isPlaying ? 'Stop Voice' : 'Listen Verdict'}</span>
        </button>
      )}
    </div>
  );
}
