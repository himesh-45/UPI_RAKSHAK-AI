import React, { useState } from 'react';
import { Lightbulb, RefreshCw, BookOpen } from 'lucide-react';

export default function SecurityTipCard({ language = 'en', onOpenLearn = null }) {
  const tips = [
    {
      en: "Never enter your UPI PIN to receive money, refunds, or lottery prizes. A PIN is strictly used to debit funds from your account.",
      hi: "पैसे या रिफंड प्राप्त करने के लिए कभी भी अपना यूपीआई पिन न डालें। पिन का उपयोग केवल आपके खाते से पैसे भेजने के लिए होता है।",
      te: "డబ్బులు లేదా క్యాష్‌బ్యాక్ అందుకోవడానికి ఎప్పుడూ యూపీఐ పిన్ నమోదు చేయవద్దు. పిన్ కేవలం డబ్బులు పంపేందుకు మాత్రమే."
    },
    {
      en: "Indian police or CBI officers never conduct interrogations or demand money via WhatsApp or Skype video calls. Digital arrest does not legally exist.",
      hi: "भारतीय पुलिस या सीबीआई कभी भी व्हाट्सएप या स्काइप वीडियो कॉल पर पूछताछ या पैसे की मांग नहीं करते। डिजिटल अरेस्ट कानूनन कोई चीज़ नहीं है।",
      te: "పోలీసులు ఎప్పుడూ వీడియో కాల్స్‌లో విచారణలు జరపరు మరియు డబ్బులు డిమాండ్ చేయరు. డిజిటల్ అరెస్ట్ పూర్తిగా నకిలీ."
    },
    {
      en: "If money is debited fraudulently, call 1930 immediately within the Golden Hour (first 2-3 hours) so the beneficiary account can be frozen.",
      hi: "यदि धोखाधड़ी से पैसे कट जाएं, तो तुरंत पहले 2-3 घंटे (गोल्डन ऑवर) में 1930 पर कॉल करें ताकि आरोपी का बैंक खाता फ्रीज हो सके।",
      te: "ఖాతా నుండి డబ్బులు మోసపూరితంగా కట్ అయితే వెంటనే మొదటి 2-3 గంటల్లో 1930 కు కాల్ చేసి ఖాతాను ఫ్రీజ్ చేయించండి."
    },
    {
      en: "Never install AnyDesk or TeamViewer on instructions of customer care. Fraudsters use screen sharing to view your banking OTPs live.",
      hi: "कस्टमर केयर के कहने पर कभी भी AnyDesk या TeamViewer डाउनलोड न करें। धोखेबाज स्क्रीन शेयरिंग के जरिए आपके ओटीपी देख लेते हैं।",
      te: "కస్టమర్ కేర్ పేరుతో AnyDesk లేదా TeamViewer డౌన్‌లోడ్ చేయవద్దు. మోసగాళ్లు లైవ్‌గా మీ బ్యాంకింగ్ ఓటీపీలు చూస్తారు."
    },
    {
      en: "Verify how many mobile SIMs are registered on your Aadhaar using the official Government TAFCOP portal (tafcop.sancharsaathi.gov.in).",
      hi: "आपके आधार पर कितने सिम चल रहे हैं, इसकी जांच सरकार के आधिकारिक TAFCOP पोर्टल (tafcop.sancharsaathi.gov.in) पर करें।",
      te: "మీ ఆధార్‌పై ఎన్ని సిమ్ కార్డులు ఉన్నాయో ప్రభుత్వ అధికారిక TAFCOP పోర్టల్ ద్వారా తనిఖీ చేసుకోండి."
    }
  ];

  const [tipIndex, setTipIndex] = useState(0);

  const rotateTip = () => {
    setTipIndex((prev) => (prev + 1) % tips.length);
  };

  const currentTip = tips[tipIndex];

  const labels = {
    en: { title: "Security Tip of the Day", rotate: "New Tip", learnMore: "Learn Red Flags" },
    hi: { title: "आज का सुरक्षा सुझाव", rotate: "नया सुझाव", learnMore: "धोखे की पहचान सीखें" },
    te: { title: "ఈ రోజు భద్రతా చిట్కా", rotate: "మరో చిట్కా", learnMore: "మోసాల గుర్తింపు నేర్చుకోండి" }
  };

  const l = labels[language] || labels.en;

  return (
    <div className="p-3.5 bg-slate-900/90 border border-cyan-500/25 rounded-xl shadow-md text-slate-100 flex flex-col justify-between">
      <div>
        <div className="flex items-center justify-between pb-2 border-b border-slate-800">
          <div className="flex items-center gap-2 text-cyan-400">
            <Lightbulb className="w-4 h-4 text-amber-400" />
            <span className="text-xs font-bold uppercase font-mono tracking-wider">
              {l.title}
            </span>
          </div>
          <button
            onClick={rotateTip}
            className="flex items-center gap-1 text-[11px] text-slate-400 hover:text-cyan-400 transition-colors"
            title="Rotate to next security tip"
          >
            <RefreshCw className="w-3 h-3" />
            <span>{l.rotate}</span>
          </button>
        </div>

        <p className="mt-2.5 text-xs text-slate-300 leading-relaxed italic">
          "{currentTip[language] || currentTip.en}"
        </p>
      </div>

      {onOpenLearn && (
        <div className="mt-3 pt-2 border-t border-slate-800/80 flex justify-end">
          <button
            onClick={onOpenLearn}
            className="inline-flex items-center gap-1.5 text-xs font-medium text-cyan-400 hover:text-cyan-300 transition-colors"
          >
            <BookOpen className="w-3.5 h-3.5" />
            <span>{l.learnMore} →</span>
          </button>
        </div>
      )}
    </div>
  );
}
