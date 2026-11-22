import React, { useState, useEffect, useRef } from 'react';
import {
  Bell, ShieldAlert, MessageSquare, AlertTriangle, Check,
  Volume2, VolumeX, ExternalLink, X, Radio, ArrowRight
} from 'lucide-react';
import { getAdminAlerts, markAdminAlertsRead } from '../api/client';

// Web Audio API Alarm Sound Synthesizer (Zero External Audio Dependencies)
export function playAdminChime() {
  try {
    const AudioContextClass = window.AudioContext || window.webkitAudioContext;
    if (!AudioContextClass) return;
    const ctx = new AudioContextClass();
    const now = ctx.currentTime;

    // Primary alert sweep: 880Hz (A5) -> 1320Hz (E6)
    const osc1 = ctx.createOscillator();
    const gain1 = ctx.createGain();
    osc1.type = 'sine';
    osc1.frequency.setValueAtTime(880, now);
    osc1.frequency.exponentialRampToValueAtTime(1320, now + 0.14);
    gain1.gain.setValueAtTime(0.3, now);
    gain1.gain.exponentialRampToValueAtTime(0.001, now + 0.38);
    osc1.connect(gain1);
    gain1.connect(ctx.destination);
    osc1.start(now);
    osc1.stop(now + 0.38);

    // High harmonic chime: 1760Hz (A6)
    const osc2 = ctx.createOscillator();
    const gain2 = ctx.createGain();
    osc2.type = 'triangle';
    osc2.frequency.setValueAtTime(1760, now + 0.16);
    gain2.gain.setValueAtTime(0.22, now + 0.16);
    gain2.gain.exponentialRampToValueAtTime(0.001, now + 0.55);
    osc2.connect(gain2);
    gain2.connect(ctx.destination);
    osc2.start(now + 0.16);
    osc2.stop(now + 0.55);
  } catch (err) {
    console.warn('Alarm chime suppressed by browser autoplay policy:', err);
  }
}

