import { useState, useEffect, createContext, useContext } from 'react';
import en from './en.json';
import hi from './hi.json';
import te from './te.json';

const dictionaries = { en, hi, te };

const TranslationContext = createContext();

export function TranslationProvider({ children }) {
  const [language, setLanguageState] = useState(() => {
    return localStorage.getItem('upi_rakshak_lang') || 'en';
  });

  const setLanguage = (lang) => {
    if (dictionaries[lang]) {
      setLanguageState(lang);
      localStorage.setItem('upi_rakshak_lang', lang);
    }
  };

  const t = (path) => {
    const keys = path.split('.');
    let current = dictionaries[language] || dictionaries.en;
    for (const key of keys) {
      if (current && current[key] !== undefined) {
        current = current[key];
      } else {
        // Fallback to English
        let fallback = dictionaries.en;
        for (const fbKey of keys) {
          if (fallback && fallback[fbKey] !== undefined) {
            fallback = fallback[fbKey];
          } else {
            return path;
          }
        }
        return fallback;
      }
    }
    return current;
  };

  return (
    <TranslationContext.Provider value={{ language, setLanguage, t }}>
      {children}
    </TranslationContext.Provider>
  );
}

export function useTranslation() {
  const ctx = useContext(TranslationContext);
  if (!ctx) {
    throw new Error('useTranslation must be used within a TranslationProvider');
  }
  return ctx;
}
