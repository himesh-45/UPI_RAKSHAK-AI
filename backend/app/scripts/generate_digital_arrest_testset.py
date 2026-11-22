import json
import os

SCAM_SCRIPTS = [
    # English Scams (1-20)
    {"id": "da_scam_en_01", "lang": "en", "is_scam": True, "text": "This is Inspector Vijay Rathore from Mumbai Crime Branch. A FedEx parcel sent in your name to Taiwan was intercepted with 16 fake passports and 140 grams of MDMA drugs. You are being placed under Digital Arrest right now. Stay on this Skype video call and do not disconnect."},
    {"id": "da_scam_en_02", "lang": "en", "is_scam": True, "text": "CBI Headquarters New Delhi: Non-bailable arrest warrant issued against you for multi-crore money laundering via 5 unauthorized bank accounts. You must join our virtual interrogation room immediately with camera turned on. Failure to comply will lead to immediate SWAT deployment at your residence."},
    {"id": "da_scam_en_03", "lang": "en", "is_scam": True, "text": "FedEx Customs Interception: Consignment #FX-88912 addressed to your Aadhaar card contains narcotics contraband. Customs has transferred your case to the Narcotics Control Bureau. Connect to our Skype investigation link immediately for verification clearance."},
    {"id": "da_scam_en_04", "lang": "en", "is_scam": True, "text": "Supreme Court Virtual Court Notice: You are booked under PMLA Section 4 for international fund diversion. To prove your funds are clean, transfer your entire bank balance to the official RBI Escrow Verification Account. Once audited, 100% of the deposit will be returned within 2 hours."},
    {"id": "da_scam_en_05", "lang": "en", "is_scam": True, "text": "Delhi Police Cyber Cell: Your mobile number is linked to an illegal child exploitation and money laundering network. We have initiated digital arrest. Keep your webcam active and stay alone in a closed room until our senior inspector finishes taking your statement."},
    {"id": "da_scam_en_06", "lang": "en", "is_scam": True, "text": "Urgent notice from Customs Department Mumbai Airport: A DHL courier booked with your PAN card containing 250 grams of contraband MDMA has been seized. An arrest warrant is being processed. Join our video call immediately for clearance."},
    {"id": "da_scam_en_07", "lang": "en", "is_scam": True, "text": "Enforcement Directorate (ED) Notice: 24 bank accounts registered under your Aadhaar are involved in terror financing. You are under 24-hour virtual detention. Do not speak to anyone or disconnect the line, or local police will enter your premises."},
    {"id": "da_scam_en_08", "lang": "en", "is_scam": True, "text": "Mumbai Police Cyber Division: An illegal SIM card registered in your name was used to threaten high-profile businessmen. You are placed under digital arrest. Stay on this video call and verify all your bank accounts immediately."},
    {"id": "da_scam_en_09", "lang": "en", "is_scam": True, "text": "CBI Crime Branch: Your Aadhaar has been compromised in a 400 crore Hawala racket. You must transfer ₹1,50,000 to the Reserve Bank of India verification treasury account as security deposit to avoid immediate arrest."},
    {"id": "da_scam_en_10", "lang": "en", "is_scam": True, "text": "BlueDart Customs Alert: Your international package destined for Malaysia has been seized for illegal arms and narcotics smuggling. Connect to the cyber police video hearing immediately or face non-bailable warrant."},
    {"id": "da_scam_en_11", "lang": "en", "is_scam": True, "text": "You are under Digital Arrest by Delhi Police. Keep your video camera on at all times. Do not inform any family members as this is a confidential national security investigation under the Official Secrets Act."},
    {"id": "da_scam_en_12", "lang": "en", "is_scam": True, "text": "NCB Interrogation Notice: 500 grams of synthetic drugs were booked in your parcel from Bangkok. To cancel the non-bailable warrant, you must remain on WhatsApp video call and deposit ₹75,000 into the government safe escrow."},
    {"id": "da_scam_en_13", "lang": "en", "is_scam": True, "text": "Interpol National Central Bureau: A Red Corner Notice notice is pending against your Aadhaar identity. Stay on this encrypted video call under virtual custody while our agents inspect your financial assets."},
    {"id": "da_scam_en_14", "lang": "en", "is_scam": True, "text": "CBI Officer Sharma speaking: A FedEx parcel with your passport photocopy was confiscated containing MDMA and forged debit cards. Do not cut the call. Transfer security deposit to the RBI verification account immediately."},
    {"id": "da_scam_en_15", "lang": "en", "is_scam": True, "text": "Customs Investigation Department: Your consignment #CU-40291 has been flagged for money laundering and prohibited narcotics. Join our video conference now to give your statement before the Magistrate."},
    {"id": "da_scam_en_16", "lang": "en", "is_scam": True, "text": "Enforcement Directorate Warning: Bank account freezing orders and arrest warrants are ready. You are in digital arrest. Keep your camera focused on your face and do not mute the microphone."},
    {"id": "da_scam_en_17", "lang": "en", "is_scam": True, "text": "This is Inspector Rajesh from Mumbai Police. Your ICICI account received funds from a terrorist syndicate. Stay in room isolation on this Skype call or face physical arrest within 30 minutes."},
    {"id": "da_scam_en_18", "lang": "en", "is_scam": True, "text": "Supreme Court of India Enforcement Bench: Pay ₹2,00,000 clearance verification bond to our escrow account to secure provisional clearance from the digital arrest warrant issued in case #SC/9921."},
    {"id": "da_scam_en_19", "lang": "en", "is_scam": True, "text": "FedEx Customs Officer: Illegal consignment seized containing 30 counterfeit credit cards and banned narcotics. You are under digital custody. Join the virtual crime cell room now."},
    {"id": "da_scam_en_20", "lang": "en", "is_scam": True, "text": "Delhi Crime Branch: You are under digital arrest. Transfer your assets to the RBI verification portal to avoid property attachment under Section 102 CrPC."},

    # Hindi Scams (21-40)
    {"id": "da_scam_hi_01", "lang": "hi", "is_scam": True, "text": "यह मुंबई क्राइम ब्रांच से इंस्पेक्टर देशमुख हैं। आपके आधार कार्ड से भेजा गया फेडेक्स पार्सल जब्त हुआ है जिसमें 15 फर्जी पासपोर्ट और 200 ग्राम एमडीएमए ड्रग्स मिले हैं। आप तुरंत डिजिटल अरेस्ट में हैं, स्काइप वीडियो कॉल चालू रखें और डिस्कनेक्ट न करें।"},
    {"id": "da_scam_hi_02", "lang": "hi", "is_scam": True, "text": "सीबीआई मुख्यालय नई दिल्ली: मनी लॉन्ड्रिंग के मामले में आपके खिलाफ गैर-जमानती गिरफ्तारी वारंट जारी हुआ है। तुरंत हमारे वर्चुअल कोर्ट रूम में कैमरा चालू करके जुड़ें, अन्यथा आपके घर पर पुलिस टीम भेजी जा रही है।"},
    {"id": "da_scam_hi_03", "lang": "hi", "is_scam": True, "text": "कस्टम्स विभाग मुंबई एयरपोर्ट: आपके नाम का एक पार्सल नारकोटिक्स कंट्रोल ब्यूरो द्वारा जब्त किया गया है। गिरफ्तारी से बचने के लिए तुरंत इस वीडियो कॉल पर उपस्थित हों।"},
    {"id": "da_scam_hi_04", "lang": "hi", "is_scam": True, "text": "सुप्रीम कोर्ट वेरिफिकेशन आदेश: आपके बैंक खातों की जांच के लिए आपको अपनी जमा पूंजी आरबीआई के सुरक्षित सत्यापन खाते में ट्रांसफर करनी होगी। जांच पूरी होते ही पैसे वापस कर दिए जाएंगे।"},
    {"id": "da_scam_hi_05", "lang": "hi", "is_scam": True, "text": "दिल्ली पुलिस साइबर सेल: आप डिजिटल अरेस्ट के तहत हैं। कमरे का दरवाजा बंद रखें और स्काइप वीडियो कॉल पर उपस्थित रहें। किसी भी परिवार के सदस्य को इसकी सूचना न दें।"},
    {"id": "da_scam_hi_06", "lang": "hi", "is_scam": True, "text": "डीएचएल कूरियर कस्टम्स: आपके पार्सल में अवैध सिम कार्ड और ड्रग्स पाए गए हैं। आपके खिलाफ एफआईआर दर्ज हो चुकी है। तुरंत वीडियो जांच में शामिल हों।"},
    {"id": "da_scam_hi_07", "lang": "hi", "is_scam": True, "text": "प्रवर्तन निदेशालय (ईडी): आपके आधार से जुड़े 12 अवैध बैंक खातों में करोड़ों का संदिग्ध लेन-देन हुआ है। आप वर्चुअल कस्टडी में हैं, कॉल मत काटना।"},
    {"id": "da_scam_hi_08", "lang": "hi", "is_scam": True, "text": "मुंबई पुलिस से इंस्पेक्टर पाटिल: आपके नाम से जारी सिम से आतंकी गतिविधियों को अंजाम दिया गया है। डिजिटल अरेस्ट लागू है, कैमरा ऑन रखें।"},
    {"id": "da_scam_hi_09", "lang": "hi", "is_scam": True, "text": "सीबीआई जांच अधिकारी: 350 करोड़ के हवाला मामले में आपका नाम आया है। तुरंत ₹1,00,000 सरकारी एस्क्रो खाते में ट्रांसफर करें अन्यथा घर पर दबिश दी जाएगी।"},
    {"id": "da_scam_hi_10", "lang": "hi", "is_scam": True, "text": "ब्लूडार्ट पार्सल नारकोटिक्स जब्ती: आपके पते पर आया हुआ पार्सल ड्रग्स तस्करी के आरोप में जब्त हुआ है। गैर-जमानती वारंट से बचने के लिए तुरंत वीडियो सुनवाई में जुड़ें।"},
    {"id": "da_scam_hi_11", "lang": "hi", "is_scam": True, "text": "दिल्ली क्राइम ब्रांच: आप डिजिटल अरेस्ट में हैं। कैमरा अपने चेहरे पर रखें और माइक्रोफोन ऑन रखें। किसी से बात करना गैर-कानूनी होगा।"},
    {"id": "da_scam_hi_12", "lang": "hi", "is_scam": True, "text": "एनसीबी नारकोटिक्स अधिकारी: आपके पार्सल से नशीला पदार्थ बरामद हुआ है। जमानत के लिए आपको ₹50,000 की रिफंडेबल राशि आरबीआई खाते में डालनी होगी।"},
    {"id": "da_scam_hi_13", "lang": "hi", "is_scam": True, "text": "इंटरपोल नोटिस: आपके आधार नंबर से अंतरराष्ट्रीय अपराध लिंक पाया गया है। डिजिटल कस्टडी में रहते हुए अपने सभी बैंक विवरण सत्यापित कराएं।"},
    {"id": "da_scam_hi_14", "lang": "hi", "is_scam": True, "text": "सीबीआई अधिकारी: फेडेक्स कूरियर में 20 फर्जी पासपोर्ट और एमडीएमए मिला है। कॉल बिल्कुल डिस्कनेक्ट न करें, तुरंत सत्यापन राशि जमा करें।"},
    {"id": "da_scam_hi_15", "lang": "hi", "is_scam": True, "text": "कस्टम्स जांच: पार्सल #CU-9812 में मनी लॉन्ड्रिंग की रकम मिली है। वर्चुअल कोर्ट में मजिस्ट्रेट के सामने बयान दर्ज कराने के लिए तुरंत जुड़ें।"},
    {"id": "da_scam_hi_16", "lang": "hi", "is_scam": True, "text": "प्रवर्तन निदेशालय: संपत्ति जब्ती और गिरफ्तारी वारंट तैयार है। आप डिजिटल अरेस्ट में हैं, स्काइप पर लगातार रहें।"},
    {"id": "da_scam_hi_17", "lang": "hi", "is_scam": True, "text": "मुंबई पुलिस साइबर सेल: आपके खाते में आतंकी फंडिंग का पैसा आया है। 2 घंटे तक वीडियो कॉल पर रहें और किसी बाहरी व्यक्ति से संपर्क न करें।"},
    {"id": "da_scam_hi_18", "lang": "hi", "is_scam": True, "text": "सुप्रीम कोर्ट एनफोर्समेंट: डिजिटल अरेस्ट वारंट को रद्द कराने के लिए ₹1,50,000 की क्लियरेंस जमानत राशि सरकारी ट्रेजरी खाते में जमा करें।"},
    {"id": "da_scam_hi_19", "lang": "hi", "is_scam": True, "text": "फेडेक्स कस्टम्स अधिकारी: आपके कंसाइनमेंट में प्रतिबंधित हथियार और ड्रग्स मिले हैं। आप डिजिटल हिरासत में हैं, वीडियो लिंक खोलें।"},
    {"id": "da_scam_hi_20", "lang": "hi", "is_scam": True, "text": "दिल्ली पुलिस: डिजिटल अरेस्ट के तहत अपनी संपत्ति का सत्यापन कराने के लिए रिजर्व बैंक के सुरक्षित खाते में राशि ट्रांसफर करें।"},

    # Telugu Scams (41-60)
    {"id": "da_scam_te_01", "lang": "te", "is_scam": True, "text": "ఇది ముంబై క్రైమ్ బ్రాంచ్ నుండి ఇన్‌స్పెక్టర్ రాథోడ్. మీ ఆధార్ కార్డు పేరుతో పంపిన ఫెడెక్స్ పార్శిల్ లో 16 నకిలీ పాస్‌పోర్టులు మరియు 150 గ్రాముల ఎండీఎంఏ డ్రగ్స్ దొరికాయి. మిమ్మల్ని డిజిటల్ అరెస్ట్ చేస్తున్నాము. స్కైప్ వీడియో కాల్ లోనే ఉండండి, కాల్ కట్ చేయవద్దు."},
    {"id": "da_scam_te_02", "lang": "te", "is_scam": True, "text": "సీబీఐ ప్రధాన కార్యాలయం: మనీ లాండరింగ్ కేసులో మీపై నాన్-బెయిలబుల్ అరెస్ట్ వారెంట్ జారీ చేయబడింది. వెంటనే వీడియో కాల్ లో కెమెరా ఆన్ చేసి వర్చువల్ కోర్టుకు హాజరుకావాలి."},
    {"id": "da_scam_te_03", "lang": "te", "is_scam": True, "text": "కస్టమ్స్ డిపార్ట్‌మెంట్ ముంబై: మీ పేరుతో ఉన్న కొరియర్ లో గంజాయి మరియు నార్కోటిక్స్ సీజ్ చేయబడ్డాయి. అరెస్ట్ కాకుండా ఉండాలంటే వెంటనే వీడియో కాల్ లో మాట్లాడండి."},
    {"id": "da_scam_te_04", "lang": "te", "is_scam": True, "text": "సుప్రీం కోర్టు ఆర్డర్: మీ బ్యాంక్ ఖాతాల ధృవీకరణ కోసం మొత్తం డబ్బును ఆర్బీఐ సేఫ్ ఎస్క్రో ఖాతాకు బదిలీ చేయాలి. విచారణ తర్వాత మీ డబ్బు వెనక్కి వస్తుంది."},
    {"id": "da_scam_te_05", "lang": "te", "is_scam": True, "text": "ఢిల్లీ పోలీస్ సైబర్ క్రైమ్: మీరు డిజిటల్ అరెస్ట్ లో ఉన్నారు. గదిలో ఒంటరిగా ఉంటూ స్కైప్ వీడియో కాల్ లోనే ఉండండి, ఎవరితోనూ మాట్లాడవద్దు."},
    {"id": "da_scam_te_06", "lang": "te", "is_scam": True, "text": "డీహెచ్ఎల్ కస్టమ్స్ సీజ్: మీ పార్శిల్ లో అక్రమ సిమ్ కార్డులు మరియు డ్రగ్స్ లభించాయి. తక్షణ అరెస్ట్ నివారించడానికి వీడియో విచారణలో చేరండి."},
    {"id": "da_scam_te_07", "lang": "te", "is_scam": True, "text": "ఈడీ (ఎన్‌ఫోర్స్‌మెంట్ డైరెక్టరేట్): మీ ఖాతాల ద్వారా ఉగ్రవాద నిధులు వెళ్లినట్లు తేలింది. మీరు వర్చువల్ కస్టడీలో ఉన్నారు, కాల్ కట్ చేయవద్దు."},
    {"id": "da_scam_te_08", "lang": "te", "is_scam": True, "text": "ముంబై పోలీస్: మీ ఆధార్‌తో నకిలీ సిమ్ తీసుకుని నేరాలు చేశారు. డిజిటల్ అరెస్ట్ అమలులో ఉంది, కెమెరా నిరంతరం ఆన్ లో ఉండాలి."},
    {"id": "da_scam_te_09", "lang": "te", "is_scam": True, "text": "సీబీఐ ఆఫీసర్: హవాలా కేసులో మీ పేరు ఉంది. వెంటనే ₹1,00,000 ఆర్బీఐ సెక్యూరిటీ ఖాతాకు బదిలీ చేయాలి లేకపోతే స్థానిక పోలీసులు ఇంటికి వస్తారు."},
    {"id": "da_scam_te_10", "lang": "te", "is_scam": True, "text": "బ్లూడార్ట్ నార్కోటిక్స్ సీజ్: డ్రగ్స్ కేసులో అరెస్ట్ వారెంట్ రాకుండా ఉండాలంటే వెంటనే మా వీడియో కాన్ఫరెన్స్‌లో చేరండి."},
    {"id": "da_scam_te_11", "lang": "te", "is_scam": True, "text": "ఢిల్లీ క్రైమ్ బ్రాంచ్: మీరు డిజిటల్ అరెస్ట్ లో ఉన్నారు. మైక్రోఫోన్ ఆన్ లో ఉంచి ముఖాన్ని కెమెరాలో చూపించండి."},
    {"id": "da_scam_te_12", "lang": "te", "is_scam": True, "text": "ఎన్‌సీబీ నార్కోటిక్స్ అధికారి: బెయిల్ డిపాజిట్ కోసం ₹50,000 ప్రభుత్వ ఎస్క్రో ఖాతాకు పంపితేనే కేసు రద్దవుతుంది."},
    {"id": "da_scam_te_13", "lang": "te", "is_scam": True, "text": "ఇంటర్‌పోల్ నోటీసు: అంతర్జాతీయ నేరాలతో మీ ఖాతా లింక్ అయింది. డిజిటల్ కస్టడీలో ఉంటూ ఆస్తులను వెరిఫై చేయించండి."},
    {"id": "da_scam_te_14", "lang": "te", "is_scam": True, "text": "సీబీఐ ఇన్‌స్పెక్టర్: ఫెడెక్స్ పార్శిల్ లో ఎండీఎంఏ దొరికింది. కాల్ కట్ చేయకుండా వెంటనే క్లియరెన్స్ డిపాజిట్ పంపండి."},
    {"id": "da_scam_te_15", "lang": "te", "is_scam": True, "text": "కస్టమ్స్ ఇన్వెస్టిగేషన్: మనీ లాండరింగ్ ఆరోపణలపై మేజిస్ట్రేట్ ముందు వీడియో ద్వారా వాంగ్మూలం ఇవ్వడానికి వెంటనే చేరండి."},
    {"id": "da_scam_te_16", "lang": "te", "is_scam": True, "text": "ఎన్‌ఫోర్స్‌మెంట్ డైరెక్టరేట్: ఆస్తుల జప్తు వారెంట్ సిద్ధంగా ఉంది. మీరు డిజిటల్ అరెస్ట్ లో ఉన్నారు, స్కైప్ లోనే ఉండండి."},
    {"id": "da_scam_te_17", "lang": "te", "is_scam": True, "text": "ముంబై పోలీస్ సైబర్ సెల్: మీ ఖాతాలోకి వచ్చిన డబ్బుపై విచారణ జరుగుతోంది. వీడియో కాల్ లోనే ఉంటూ సమాచారం ఇవ్వండి."},
    {"id": "da_scam_te_18", "lang": "te", "is_scam": True, "text": "సుప్రీం కోర్టు ఎన్‌ఫోర్స్‌మెంట్: డిజిటల్ అరెస్ట్ రద్దు కావడానికి ₹2,00,000 క్లియరెన్స్ బాండ్ ఆర్బీఐ ఖాతాకు బదిలీ చేయండి."},
    {"id": "da_scam_te_19", "lang": "te", "is_scam": True, "text": "ఫెడెక్స్ కస్టమ్స్ అధికారి: నిషేధిత మందుల పార్శిల్ పట్టుబడింది. మీరు డిజిటల్ అదుపులో ఉన్నారు, వీడియో లింక్ ఓపెన్ చేయండి."},
    {"id": "da_scam_te_20", "lang": "te", "is_scam": True, "text": "ఢిల్లీ పోలీసులు: డిజిటల్ అరెస్ట్ కింద మీ ఆస్తుల పరిశీలనకు రిజర్వ్ బ్యాంక్ ఖాతాకు డబ్బు పంపండి."},

    # Hinglish & Multi-Agency Scams (61-65)
    {"id": "da_scam_hing_01", "lang": "hi", "is_scam": True, "text": "CBI Officer here. Aapka FedEx parcel Mumbai airport par pakda gaya hai with 140 grams MDMA and illegal SIM cards. You are placed under digital arrest right now. Stay on Skype video call camera on."},
    {"id": "da_scam_hing_02", "lang": "hi", "is_scam": True, "text": "Mumbai Police cyber department se bol rahe hain. Aapke naam par non-bailable warrant nikla hai for money laundering. Video call cut mat karna, virtual room mein remain present."},
    {"id": "da_scam_hing_03", "lang": "hi", "is_scam": True, "text": "Customs officer: Consignment seized with narcotics. Case handed to NCB. Transfer ₹1,20,000 verification deposit to RBI escrow account for clean chit."},
    {"id": "da_scam_hing_04", "lang": "hi", "is_scam": True, "text": "Delhi Crime Branch: You are under 24 hour digital arrest. Keep webcam active, room ka door lock rakhein and kisi ko mat batayein."},
    {"id": "da_scam_hing_05", "lang": "hi", "is_scam": True, "text": "ED office New Delhi: Multi-crore scam mein aapka account freeze hoga. Warrant cancel karne ke liye government escrow account mein clearance amount bhejo."}
]

