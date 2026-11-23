import React, { useState } from 'react';
import { X, ChevronLeft, ChevronRight, ShieldCheck, AlertTriangle, Key, Zap, PhoneCall } from 'lucide-react';

export default function LearnCarouselModal({ isOpen, onClose, language = 'en' }) {
  if (!isOpen) return null;

  const [currentIndex, setCurrentIndex] = useState(0);

  const slides = [
    {
      id: 1,
      title: {
        en: "1. The Golden PIN Rule",
        hi: "1. यूपीआई पिन का स्वर्णिम नियम",
        te: "1. యూపీఐ పిన్ గోల్డెన్ రూల్"
      },
      tag: "CORE ARCHITECTURE",
      summary: {
        en: "Entering a UPI PIN is strictly to PAY or SEND money. You NEVER need to enter a PIN to receive money, cashback, or refunds.",
        hi: "यूपीआई पिन केवल पैसे भेजने के लिए होता है। पैसे, कैशबैक या रिफंड प्राप्त करने के लिए कभी भी पिन दर्ज करने की आवश्यकता नहीं होती।",
        te: "డబ్బులు పంపేందుకు మాత్రమే యూపీఐ పిన్ అవసరం. డబ్బులు అందుకోవడానికి లేదా క్యాష్‌బ్యాక్ కోసం ఎప్పుడూ పిన్ ఎంటర్ చేయవద్దు."
      },
      redFlag: {
        en: "Scammer says: 'Scan this QR or enter PIN to claim your Rs 5000 cashback.'",
        hi: "धोखेबाज कहता है: '5000 रुपये कैशबैक पाने के लिए यह क्यूआर कोड स्कैन करें या पिन डालें।'",
        te: "స్కామర్ మాట: 'మీ రూ. 5000 క్యాష్‌బ్యాక్ పొందడానికి ఈ క్యూఆర్ స్కాన్ చేయండి లేదా పిన్ ఎంటర్ చేయండి.'"
      },
      icon: Key
    },
    {
      id: 2,
      title: {
        en: "2. Collect Requests Disguised as Refunds",
        hi: "2. कलेक्ट रिक्वेस्ट का फर्जीवाड़ा",
        te: "2. కలెక్ట్ రిక్వెస్ట్ మోసం"
      },
      tag: "PAYMENT PULL SCAMS",
      summary: {
        en: "Fraudsters send payment requests labeled 'Refund Approved' or 'OLX Payment'. Clicking Pay debits your account instantly.",
        hi: "जालसाज 'रिफंड स्वीकृत' या 'ओएलएक्स पेमेंट' नाम से पैसे काटने की रिक्वेस्ट भेजते हैं। 'Pay' दबाते ही पैसे कट जाते हैं।",
        te: "'రీఫండ్ అప్రూవ్ అయింది' అని కలెక్ట్ రిక్వెస్ట్ పంపుతారు. పే బటన్ నొక్కితే మీ ఖాతా నుండి డబ్బులు కట్ అవుతాయి."
      },
      redFlag: {
        en: "Check the button text: If it asks for 4/6 digit PIN, money is leaving your account.",
        hi: "बटन ध्यान से देखें: यदि 4 या 6 अंकों का पिन मांगा जा रहा है, तो पैसे कट रहे हैं।",
        te: "బటన్ గమనించండి: 4 లేదా 6 అంకెల పిన్ అడిగితే మీ డబ్బులు పోతున్నాయని అర్థం."
      },
      icon: AlertTriangle
    },
    {
      id: 3,
      title: {
        en: "3. Digital Arrest is 100% Illegal & Fake",
        hi: "3. डिजिटल अरेस्ट पूरी तरह गैर-कानूनी और फर्जी है",
        te: "3. డిజిటల్ అరెస్ట్ పూర్తిగా నకిలీ మరియు చట్టవిరుద్ధం"
      },
      tag: "POLICE IMPERSONATION",
      summary: {
        en: "Indian law has NO provision for 'digital arrest'. Real police, CBI, or ED never issue arrest warrants or conduct trials on Skype / WhatsApp.",
        hi: "भारतीय कानून में 'डिजिटल अरेस्ट' जैसा कोई प्रावधान नहीं है। असली पुलिस या सीबीआई वीडियो कॉल पर जमानत या पूछताछ नहीं करती।",
        te: "భారతీయ చట్టంలో 'డిజిటల్ అరెస్ట్' అనే పదం లేదు. పోలీసులు ఎప్పుడూ వాట్సాప్ లేదా స్కైప్ వీడియో కాల్స్‌లో అరెస్ట్ బెదిరింపులు చేయరు."
      },
      redFlag: {
        en: "Caller in uniform demands money to clear narcotics or customs parcel cases.",
        hi: "वर्दी में बैठा व्यक्ति पार्सल या मनी लॉन्ड्रिंग के नाम पर पैसे ट्रांसफर करने की धमकी देता है।",
        te: "యూనిఫాంలో ఉన్న వ్యక్తి మీ పేరుతో డ్రగ్స్ పార్శిల్ వచ్చిందని డబ్బులు డిమాండ్ చేస్తాడు."
      },
      icon: ShieldCheck
    },
    {
      id: 4,
      title: {
        en: "4. Remote Screen Sharing Malware",
        hi: "4. रिमोट स्क्रीन शेयरिंग ऐप्स का खतरा",
        te: "4. స్క్రీన్ షేరింగ్ రిమోట్ యాప్స్ మోసం"
      },
      tag: "DEVICE COMPROMISE",
      summary: {
        en: "Never install AnyDesk, TeamViewer, or RustDesk on the instructions of customer care. Attackers view your OTPs live.",
        hi: "कस्टमर केयर के कहने पर कभी भी एनीडेस्क, टीमव्यूअर या रस्टडेस्क डाउनलोड न करें। धोखेबाज लाइव आपकी स्क्रीन और ओटीपी देख लेते हैं।",
        te: "కస్టమర్ కేర్ పేరుతో AnyDesk లేదా TeamViewer డౌన్‌లోడ్ చేసుకోమని చెబితే ఎప్పుడూ చేయవద్దు. వారు లైవ్‌గా మీ ఓటీపీలు చూస్తారు."
      },
      redFlag: {
        en: "Fake helpline asks you to share a 9-digit remote access code for 'server verification'.",
        hi: "फर्जी सहायता नंबर सर्वर सत्यापन के नाम पर 9 अंकों का रिमोट कोड मांगता है।",
        te: "నకిలీ హెల్ప్‌లైన్ మీ ఫోన్ సరిచేస్తామని 9 అంకెల రిమోట్ యాక్సెస్ కోడ్ అడుగుతుంది."
      },
      icon: Zap
    },
    {
      id: 5,
      title: {
        en: "5. 1930 Helpline Golden Hour Protocol",
        hi: "5. राष्ट्रीय हेल्पलाइन 1930 और गोल्डन ऑवर",
        te: "5. 1930 హెల్ప్‌లైన్ గోల్డెన్ అవర్ నిబంధన"
      },
      tag: "INCIDENT RESPONSE",
      summary: {
        en: "If money is lost, call 1930 within 2-3 hours. Police notify the beneficiary bank to freeze transit accounts before cashout.",
        hi: "पैसे कटने पर 2-3 घंटे के भीतर 1930 पर कॉल करें। पुलिस लाभार्थी बैंक को अलर्ट भेजकर पैसे फ्रीज करवा देती है।",
        te: "మోసం జరిగిన 2-3 గంటల లోపు 1930 కు కాల్ చేయండి. పోలీసులు వెంటనే లబ్ధిదారుడి బ్యాంక్ ఖాతాను ఫ్రీజ్ చేస్తారు."
      },
      redFlag: {
        en: "Delaying reporting beyond 24 hours drastically reduces recovery chance. Act immediately.",
        hi: "शिकायत में देरी होने पर पैसे वापस मिलने की संभावना कम हो जाती है। तुरंत डायल करें।",
        te: "ఫిర్యాదు చేయడంలో ఆలస్యం జరిగితే డబ్బు తిరిగి రావడం కష్టమవుతుంది. వెంటనే కాల్ చేయండి."
      },
      icon: PhoneCall
    }
  ];

  const current = slides[currentIndex];
  const Icon = current.icon;

  const nextSlide = () => setCurrentIndex((prev) => (prev + 1) % slides.length);
  const prevSlide = () => setCurrentIndex((prev) => (prev - 1 + slides.length) % slides.length);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-md animate-fadeIn">
      <div className="relative w-full max-w-md bg-navy-surface border border-border border-t-2 border-t-gold-500 rounded-2xl shadow-2xl p-6 text-ink overflow-hidden">
        {/* Header */}
        <div className="flex items-center justify-between pb-3 border-b border-border">
          <div className="flex items-center gap-2">
            <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-navy text-teal border border-border">
              {current.tag}
            </span>
            <span className="text-xs font-mono text-ink-muted">
              {currentIndex + 1} of {slides.length}
            </span>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 text-ink-muted hover:text-ink rounded-lg hover:bg-navy-raised transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Slide Content */}
        <div className="mt-4 min-h-[220px] flex flex-col justify-between">
          <div>
            <div className="flex items-center gap-3 mb-2">
              <div className="p-2.5 rounded-xl bg-navy border border-border text-teal">
                <Icon className="w-6 h-6" />
              </div>
              <h3 className="text-sm font-bold text-ink font-sans">
                {current.title[language] || current.title.en}
              </h3>
            </div>

            <p className="text-xs text-ink-muted leading-relaxed mt-2.5">
              {current.summary[language] || current.summary.en}
            </p>

            {/* Red Flag Warning Box */}
            <div className="mt-3 p-3 bg-verdict-danger/15 border border-verdict-danger/40 rounded-xl text-xs text-[#FDA4AF]">
              <span className="font-bold font-mono text-[11px] text-verdict-danger block mb-0.5">
                ⚠️ RED FLAG TO SPOT:
              </span>
              <p className="italic text-ink">
                {current.redFlag[language] || current.redFlag.en}
              </p>
            </div>
          </div>
        </div>

        {/* Carousel Navigation Footer */}
        <div className="mt-5 pt-3 border-t border-border flex items-center justify-between">
          <button
            onClick={prevSlide}
            className="p-2 rounded-lg bg-navy-raised hover:bg-border text-ink border border-border transition-colors flex items-center gap-1 text-xs"
          >
            <ChevronLeft className="w-4 h-4" /> Prev
          </button>

          {/* Dots Indicator */}
          <div className="flex items-center gap-1.5">
            {slides.map((_, i) => (
              <span
                key={i}
                onClick={() => setCurrentIndex(i)}
                className={`w-2 h-2 rounded-full cursor-pointer transition-all ${
                  i === currentIndex ? 'w-5 bg-gold-500' : 'bg-[#1E3A5F] hover:bg-[#A9B4CC]'
                }`}
              />
            ))}
          </div>

          <button
            onClick={nextSlide}
            className="p-2 rounded-lg bg-gradient-to-r from-gold-500 to-gold-400 text-navy-deep font-bold shadow-md hover:shadow-glow-gold transition-all flex items-center gap-1 text-xs"
          >
            Next <ChevronRight className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  );
}
