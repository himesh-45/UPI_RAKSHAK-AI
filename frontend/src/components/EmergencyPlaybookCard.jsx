import React, { useState } from 'react';
import { PhoneCall, ShieldAlert, Clock, ChevronDown, ChevronUp, ExternalLink, Camera, Lock } from 'lucide-react';

export default function EmergencyPlaybookCard({ language = 'en', onOpen1930Modal = null }) {
  const [bankAccordionOpen, setBankAccordionOpen] = useState(false);

  const bankHelplines = [
    { name: "State Bank of India (SBI)", num: "1800 1234 / 1800 2100", sms: "BLOCK to 567676" },
    { name: "HDFC Bank", num: "1800 202 6161 / 1800 1600", sms: "Via Mobile App" },
    { name: "ICICI Bank", num: "1800 1080", sms: "BLOCK <last 4> to 9215676766" },
    { name: "Axis Bank", num: "1800 419 5959", sms: "BLOCK to 5676782" },
    { name: "Punjab National Bank (PNB)", num: "1800 180 2222", sms: "BLOCK to 5607040" },
    { name: "Canara Bank", num: "1800 425 0018", sms: "CAN HOTLIST to 9266623333" },
    { name: "Bank of Baroda (BoB)", num: "1800 5700 / 1800 5000", sms: "BLOCK to 8422009988" },
    { name: "Union Bank of India", num: "1800 22 22 44", sms: "UBLOCK to 9223008486" },
    { name: "Kotak Mahindra Bank", num: "1860 266 2666", sms: "Via Kotak811 App" },
    { name: "IndusInd Bank", num: "1800 209 0061", sms: "Via IndusMobile" }
  ];

  const content = {
    en: {
      bannerTitle: "ACT WITHIN THE GOLDEN HOUR (FIRST 2-3 HOURS)",
      bannerSub: "Rapid reporting triggers inter-bank CFCFRMS freezing to halt stolen money before withdrawal.",
      tile1Title: "1. Dial 1930 Cyber Helpline",
      tile1Desc: "Toll-free national hotline. Have your 12-digit UTR and scammer details ready.",
      tile1Action: "Call 1930 Now",
      tile2Title: "2. Report Online at cybercrime.gov.in",
      tile2Desc: "Lodge formal complaint to obtain official police Acknowledgement Number.",
      tile2Action: "Open Portal",
      tile3Title: "3. Freeze Bank & Block UPI",
      tile3Desc: "Hotlist debit card & suspend netbanking immediately with your bank.",
      tile3Toggle: "View Top 10 Bank Hotlines",
      tile4Title: "4. Preserve Incident Evidence",
      tile4Desc: "Take unedited screenshots of debit SMS, UPI transaction receipt, and scammer chat."
    },
    hi: {
      bannerTitle: "गोल्डन ऑवर में तुरंत कार्रवाई करें (पहले 2-3 घंटे)",
      bannerSub: "जल्द शिकायत दर्ज करने से बैंक फ्रॉड की रकम को निकासी से पहले फ्रीज कर सकते हैं।",
      tile1Title: "1. तुरंत 1930 हेल्पलाइन डायल करें",
      tile1Desc: "टोल-फ्री राष्ट्रीय हेल्पलाइन। 12 अंकों का UTR नंबर और बैंक विवरण तैयार रखें।",
      tile1Action: "1930 पर कॉल करें",
      tile2Title: "2. cybercrime.gov.in पर ऑनलाइन रिपोर्ट करें",
      tile2Desc: "आधिकारिक शिकायत पावती संख्या (Acknowledgement) प्राप्त करने के लिए पोर्टल पर जाएं।",
      tile2Action: "पोर्टल खोलें",
      tile3Title: "3. बैंक खाता व यूपीआई ब्लॉक करें",
      tile3Desc: "डेबिट कार्ड को हॉटलिस्ट करें और तुरंत इंटरनेट बैंकिंग बंद करवाएं।",
      tile3Toggle: "शीर्ष 10 बैंकों के हेल्पलाइन नंबर",
      tile4Title: "4. सभी साक्ष्य सुरक्षित रखें",
      tile4Desc: "बैंक एसएमएस, पेमेंट रसीद और स्कैमर के व्हाट्सएप संदेशों के स्क्रीनशॉट लें।"
    },
    te: {
      bannerTitle: "గోల్డెన్ అవర్‌లో తక్షణమే స్పందించండి (మొదటి 2-3 గంటలు)",
      bannerSub: "వెంటనే ఫిర్యాదు చేస్తే సైబర్ పోలీసులు బ్యాంకుల ద్వారా దొంగిలించబడిన డబ్బును ఫ్రీజ్ చేయగలరు.",
      tile1Title: "1. 1930 జాతీయ హెల్ప్‌లైన్‌కు కాల్ చేయండి",
      tile1Desc: "12 అంకెల UTR నంబర్ మరియు మోసగాడి వివరాలు సిద్ధంగా ఉంచుకోండి.",
      tile1Action: "1930 కు కాల్ చేయండి",
      tile2Title: "2. cybercrime.gov.in లో ఆన్‌లైన్ ఫిర్యాదు చేయండి",
      tile2Desc: "పోలీస్ ఎక్నాలెడ్జ్‌మెంట్ నంబర్ కోసం పోర్టల్‌లో అధికారిక ఫిర్యాదు నమోదు చేయండి.",
      tile2Action: "పోర్టల్ ఓపెన్ చేయండి",
      tile3Title: "3. బ్యాంక్ ఖాతా & యూపీఐ నిలిపివేయండి",
      tile3Desc: "మీ బ్యాంక్‌కు కాల్ చేసి కార్డులు మరియు నెట్ బ్యాంకింగ్‌ను వెంటనే ఫ్రీజ్ చేయించండి.",
      tile3Toggle: "టాప్ 10 బ్యాంకుల హెల్ప్‌లైన్ నంబర్లు",
      tile4Title: "4. ఆధారాలను భద్రపరచండి",
      tile4Desc: "డెబిట్ ఎస్ఎంఎస్, లావాదేవీ రసీదు మరియు చాట్ స్క్రీన్‌షాట్లను సిద్ధంగా ఉంచండి."
    }
  };

  const text = content[language] || content.en;

  return (
    <div className="mt-3 p-4 bg-navy-surface/95 border-2 border-verdict-danger/50 rounded-2xl shadow-2xl text-ink">
      {/* Golden Hour Urgency Banner */}
      <div className="flex items-center gap-3 p-3 bg-verdict-danger/15 border border-verdict-danger/40 rounded-xl mb-4">
        <Clock className="w-6 h-6 text-verdict-danger shrink-0 animate-pulse" />
        <div>
          <h4 className="text-xs font-bold text-rose-600 dark:text-rose-300 tracking-wider font-mono">
            {text.bannerTitle}
          </h4>
          <p className="text-[11px] text-rose-600 dark:text-rose-300/90 mt-0.5">
            {text.bannerSub}
          </p>
        </div>
      </div>

      {/* 4 Action Tiles */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
        {/* Tile 1: 1930 */}
        <div className="p-3 bg-navy border border-verdict-danger/30 rounded-xl flex flex-col justify-between">
          <div>
            <div className="flex items-center gap-2 text-xs font-bold text-verdict-danger">
              <PhoneCall className="w-4 h-4" />
              <span>{text.tile1Title}</span>
            </div>
            <p className="text-[11px] text-ink-muted mt-1 leading-relaxed">
              {text.tile1Desc}
            </p>
          </div>
          <div className="mt-3 flex items-center gap-2">
            <a
              href="tel:1930"
              className="flex-1 py-1.5 px-3 rounded-lg bg-verdict-danger hover:bg-[#E11D48] text-white text-xs font-bold text-center flex items-center justify-center gap-1.5 transition-colors shadow-md shadow-rose-950/50"
            >
              <PhoneCall className="w-3.5 h-3.5" /> {text.tile1Action}
            </a>
            {onOpen1930Modal && (
              <button
                onClick={onOpen1930Modal}
                className="py-1.5 px-2.5 rounded-lg bg-navy-raised hover:bg-border text-ink text-xs font-medium border border-border transition-colors"
                title="Pre-fill 1930 incident sheet"
              >
                Pre-fill
              </button>
            )}
          </div>
        </div>

        {/* Tile 2: cybercrime.gov.in */}
        <div className="p-3 bg-navy border border-teal/30 rounded-xl flex flex-col justify-between">
          <div>
            <div className="flex items-center gap-2 text-xs font-bold text-teal">
              <ExternalLink className="w-4 h-4" />
              <span>{text.tile2Title}</span>
            </div>
            <p className="text-[11px] text-ink-muted mt-1 leading-relaxed">
              {text.tile2Desc}
            </p>
          </div>
          <div className="mt-3">
            <a
              href="https://cybercrime.gov.in"
              target="_blank"
              rel="noopener noreferrer"
              className="w-full py-1.5 px-3 rounded-lg bg-teal hover:bg-teal text-navy-deep text-xs font-bold text-center flex items-center justify-center gap-1.5 transition-colors"
            >
              <ExternalLink className="w-3.5 h-3.5" /> {text.tile2Action}
            </a>
          </div>
        </div>

        {/* Tile 3: Bank Freeze */}
        <div className="p-3 bg-navy border border-border rounded-xl flex flex-col justify-between">
          <div>
            <div className="flex items-center gap-2 text-xs font-bold text-gold-400">
              <Lock className="w-4 h-4" />
              <span>{text.tile3Title}</span>
            </div>
            <p className="text-[11px] text-ink-muted mt-1 leading-relaxed">
              {text.tile3Desc}
            </p>
          </div>
          <button
            onClick={() => setBankAccordionOpen(!bankAccordionOpen)}
            className="mt-3 w-full py-1.5 px-2 rounded-lg bg-navy-raised hover:bg-border text-ink-muted text-xs font-medium border border-border flex items-center justify-between transition-colors"
          >
            <span>{text.tile3Toggle}</span>
            {bankAccordionOpen ? <ChevronUp className="w-3.5 h-3.5" /> : <ChevronDown className="w-3.5 h-3.5" />}
          </button>
        </div>

        {/* Tile 4: Evidence */}
        <div className="p-3 bg-navy border border-border rounded-xl flex flex-col justify-between">
          <div>
            <div className="flex items-center gap-2 text-xs font-bold text-teal">
              <Camera className="w-4 h-4" />
              <span>{text.tile4Title}</span>
            </div>
            <p className="text-[11px] text-ink-muted mt-1 leading-relaxed">
              {text.tile4Desc}
            </p>
          </div>
          <div className="mt-3 text-[11px] text-gold-400 font-mono bg-navy-raised p-1.5 rounded border border-gold-500/30 text-center">
            📸 Keep uncropped screenshots safe
          </div>
        </div>
      </div>

      {/* Accordion List for Top 10 Banks */}
      {bankAccordionOpen && (
        <div className="mt-3.5 p-3 bg-navy border border-border rounded-xl max-h-56 overflow-y-auto space-y-2 animate-fadeIn text-xs">
          <span className="text-[11px] font-semibold text-ink-muted uppercase font-mono block mb-1">
            Official 24x7 Bank Emergency Hotlines
          </span>
          {bankHelplines.map((b, i) => (
            <div key={i} className="flex items-center justify-between p-2 rounded-lg bg-navy-surface border border-border">
              <div>
                <span className="font-semibold text-ink block">{b.name}</span>
                <span className="text-[10px] text-ink-muted font-mono">{b.sms}</span>
              </div>
              <span className="text-xs font-mono font-bold text-teal">{b.num}</span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