export default function AdminAlarmBell({ onNavigateToDashboard }) {
  const [isOpen, setIsOpen] = useState(false);
  const [alerts, setAlerts] = useState([]);
  const [unreadCount, setUnreadCount] = useState(2);
  const [filter, setFilter] = useState('all'); // 'all', 'case_filed', 'user_feedback'
  const [isRinging, setIsRinging] = useState(false);
  const [toastAlert, setToastAlert] = useState(null);
  const [soundEnabled, setSoundEnabled] = useState(() => {
    return localStorage.getItem('upi_alarm_sound') !== 'false';
  });

  const previousCountRef = useRef(0);
  const dropdownRef = useRef(null);

  // Fetch alerts from backend
  const fetchAlerts = async (silent = false) => {
    try {
      const data = await getAdminAlerts(35);
      if (data && Array.isArray(data.alerts)) {
        setAlerts(data.alerts);

        // Calculate unread items based on last read timestamp stored in localStorage
        const lastReadTime = parseInt(localStorage.getItem('upi_alarm_last_read') || '0', 10);
        const newUnread = data.alerts.filter(a => {
          const alertTime = new Date(a.created_at).getTime();
          return alertTime > lastReadTime;
        }).length;

        // If count increased since last poll, trigger alarm ring & chime
        if (!silent && previousCountRef.current > 0 && data.total_alerts > previousCountRef.current) {
          triggerAlarmAlert({
            title: data.alerts[0]?.title || '🚨 New Incident Alert',
            subtitle: data.alerts[0]?.content || 'New case or feedback received',
            type: data.alerts[0]?.type || 'case_filed'
          });
        }

        previousCountRef.current = data.total_alerts;
        setUnreadCount(lastReadTime === 0 ? Math.max(data.unread_count, 2) : newUnread);
      }
    } catch (err) {
      console.warn('Failed to fetch admin alerts:', err);
    }
  };

  // Trigger live alarm ring, chime sound and visual toast
  const triggerAlarmAlert = (alertInfo) => {
    setIsRinging(true);
    setTimeout(() => setIsRinging(false), 2400);

    if (soundEnabled) {
      playAdminChime();
    }

    setToastAlert(alertInfo);
    setTimeout(() => {
      setToastAlert(null);
    }, 4500);

    setUnreadCount(prev => prev + 1);
  };

  // Initial load and periodic polling every 10 seconds
  useEffect(() => {
    fetchAlerts(true);
    const interval = setInterval(() => {
      fetchAlerts(false);
    }, 10000);
    return () => clearInterval(interval);
  }, [soundEnabled]);

  // Listen to live client events dispatched when user feedback or reports are filed
  useEffect(() => {
    const handleLiveAlertEvent = (e) => {
      const detail = e.detail || {};
      const newAlert = {
        id: `live-${Date.now()}`,
        source_id: Date.now(),
        type: detail.type || 'case_filed',
        category: detail.category || 'general_fraud',
        title: detail.title || '🚨 New Case Filed',
        content: detail.content || 'Citizen reported threat incident',
        comments: detail.comments || 'Direct submission',
        status: 'PENDING_REVIEW',
        severity: 'CRITICAL',
        created_at: detail.timestamp || new Date().toISOString(),
        time_ago: 'Just now'
      };

      setAlerts(prev => [newAlert, ...prev]);
      triggerAlarmAlert({
        title: newAlert.title,
        subtitle: newAlert.content,
        type: newAlert.type
      });

      // Synchronize with backend after short delay
      setTimeout(() => fetchAlerts(true), 1200);
    };

    window.addEventListener('upi-admin-alert-trigger', handleLiveAlertEvent);
    return () => {
      window.removeEventListener('upi-admin-alert-trigger', handleLiveAlertEvent);
    };
  }, [soundEnabled]);

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (e) => {
      if (dropdownRef.current && !dropdownRef.current.contains(e.target)) {
        setIsOpen(false);
      }
    };
    if (isOpen) {
      document.addEventListener('mousedown', handleClickOutside);
    }
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, [isOpen]);

  const toggleSound = () => {
    const nextState = !soundEnabled;
    setSoundEnabled(nextState);
    localStorage.setItem('upi_alarm_sound', nextState ? 'true' : 'false');
    if (nextState) {
      playAdminChime();
    }
  };

  const handleMarkAllRead = async () => {
    try {
      await markAdminAlertsRead();
    } catch {
      // Ignore network errors on local
    }
    localStorage.setItem('upi_alarm_last_read', Date.now().toString());
    setUnreadCount(0);
  };

  const filteredAlerts = alerts.filter(a => {
    if (filter === 'all') return true;
    return a.type === filter;
  });

  const casesCount = alerts.filter(a => a.type === 'case_filed').length;
  const feedbackCount = alerts.filter(a => a.type === 'user_feedback').length;

  return (
    <div className="relative" ref={dropdownRef}>
      {/* Alarm Bell Button with Live Badge */}
      <button
        onClick={() => {
          setIsOpen(!isOpen);
          if (!isOpen && unreadCount > 0) {
            // Optional: Mark as seen when opening
          }
        }}
        className={`relative p-2 rounded-xl bg-[#0c122b] border transition cursor-pointer select-none ${
          isRinging
            ? 'border-rose-500 text-rose-400 shadow-[0_0_20px_rgba(244,63,94,0.7)] animate-bounce'
            : unreadCount > 0
            ? 'border-rose-500/40 text-cyan-400 hover:text-white hover:border-cyan-400/60'
            : 'border-cyan-500/20 text-cyan-400 hover:text-white hover:border-cyan-400/50'
        }`}
        title={`Admin Incident & Feedback Alarm (${unreadCount} unread)`}
        aria-label="Admin Alerts Alarm"
      >
        <Bell className={`w-4 h-4 ${isRinging ? 'animate-wiggle text-rose-400' : ''}`} />

        {unreadCount > 0 && (
          <span className="absolute -top-1 -right-1 w-4 h-4 rounded-full bg-rose-500 text-white text-[10px] font-black flex items-center justify-center shadow-[0_0_10px_rgba(239,68,68,0.85)] ring-2 ring-[#060919] animate-pulse">
            {unreadCount > 9 ? '9+' : unreadCount}
          </span>
        )}
      </button>

      {/* Interactive Cyber Alarm & Notification Dropdown */}
      {isOpen && (
        <div className="absolute right-0 mt-2 w-96 max-w-[90vw] bg-[#080d22]/98 backdrop-blur-xl border border-cyan-500/30 rounded-2xl shadow-[0_12px_40px_rgba(0,0,0,0.8)] z-50 overflow-hidden animate-in fade-in zoom-in-95 duration-150">
          {/* Header */}
          <div className="p-3.5 border-b border-cyan-500/20 bg-[#060919]/90 flex items-center justify-between">
            <div className="flex items-center gap-2">
              <div className="p-1.5 rounded-lg bg-rose-500/10 border border-rose-500/30 text-rose-400">
                <ShieldAlert className="w-4 h-4" />
              </div>
              <div>
                <h4 className="text-xs font-black text-white uppercase tracking-wider flex items-center gap-1.5">
                  Admin Alarm Center
                  <span className="flex h-2 w-2 relative">
                    <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-rose-400 opacity-75"></span>
                    <span className="relative inline-flex rounded-full h-2 w-2 bg-rose-500"></span>
                  </span>
                </h4>
                <p className="text-[10px] text-slate-400">Cases filed & citizen feedback alerts</p>
              </div>
            </div>

            <div className="flex items-center gap-1.5">
              {/* Sound Toggle */}
              <button
                onClick={toggleSound}
                className={`p-1.5 rounded-lg border text-xs transition ${
                  soundEnabled
                    ? 'border-cyan-500/40 bg-cyan-500/10 text-cyan-300 hover:bg-cyan-500/20'
                    : 'border-slate-700 bg-slate-800 text-slate-400 hover:text-slate-200'
                }`}
                title={soundEnabled ? 'Alarm Sound: Enabled' : 'Alarm Sound: Muted'}
              >
                {soundEnabled ? <Volume2 className="w-3.5 h-3.5" /> : <VolumeX className="w-3.5 h-3.5" />}
              </button>

              {/* Test Chime Button */}
              <button
                onClick={() => playAdminChime()}
                className="px-2 py-1 rounded-lg border border-cyan-500/30 bg-cyan-950/40 hover:bg-cyan-900/60 text-cyan-300 text-[10px] font-bold transition"
                title="Play test alert chime"
              >
                Test Chime
              </button>

              {/* Close */}
              <button
                onClick={() => setIsOpen(false)}
                className="p-1 rounded-lg text-slate-400 hover:text-white"
              >
                <X className="w-4 h-4" />
              </button>
            </div>
          </div>

          {/* Filter Pills & Actions */}
          <div className="px-3 py-2 bg-[#0a0f28] border-b border-cyan-500/10 flex items-center justify-between text-[11px]">
            <div className="flex items-center gap-1">
              <button
                onClick={() => setFilter('all')}
                className={`px-2 py-0.5 rounded-md font-bold transition ${
                  filter === 'all'
                    ? 'bg-cyan-500/20 text-cyan-300 border border-cyan-400/40'
                    : 'text-slate-400 hover:text-slate-200'
                }`}
              >
                All ({alerts.length})
              </button>
              <button
                onClick={() => setFilter('case_filed')}
                className={`px-2 py-0.5 rounded-md font-bold transition ${
                  filter === 'case_filed'
                    ? 'bg-rose-500/20 text-rose-300 border border-rose-400/40'
                    : 'text-slate-400 hover:text-slate-200'
                }`}
              >
                🚨 Cases ({casesCount})
              </button>
              <button
                onClick={() => setFilter('user_feedback')}
                className={`px-2 py-0.5 rounded-md font-bold transition ${
                  filter === 'user_feedback'
                    ? 'bg-amber-500/20 text-amber-300 border border-amber-400/40'
                    : 'text-slate-400 hover:text-slate-200'
                }`}
              >
                💬 Feedback ({feedbackCount})
              </button>
            </div>

            {unreadCount > 0 && (
              <button
                onClick={handleMarkAllRead}
                className="text-[10px] text-cyan-400 hover:text-cyan-300 font-semibold flex items-center gap-1"
              >
                <Check className="w-3 h-3" /> Mark read
              </button>
            )}
          </div>

          {/* Scrollable Alerts List */}
          <div className="max-h-80 overflow-y-auto divide-y divide-cyan-500/10 text-xs">
            {filteredAlerts.length === 0 ? (
              <div className="p-8 text-center text-slate-400">
                <Check className="w-8 h-8 mx-auto mb-2 text-emerald-400 opacity-60" />
                <p className="font-bold text-slate-300 text-xs">All Clear!</p>
                <p className="text-[11px]">No incident cases or feedback alerts pending.</p>
              </div>
            ) : (
              filteredAlerts.map(alert => (
                <div
                  key={alert.id}
                  className="p-3 hover:bg-cyan-950/20 transition flex flex-col gap-1.5"
                >
                  <div className="flex items-start justify-between gap-2">
                    <div className="flex items-center gap-1.5 font-bold text-white text-xs">
                      {alert.type === 'case_filed' ? (
                        <span className="text-rose-400">🚨</span>
                      ) : alert.type === 'user_feedback' ? (
                        <span className="text-amber-400">💬</span>
                      ) : (
                        <span className="text-cyan-400">⚠️</span>
                      )}
                      <span className="truncate">{alert.title}</span>
                    </div>

                    <span className="text-[10px] text-slate-400 font-mono whitespace-nowrap">
                      {alert.time_ago || 'Recent'}
                    </span>
                  </div>

                  {alert.content && (
                    <p className="text-[11px] text-slate-300 line-clamp-2 bg-slate-900/60 p-1.5 rounded-lg border border-cyan-500/10 font-mono">
                      {alert.content}
                    </p>
                  )}

                  {alert.comments && (
                    <p className="text-[10px] text-slate-400 italic">
                      "{alert.comments}"
                    </p>
                  )}

                  <div className="flex items-center justify-between pt-1">
                    <span className={`px-1.5 py-0.5 rounded text-[9px] font-black uppercase tracking-wider ${
                      alert.severity === 'CRITICAL'
                        ? 'bg-rose-500/20 text-rose-300 border border-rose-500/30'
                        : alert.severity === 'HIGH'
                        ? 'bg-red-500/20 text-red-300 border border-red-500/30'
                        : alert.severity === 'WARNING'
                        ? 'bg-amber-500/20 text-amber-300 border border-amber-500/30'
                        : 'bg-cyan-500/20 text-cyan-300 border border-cyan-500/30'
                    }`}>
                      {alert.status}
                    </span>

                    {onNavigateToDashboard && (
                      <button
                        onClick={() => {
                          setIsOpen(false);
                          onNavigateToDashboard();
                        }}
                        className="text-[10px] text-cyan-400 hover:text-cyan-200 font-bold flex items-center gap-1 hover:underline"
                      >
                        Inspect in Dashboard <ArrowRight className="w-3 h-3" />
                      </button>
                    )}
                  </div>
                </div>
              ))
            )}
          </div>

          {/* Footer with Moderation Direct Link */}
          <div className="p-2.5 bg-[#060919] border-t border-cyan-500/20 flex items-center justify-between text-[11px]">
            <span className="text-slate-400 text-[10px] flex items-center gap-1">
              <Radio className="w-3 h-3 text-cyan-400 animate-pulse" /> Live Polling (10s)
            </span>

            {onNavigateToDashboard && (
              <button
                onClick={() => {
                  setIsOpen(false);
                  onNavigateToDashboard();
                }}
                className="px-2.5 py-1 rounded-lg bg-cyan-500/20 border border-cyan-400/40 text-cyan-300 hover:bg-cyan-500/30 font-bold text-[10px] flex items-center gap-1 transition"
              >
                Open Admin Moderation <ExternalLink className="w-3 h-3" />
              </button>
            )}
          </div>
        </div>
      )}

      {/* Floating Cyber Alert Toast (Pops up whenever a case or feedback arrives) */}
      {toastAlert && (
        <div className="fixed bottom-6 right-6 z-50 max-w-sm w-full bg-[#080d22]/95 backdrop-blur-xl border border-rose-500/50 rounded-2xl p-4 shadow-[0_0_30px_rgba(244,63,94,0.4)] animate-in slide-in-from-bottom-5 duration-200">
          <div className="flex items-start gap-3">
            <div className="p-2 rounded-xl bg-rose-500/20 text-rose-400 border border-rose-500/40 animate-pulse">
              <ShieldAlert className="w-5 h-5" />
            </div>
            <div className="flex-1 min-w-0">
              <div className="flex items-center justify-between">
                <span className="text-[10px] font-black uppercase text-rose-400 tracking-wider">
                  Live Admin Alarm
                </span>
                <button
                  onClick={() => setToastAlert(null)}
                  className="text-slate-400 hover:text-white"
                >
                  <X className="w-3.5 h-3.5" />
                </button>
              </div>
              <h5 className="font-bold text-white text-xs truncate mt-0.5">
                {toastAlert.title}
              </h5>
              <p className="text-[11px] text-slate-300 line-clamp-1 mt-0.5 font-mono">
                {toastAlert.subtitle}
              </p>
              {onNavigateToDashboard && (
                <button
                  onClick={() => {
                    setToastAlert(null);
                    onNavigateToDashboard();
                  }}
                  className="mt-2 text-[10px] font-bold text-cyan-400 hover:text-cyan-200 flex items-center gap-1 hover:underline"
                >
                  Review incident in Admin Dashboard &rarr;
                </button>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
