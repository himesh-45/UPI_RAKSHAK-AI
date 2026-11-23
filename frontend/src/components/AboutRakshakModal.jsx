import React from 'react';
import { X, ShieldCheck, Lock, EyeOff, BookOpen, AlertTriangle } from 'lucide-react';
import GuardianAvatar from './GuardianAvatar';

export default function AboutRakshakModal({ isOpen, onClose, language = 'en' }) {
  if (!isOpen) return null;

  const content = {
    en: {
      title: "About Rakshak Assistant",
      subtitle: "Grounded AI Digital Guardian for Financial Cybersecurity",
      purityTitle: "Deterministic Verdict Purity",
      purityDesc: "The language model NEVER gives its own scam verdict. Threat verdicts and risk scores originate strictly from verified detector tools and statutory rules.",
      privacyTitle: "Zero Plaintext PII Storage",
      privacyDesc: "Your phone numbers, bank accounts, and OTPs are redacted locally as [PHONE], [ACCOUNT], [OTP] before external processing. No sensitive PII is logged.",
      groundingTitle: "Human-Reviewed Knowledge Base",
      groundingDesc: "All procedures are strictly retrieved from 160+ human-reviewed entries grounded in MHA (1930), RBI master directions, NPCI circulars, and DoT Sanchar Saathi.",
      statesTitle: "Guardian States",
      close: "Close"
    },
    hi: {
      title: "रक्षक असिस्टेंट के बारे में",
      subtitle: "वित्तीय साइबर सुरक्षा के लिए प्रमाणित एआई डिजिटल रक्षक",
      purityTitle: "सटीक और निष्पक्ष निर्णय",
      purityDesc: "लैंग्वेज मॉडल कभी भी अपने मन से कोई फैसला या स्कोर नहीं देता। जोखिम स्कोर केवल समर्पित डिटेक्टर टूल्स और सरकारी नियमों द्वारा निर्धारित होता है।",
      privacyTitle: "गोपनीयता और डेटा सुरक्षा",
      privacyDesc: "आपके फोन नंबर, बैंक खाते और ओटीपी को बाहरी प्रोसेसिंग से पहले [PHONE], [ACCOUNT], [OTP] से बदल दिया जाता है। कोई निजी जानकारी स्टोर नहीं होती।",
      groundingTitle: "सत्यापित ज्ञानकोश (Knowledge Base)",
      groundingDesc: "सभी दिशानिर्देश गृह मंत्रालय (1930), भारतीय रिजर्व बैंक (RBI), एनपीसीआई और संचार साथी के आधिकारिक नियमों पर आधारित हैं।",
      statesTitle: "रक्षक के अवस्थाएं (States)",
      close: "बंद करें"
    },
    te: {
      title: "రక్షక్ అసిస్టెంట్ గురించి",
      subtitle: "ఆర్థిక సైబర్ భద్రత కోసం ధృవీకరించబడిన ఏఐ డిజిటల్ గార్డియన్",
      purityTitle: "ఖచ్చితమైన భద్రతా నిర్ణయం",
      purityDesc: "లాంగ్వేజ్ మోడల్ స్వయంగా ఎటువంటి స్కామ్ తీర్పు ఇవ్వదు. ముప్పు విశ్లేషణ కేవలం అధికారిక డిటెక్టర్ టూల్స్ ద్వారా మాత్రమే జరుగుతుంది.",
      privacyTitle: "పూర్తి డేటా గోప్యత",
      privacyDesc: "మీ ఫోన్ నంబర్లు, బ్యాంక్ ఖాతాలు మరియు ఓటీపీలు ఎవరికీ వెల్లడి కాకుండా [PHONE], [ACCOUNT], [OTP] గా స్థానికంగా మాస్క్ చేయబడతాయి.",
      groundingTitle: "సమీక్షించిన అధికారిక మార్గదర్శకాలు",
      groundingDesc: "అన్ని పరిష్కారాలు కేంద్ర హోం శాఖ (1930), ఆర్బీఐ, ఎన్‌పీసీఐ నిబంధనల ఆధారంగా మాత్రమే అందించబడతాయి.",
      statesTitle: "రక్షక్ రూపాలు (States)",
      close: "మూసివేయి"
    }
  };

  const text = content[language] || content.en;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-[#050A18]/80 backdrop-blur-md animate-fadeIn">
      <div className="relative w-full max-w-lg bg-[#0F1D3A] border border-[#1E3A5F] border-t-2 border-t-[#D9A441] rounded-2xl shadow-2xl p-6 text-[#F5F1E6] overflow-hidden">
        {/* Ambient Top Glow */}
        <div className="absolute -top-12 left-1/2 -translate-x-1/2 w-64 h-24 bg-[#35D0C8]/15 rounded-full blur-2xl pointer-events-none" />

        {/* Header */}
        <div className="flex items-start justify-between pb-4 border-b border-[#1E3A5F]">
          <div className="flex items-center gap-3">
            <GuardianAvatar state="idle" size={42} />
            <div>
              <h2 className="text-lg font-bold text-[#F5F1E6] font-sans tracking-wide">{text.title}</h2>
              <p className="text-xs text-[#35D0C8] font-mono">{text.subtitle}</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 text-[#A9B4CC] hover:text-[#F5F1E6] rounded-lg hover:bg-[#14254B] transition-colors"
            aria-label={text.close}
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Body Pillars */}
        <div className="mt-4 space-y-3.5 text-xs">
          <div className="p-3 bg-[#0B1530] rounded-xl border border-[#1E3A5F] flex items-start gap-3">
            <ShieldCheck className="w-5 h-5 text-[#34D399] shrink-0 mt-0.5" />
            <div>
              <h3 className="font-semibold text-[#F5F1E6]">{text.purityTitle}</h3>
              <p className="text-[#A9B4CC] mt-0.5 leading-relaxed">{text.purityDesc}</p>
            </div>
          </div>

          <div className="p-3 bg-[#0B1530] rounded-xl border border-[#1E3A5F] flex items-start gap-3">
            <EyeOff className="w-5 h-5 text-[#35D0C8] shrink-0 mt-0.5" />
            <div>
              <h3 className="font-semibold text-[#F5F1E6]">{text.privacyTitle}</h3>
              <p className="text-[#A9B4CC] mt-0.5 leading-relaxed">{text.privacyDesc}</p>
            </div>
          </div>

          <div className="p-3 bg-[#0B1530] rounded-xl border border-[#1E3A5F] flex items-start gap-3">
            <BookOpen className="w-5 h-5 text-[#F5C96A] shrink-0 mt-0.5" />
            <div>
              <h3 className="font-semibold text-[#F5F1E6]">{text.groundingTitle}</h3>
              <p className="text-[#A9B4CC] mt-0.5 leading-relaxed">{text.groundingDesc}</p>
            </div>
          </div>

          {/* States Gallery */}
          <div className="pt-2">
            <h4 className="text-xs font-semibold text-[#A9B4CC] uppercase tracking-wider mb-2 font-mono">
              {text.statesTitle}
            </h4>
            <div className="grid grid-cols-5 gap-2 text-center">
              <div className="p-2 bg-[#0B1530] rounded-lg border border-[#1E3A5F] flex flex-col items-center">
                <GuardianAvatar state="idle" size={28} />
                <span className="text-[10px] mt-1 text-[#A9B4CC] font-mono">Idle</span>
              </div>
              <div className="p-2 bg-[#0B1530] rounded-lg border border-[#1E3A5F] flex flex-col items-center">
                <GuardianAvatar state="listening" size={28} />
                <span className="text-[10px] mt-1 text-[#F5C96A] font-mono">Listening</span>
              </div>
              <div className="p-2 bg-[#0B1530] rounded-lg border border-[#1E3A5F] flex flex-col items-center">
                <GuardianAvatar state="scanning" size={28} />
                <span className="text-[10px] mt-1 text-[#35D0C8] font-mono">Scanning</span>
              </div>
              <div className="p-2 bg-[#0B1530] rounded-lg border border-[#1E3A5F] flex flex-col items-center">
                <GuardianAvatar state="safe" size={28} />
                <span className="text-[10px] mt-1 text-[#34D399] font-mono">Safe</span>
              </div>
              <div className="p-2 bg-[#0B1530] rounded-lg border border-[#1E3A5F] flex flex-col items-center">
                <GuardianAvatar state="alert" size={28} />
                <span className="text-[10px] mt-1 text-[#F43F5E] font-mono">Alert</span>
              </div>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="mt-5 pt-3 border-t border-[#1E3A5F] flex justify-end">
          <button
            onClick={onClose}
            className="px-4 py-2 bg-[#14254B] hover:bg-[#1E3A5F] text-[#F5F1E6] text-xs font-semibold rounded-lg transition-colors border border-[#1E3A5F]"
          >
            {text.close}
          </button>
        </div>
      </div>
    </div>
  );
}
