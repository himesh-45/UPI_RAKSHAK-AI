import React, { useState, useEffect } from 'react';
import {
  ShieldAlert, ShieldCheck, AlertTriangle, Link as LinkIcon,
  MessageSquare, Image as ImageIcon, Upload, Check, Copy,
  Share2, Sparkles, BookOpen, ExternalLink, Flag, Info
} from 'lucide-react';
import { useTranslation } from '../i18n/useTranslation';
import ScoreGauge from '../components/ScoreGauge';
import EvidenceList from '../components/EvidenceList';
import ActionBox from '../components/ActionBox';
import ReportModal from '../components/ReportModal';
import VoiceInput from '../components/VoiceInput';
import { analyzeText, analyzeUrl, analyzeImage } from '../api/client';

export default function AnalyzerPage() {
  const { language, t } = useTranslation();
  const [activeInputTab, setActiveInputTab] = useState('text'); // 'text', 'url', 'image'
  const [textInput, setTextInput] = useState('');
  const [urlInput, setUrlInput] = useState('');
  const [selectedFile, setSelectedFile] = useState(null);
  const [filePreview, setFilePreview] = useState(null);
  const [saveHistory, setSaveHistory] = useState(true);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [report, setReport] = useState(null);
  const [copied, setCopied] = useState(false);
  const [demoExamples, setDemoExamples] = useState([]);
  const [reportModalOpen, setReportModalOpen] = useState(false);

  // Load demo examples from public JSON
  useEffect(() => {
    fetch('/demo_assets/demo_examples.json')
      .then((res) => res.json())
      .then((data) => setDemoExamples(data))
      .catch((err) => console.warn('Could not load demo examples:', err));
  }, []);

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setSelectedFile(file);
      setFilePreview(URL.createObjectURL(file));
      setError('');
    }
  };

  const handleApplyChip = async (chip) => {
    setError('');
    if (chip.type === 'text') {
      setActiveInputTab('text');
      setTextInput(chip.input);
    } else if (chip.type === 'url') {
      setActiveInputTab('url');
      setUrlInput(chip.input);
    } else if (chip.type === 'image') {
      setActiveInputTab('image');
      try {
        const response = await fetch(`/${chip.input}`);
        const blob = await response.blob();
        const file = new File([blob], chip.image_filename, { type: 'image/png' });
        setSelectedFile(file);
        setFilePreview(URL.createObjectURL(file));
      } catch (e) {
        console.warn('Failed to load chip image:', e);
      }
    }
  };

  const handleAnalyze = async () => {
    setLoading(true);
    setError('');
    setReport(null);

    try {
      let result;
      if (activeInputTab === 'text') {
        if (!textInput.trim()) throw new Error('Please enter a message or SMS to analyze.');
        result = await analyzeText(textInput, language, saveHistory);
      } else if (activeInputTab === 'url') {
        if (!urlInput.trim()) throw new Error('Please enter a URL to inspect.');
        result = await analyzeUrl(urlInput, saveHistory);
      } else if (activeInputTab === 'image') {
        if (!selectedFile) throw new Error('Please upload an image screenshot or QR code.');
        const formData = new FormData();
        formData.append('file', selectedFile);
        formData.append('save_history', saveHistory);
        formData.append('language', language);
        result = await analyzeImage(formData);
      }
      setReport(result);
    } catch (err) {
      setError(err.message || 'Analysis failed. Please check inputs.');
    } finally {
      setLoading(false);
    }
  };

  const handleCopySummary = () => {
    if (!report) return;
    const text = `[UPI Rakshak AI Safety Report]\nVerdict: ${report.verdict} (Score: ${report.risk_score}/100)\nCategory: ${report.detected_category}\nExplanation: ${report.plain_language_explanation}\nEmergency Helpline: Dial 1930 / cybercrime.gov.in`;
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="max-w-5xl mx-auto px-4 py-8 space-y-8 animate-fade-in">
      
      {/* Hero Header */}
      <div className="text-center space-y-3">
        <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold bg-indigo-50 dark:bg-indigo-950/60 text-indigo-700 dark:text-indigo-300 border border-indigo-200 dark:border-indigo-800">
          <Sparkles className="w-3.5 h-3.5" />
          <span>{t('hero.badge')}</span>
        </div>
        <h1 className="text-3xl sm:text-4xl font-extrabold tracking-tight text-slate-900 dark:text-white">
          {t('hero.title')}
        </h1>
        <p className="text-sm sm:text-base text-slate-600 dark:text-slate-400 max-w-2xl mx-auto">
          {t('hero.subtitle')}
        </p>
      </div>

      {/* Input Workspace Card */}
      <div className="bg-white dark:bg-slate-900 rounded-3xl border border-slate-200 dark:border-slate-800 shadow-xl shadow-slate-100 dark:shadow-none p-6 sm:p-8 space-y-6">
        
        {/* Workspace Mode Tabs */}
        <div className="flex items-center gap-2 border-b border-slate-200 dark:border-slate-800 pb-4">
          <button
            onClick={() => setActiveInputTab('text')}
            className={`px-4 py-2 rounded-xl text-xs font-bold flex items-center gap-2 transition ${
              activeInputTab === 'text'
                ? 'bg-indigo-600 text-white shadow-md shadow-indigo-500/20'
                : 'bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 hover:bg-slate-200 dark:hover:bg-slate-700'
            }`}
          >
            <MessageSquare className="w-4 h-4" />
            {t('tabs.text')}
          </button>

          <button
            onClick={() => setActiveInputTab('url')}
            className={`px-4 py-2 rounded-xl text-xs font-bold flex items-center gap-2 transition ${
              activeInputTab === 'url'
                ? 'bg-indigo-600 text-white shadow-md shadow-indigo-500/20'
                : 'bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 hover:bg-slate-200 dark:hover:bg-slate-700'
            }`}
          >
            <LinkIcon className="w-4 h-4" />
            {t('tabs.url')}
          </button>

          <button
            onClick={() => setActiveInputTab('image')}
            className={`px-4 py-2 rounded-xl text-xs font-bold flex items-center gap-2 transition ${
              activeInputTab === 'image'
                ? 'bg-indigo-600 text-white shadow-md shadow-indigo-500/20'
                : 'bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 hover:bg-slate-200 dark:hover:bg-slate-700'
            }`}
          >
            <ImageIcon className="w-4 h-4" />
            {t('tabs.image')}
          </button>
        </div>

        {/* Input Controls */}
        {activeInputTab === 'text' && (
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <label className="text-xs font-semibold text-slate-600 dark:text-slate-300">
                Suspicious SMS / WhatsApp / Message Body
              </label>
              <VoiceInput
                onTranscript={(txt) => setTextInput((prev) => (prev ? prev + ' ' + txt : txt))}
                selectedLang={language === 'hi' ? 'hi-IN' : (language === 'te' ? 'te-IN' : 'en-IN')}
              />
            </div>
            <textarea
              rows="5"
              value={textInput}
              onChange={(e) => setTextInput(e.target.value)}
              placeholder={t('analyzer.textPlaceholder')}
              className="w-full p-4 text-sm rounded-2xl bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-indigo-500 focus:outline-hidden transition"
            />
          </div>
        )}

        {activeInputTab === 'url' && (
          <div className="space-y-2">
            <label className="text-xs font-semibold text-slate-600 dark:text-slate-300">
              Suspicious Link (Static Analysis only — Never opened or executed)
            </label>
            <input
              type="text"
              value={urlInput}
              onChange={(e) => setUrlInput(e.target.value)}
              placeholder={t('analyzer.urlPlaceholder')}
              className="w-full p-4 text-sm rounded-2xl bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-indigo-500 focus:outline-hidden transition"
            />
          </div>
        )}

        {activeInputTab === 'image' && (
          <div className="space-y-4">
            <label className="text-xs font-semibold text-slate-600 dark:text-slate-300">
              Payment Screenshot or QR Code
            </label>
            <div className="border-2 border-dashed border-slate-300 dark:border-slate-700 rounded-2xl p-6 text-center hover:bg-slate-50/50 dark:hover:bg-slate-950/50 transition cursor-pointer relative">
              <input
                type="file"
                accept="image/png, image/jpeg, image/jpg, image/webp"
                onChange={handleFileChange}
                className="absolute inset-0 opacity-0 cursor-pointer w-full h-full"
              />
              {filePreview ? (
                <div className="flex flex-col items-center gap-3">
                  <img src={filePreview} alt="Upload preview" className="max-h-48 rounded-xl object-contain shadow-md" />
                  <p className="text-xs font-semibold text-indigo-600 dark:text-indigo-400">
                    {selectedFile?.name} (Click to replace)
                  </p>
                </div>
              ) : (
                <div className="flex flex-col items-center gap-2">
                  <div className="p-3 rounded-full bg-indigo-50 dark:bg-indigo-950 text-indigo-600 dark:text-indigo-400">
                    <Upload className="w-6 h-6" />
                  </div>
                  <p className="text-sm font-bold text-slate-800 dark:text-slate-200">
                    {t('analyzer.uploadPrompt')}
                  </p>
                  <p className="text-xs text-slate-500">
                    {t('analyzer.uploadHint')}
                  </p>
                </div>
              )}
            </div>
          </div>
        )}

        {/* Demo Chips Section */}
        {demoExamples.length > 0 && (
          <div className="space-y-2.5 pt-2">
            <span className="text-xs font-bold text-slate-500 dark:text-slate-400 uppercase tracking-wider">
              {t('analyzer.sampleChipsTitle')}
            </span>
            <div className="flex items-center gap-2 overflow-x-auto pb-2 scrollbar-none">
              {demoExamples.slice(0, 8).map((chip) => (
                <button
                  key={chip.id}
                  onClick={() => handleApplyChip(chip)}
                  className="px-3 py-1.5 rounded-full text-xs font-semibold whitespace-nowrap bg-slate-100 dark:bg-slate-800 hover:bg-indigo-50 dark:hover:bg-indigo-950/60 hover:text-indigo-600 dark:hover:text-indigo-400 text-slate-700 dark:text-slate-300 border border-slate-200 dark:border-slate-700 transition"
                >
                  {chip.label}
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Error message banner */}
        {error && (
          <div className="p-3.5 rounded-xl bg-rose-50 dark:bg-rose-950/50 border border-rose-200 dark:border-rose-800 text-rose-700 dark:text-rose-300 text-xs font-semibold">
            {error}
          </div>
        )}

        {/* Bottom Actions Bar */}
        <div className="flex flex-col sm:flex-row items-center justify-between gap-4 pt-4 border-t border-slate-100 dark:border-slate-800">
          <label className="flex items-center gap-2 cursor-pointer text-xs font-medium text-slate-600 dark:text-slate-400">
            <input
              type="checkbox"
              checked={saveHistory}
              onChange={(e) => setSaveHistory(e.target.checked)}
              className="rounded border-slate-300 text-indigo-600 focus:ring-indigo-500"
            />
            <span>{t('analyzer.saveHistoryLabel')}</span>
          </label>

          <button
            onClick={handleAnalyze}
            disabled={loading}
            className="w-full sm:w-auto px-8 py-3.5 rounded-2xl bg-indigo-600 hover:bg-indigo-500 text-white font-extrabold text-sm tracking-wide shadow-lg shadow-indigo-600/30 flex items-center justify-center gap-2 transition transform active:scale-95 disabled:opacity-50"
          >
            {loading ? (
              <>
                <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                <span>{t('analyzer.analyzing')}</span>
              </>
            ) : (
              <>
                <ShieldAlert className="w-4 h-4" />
                <span>{t('analyzer.analyzeBtn')}</span>
              </>
            )}
          </button>
        </div>
      </div>

      {/* Safety Report Output Card */}
      {report && (
        <div className="bg-white dark:bg-slate-900 rounded-3xl border border-slate-200 dark:border-slate-800 shadow-2xl p-6 sm:p-8 space-y-8 animate-fade-in">
          
          {/* Top Verdict Row */}
          <div className="flex flex-col lg:flex-row items-center gap-6 pb-6 border-b border-slate-100 dark:border-slate-800">
            <ScoreGauge score={report.risk_score} verdict={report.verdict} />
            
            <div className="space-y-2.5 flex-1 text-center lg:text-left">
              <div className="inline-block px-3 py-1 rounded-lg text-xs font-bold uppercase tracking-wider bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300">
                {report.detected_category.replace(/_/g, ' ')}
              </div>
              <h2 className="text-xl sm:text-2xl font-extrabold text-slate-900 dark:text-white">
                {report.verdict === 'HIGH RISK' ? '🚨 High Risk Digital Payment Scam Detected' : (report.verdict === 'SUSPICIOUS' ? '⚠️ Suspicious Threat Signals Found' : '✅ No Strong Scam Patterns Found')}
              </h2>
              <p className="text-sm text-slate-600 dark:text-slate-300 leading-relaxed font-medium">
                {report.plain_language_explanation}
              </p>
            </div>

            {/* Quick Share / Report Buttons */}
            <div className="flex lg:flex-col gap-2 shrink-0">
              <button
                onClick={handleCopySummary}
                className="px-3.5 py-2 rounded-xl text-xs font-bold border border-slate-200 dark:border-slate-800 hover:bg-slate-100 dark:hover:bg-slate-800 text-slate-700 dark:text-slate-300 flex items-center gap-1.5 transition"
              >
                {copied ? <Check className="w-3.5 h-3.5 text-emerald-500" /> : <Copy className="w-3.5 h-3.5" />}
                <span>{copied ? t('report.copied') : t('report.copySummaryBtn')}</span>
              </button>

              <button
                onClick={() => setReportModalOpen(true)}
                className="px-3.5 py-2 rounded-xl text-xs font-bold bg-rose-50 dark:bg-rose-950/40 text-rose-700 dark:text-rose-300 border border-rose-200 dark:border-rose-800 hover:bg-rose-100 dark:hover:bg-rose-900/40 flex items-center gap-1.5 transition"
              >
                <Flag className="w-3.5 h-3.5" />
                <span>{t('report.reportScamBtn')}</span>
              </button>
            </div>
          </div>

          {/* Evidence and Recommended Actions 2-Column Grid */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {/* Left: Ranked Evidence List */}
            <div className="space-y-3">
              <h3 className="text-sm font-bold uppercase tracking-wider text-slate-900 dark:text-white flex items-center gap-2">
                <ShieldAlert className="w-4 h-4 text-indigo-500" />
                {t('report.evidenceTitle')}
              </h3>
              <EvidenceList evidence={report.evidence} />
            </div>

            {/* Right: Recommended Actions Box */}
            <div className="space-y-3">
              <h3 className="text-sm font-bold uppercase tracking-wider text-slate-900 dark:text-white flex items-center gap-2">
                <ShieldCheck className="w-4 h-4 text-emerald-500" />
                {t('report.actionsTitle')}
              </h3>
              <ActionBox actions={report.recommended_actions} verdict={report.verdict} />
            </div>
          </div>

          {/* RAG Knowledge Citations Box */}
          {report.citations && report.citations.length > 0 && (
            <div className="p-5 rounded-2xl bg-indigo-50/50 dark:bg-indigo-950/20 border border-indigo-100 dark:border-indigo-900/50 space-y-3">
              <h4 className="text-xs font-extrabold uppercase tracking-wider text-indigo-900 dark:text-indigo-300 flex items-center gap-1.5">
                <BookOpen className="w-4 h-4" />
                {t('report.citationsTitle')}
              </h4>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                {report.citations.map((c, i) => (
                  <div key={i} className="p-3.5 rounded-xl bg-white dark:bg-slate-900 border border-indigo-100 dark:border-slate-800 text-xs space-y-1.5">
                    <p className="font-bold text-slate-900 dark:text-white">{c.title}</p>
                    <p className="text-slate-600 dark:text-slate-400 line-clamp-3">{c.content}</p>
                    <p className="text-[10px] font-semibold text-indigo-600 dark:text-indigo-400">
                      Source: {c.source}
                    </p>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Heuristic Disclaimer */}
          <div className="p-4 rounded-xl bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 text-xs text-slate-500 dark:text-slate-400 flex items-start gap-2.5">
            <Info className="w-4 h-4 text-slate-400 shrink-0 mt-0.5" />
            <p>{report.disclaimer}</p>
          </div>
        </div>
      )}

      {/* Threat Report Submission Modal */}
      <ReportModal
        isOpen={reportModalOpen}
        onClose={() => setReportModalOpen(false)}
        analysisId={report?.id}
        inputType={activeInputTab}
        defaultContent={report?.masked_input || textInput || urlInput}
        defaultCategory={report?.detected_category || 'general_fraud'}
      />
    </div>
  );
}