LEGITIMATE_SCRIPTS = [
    # Legitimate Couriers (1-15)
    {"id": "legit_courier_01", "lang": "en", "is_scam": False, "text": "FedEx Express: Your shipment with tracking number FX-78219482 is out for delivery today with courier executive Ramesh. Track live on fedex.com."},
    {"id": "legit_courier_02", "lang": "en", "is_scam": False, "text": "BlueDart: Consignment #BL-992147 has arrived at the Gurgaon delivery center. Expected delivery by 6:00 PM today."},
    {"id": "legit_courier_03", "lang": "en", "is_scam": False, "text": "DHL Express: Package #DHL-128472 was delivered to your building reception and signed for by S. Kumar. Thank you for choosing DHL."},
    {"id": "legit_courier_04", "lang": "en", "is_scam": False, "text": "FedEx Alert: Delivery attempt for tracking #49281729 was unsuccessful because the premises were closed. Rescheduled for tomorrow."},
    {"id": "legit_courier_05", "lang": "en", "is_scam": False, "text": "India Post Speed Post: Article #EK9921847IN dispatched from Mumbai GPO to Bangalore Sorting Hub."},
    {"id": "legit_courier_hi_01", "lang": "hi", "is_scam": False, "text": "ब्लूडार्ट कूरियर: आपका पार्सल #BL-88219 आज शाम 5 बजे तक आपके पते पर डिलीवर कर दिया जाएगा। डिलीवरी एजेंट: राजेश कुमार।"},
    {"id": "legit_courier_hi_02", "lang": "hi", "is_scam": False, "text": "फेडेक्स इंडिया: ट्रैकिंग संख्या FX-992819 का पार्सल सफलतापूर्वक आपके गार्ड को सौंप दिया गया है। धन्यवाद।"},
    {"id": "legit_courier_hi_03", "lang": "hi", "is_scam": False, "text": "डीएचएल एक्सप्रेस: बारिश के कारण डिलीवरी में थोड़ा विलंब हो सकता है। अपनी शिपमेंट dhl.com पर ट्रैक करें।"},
    {"id": "legit_courier_te_01", "lang": "te", "is_scam": False, "text": "బ్లూడార్ట్: మీ కొరియర్ కన్సైన్‌మెంట్ #BL-49120 ఈరోజు సాయంత్రం లోగా డెలివరీ చేయబడుతుంది. లైవ్ ట్రాకింగ్ కోసం bluedart.com సందర్శించండి."},
    {"id": "legit_courier_te_02", "lang": "te", "is_scam": False, "text": "ఫెడెక్స్: మీ పార్శిల్ #FX-99120 మీ గేట్ సెక్యూరిటీ వద్ద అందించబడింది. డెలివరీ సంతకం: కె. రాజు."},
    {"id": "legit_courier_te_03", "lang": "te", "is_scam": False, "text": "ఇండియా పోస్ట్ స్పీడ్ పోస్ట్: మీ ఆర్టికల్ విజయవాడ హెడ్ పోస్ట్ ఆఫీస్ నుండి బయలుదేరింది."},
    {"id": "legit_courier_12", "lang": "en", "is_scam": False, "text": "Shiprocket tracking update: Your Nykaa beauty order has reached the local hub in Pune."},
    {"id": "legit_courier_13", "lang": "en", "is_scam": False, "text": "Delhivery: Package with AWB 88192849102 is arriving today. Share delivery PIN 4821 only when handed over."},
    {"id": "legit_courier_14", "lang": "en", "is_scam": False, "text": "Amazon Logistics: Your order of boAt headphones is out for delivery with associate Amit."},
    {"id": "legit_courier_15", "lang": "en", "is_scam": False, "text": "Flipkart Wishmaster is arriving with your parcel #FMPP-88219. Total payable amount ₹0.00 (Prepaid)."},

    # Legitimate Bank & Official Notifications (16-25)
    {"id": "legit_bank_01", "lang": "en", "is_scam": False, "text": "State Bank of India: Your savings account KYC is scheduled for periodic review. Please visit your nearest branch with original Aadhaar and PAN."},
    {"id": "legit_bank_02", "lang": "en", "is_scam": False, "text": "HDFC Bank: Rs 2,400 debited from account **8192 for insurance premium payment. Available balance Rs 45,900."},
    {"id": "legit_bank_hi_01", "lang": "hi", "is_scam": False, "text": "एसबीआई बैंक: आपकी शाखा में केवाईसी अपडेशन का कार्य जारी है। कृपया अपनी नजदीकी शाखा में जाकर दस्तावेज जमा करें।"},
    {"id": "legit_bank_te_01", "lang": "te", "is_scam": False, "text": "హెచ్‌డీఎఫ్‌సీ బ్యాంక్: మీ ఖాతా నుండి రూ. 1,500 డెబిట్ చేయబడింది. ఎవరితోనూ మీ ఓటీపీ లేదా పిన్ పంచుకోవద్దు."},
    {"id": "legit_bank_05", "lang": "en", "is_scam": False, "text": "ICICI Bank Alert: New credit card dispatched via BlueDart with tracking #BL-881920."},

    # Legitimate Legal Summons / Awareness (26-42)
    {"id": "legit_legal_01", "lang": "en", "is_scam": False, "text": "District and Sessions Court Saket New Delhi: Summons for witness testimony in Civil Suit #CS/102/2024. Please appear in Courtroom 302 on 15-Dec-2026 at 10:30 AM."},
    {"id": "legit_legal_02", "lang": "en", "is_scam": False, "text": "High Court Registry Notice: Certified copy of the order in Appeal No. 441/2025 is ready for collection at the filing counter."},
    {"id": "legit_awareness_01", "lang": "en", "is_scam": False, "text": "Mumbai Police Advisory: Beware of digital arrest scam calls! Cyber criminals posing as CBI or FedEx threaten arrest via Skype. Law enforcement never conducts video arrests. Call 1930 immediately."},
    {"id": "legit_awareness_02", "lang": "en", "is_scam": False, "text": "Cyber Dost (MHA Official): Digital arrest is a scam! No government agency or court arrests citizens over video call or demands money in RBI accounts. Report calls at cybercrime.gov.in."},
    {"id": "legit_awareness_hi_01", "lang": "hi", "is_scam": False, "text": "दिल्ली पुलिस जनहित जारी चेतावनी: डिजिटल अरेस्ट से सावधान रहें! पुलिस कभी भी व्हाट्सएप या स्काइप वीडियो कॉल पर जांच नहीं करती और न ही पैसे मांगती है। हेल्पलाइन 1930 पर फोन करें।"},
    {"id": "legit_awareness_hi_02", "lang": "hi", "is_scam": False, "text": "साइबर दोस्त अलर्ट: डिजिटल अरेस्ट एक नया ऑनलाइन फ्रॉड है। यदि कोई खुद को सीबीआई या पुलिस बताकर वीडियो कॉल पर डराए तो तुरंत कॉल काटें।"},
    {"id": "legit_awareness_te_01", "lang": "te", "is_scam": False, "text": "తెలంగాణ సైబర్ సెల్ హెచ్చరిక: డిజిటల్ అరెస్ట్ అనేది ఒక మోసం. పోలీసులు ఎప్పుడూ వీడియో కాల్స్ లో విచారణ చేయరు లేదా డబ్బు అడగరు. వెంటనే 1930 కు ఫిర్యాదు చేయండి."},
    {"id": "legit_awareness_te_02", "lang": "te", "is_scam": False, "text": "ఆంధ్రప్రదేశ్ పోలీస్ సలహా: సీబీఐ లేదా కస్టమ్స్ పేరుతో వచ్చే వీడియో కాల్స్ నమ్మవద్దు. ఎలాంటి డబ్బు బదిలీ చేయవద్దు."},
    {"id": "legit_legal_07", "lang": "en", "is_scam": False, "text": "Consumer Disputes Redressal Commission: Your complaint #CC/492/2026 has been registered. Hearing date posted on e-daakhil.nic.in."},
    {"id": "legit_legal_08", "lang": "en", "is_scam": False, "text": "National Legal Services Authority: Free legal aid helpline 15100 is available 24x7 for all citizens in need of legal counsel."},
    {"id": "legit_legal_09", "lang": "en", "is_scam": False, "text": "Income Tax Department Notice: Intimation under Section 143(1) for AY 2025-26 has been sent to your registered email. Check incometax.gov.in."},
    {"id": "legit_legal_10", "lang": "en", "is_scam": False, "text": "Passport Seva Kendra: Your police verification appointment is scheduled at Indiranagar Police Station on Thursday 11:00 AM with original documents."},
    {"id": "legit_legal_11", "lang": "en", "is_scam": False, "text": "Ministry of Communications: Telemarketer registration renewal acknowledgment #TR-4912 approved on saralsanchar.gov.in."},
    {"id": "legit_legal_12", "lang": "en", "is_scam": False, "text": "EPFO Member alert: Your provident fund claim #PF-88219 has been settled and credited to your verified bank account."},
    {"id": "legit_legal_13", "lang": "en", "is_scam": False, "text": "Indian Railways IRCTC: Train 12952 confirmation. PNR 2849182910 coach B4 seat 21. Have a safe journey."},
    {"id": "legit_legal_14", "lang": "en", "is_scam": False, "text": "BSNL Customer Care: Bill for landline connection 022-2819284 is ₹650. Pay via bsnl.co.in by 20th of this month."},
    {"id": "legit_legal_15", "lang": "en", "is_scam": False, "text": "Aadhaar authentication OTP for DigiLocker login is 819204. Valid for 10 minutes. Do not share with anyone."}
]

ALL_ITEMS = SCAM_SCRIPTS + LEGITIMATE_SCRIPTS

def main():
    target_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "digital_arrest_testset.json")
    with open(target_path, "w", encoding="utf-8") as f:
        json.dump(ALL_ITEMS, f, ensure_ascii=False, indent=2)
    print(f"Generated {len(ALL_ITEMS)} digital arrest benchmark items ({len(SCAM_SCRIPTS)} scams, {len(LEGITIMATE_SCRIPTS)} legitimate) -> {target_path}")

if __name__ == "__main__":
    main()
