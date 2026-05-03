"""
Chatbot service using Google Gemini API
"""
import google.generativeai as genai
from typing import Optional, Dict, Any
import asyncio
from app.config import settings


class ChatbotService:
    """Service for handling chatbot interactions with Gemini API"""
    
    def __init__(self):
        """Initialize the chatbot service"""
        self.model_name = settings.GEMINI_MODEL
        self.api_key = settings.GEMINI_API_KEY
        
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel(self.model_name)
        else:
            self.model = None
    
    def generate_prompt(
        self,
        user_input: str,
        intent: str,
        language: str = "en",
        is_first_time_voter: bool = False
    ) -> str:
        """
        Generate a system prompt for Gemini API
        
        Args:
            user_input: User's question
            intent: Detected intent
            language: Language code (en, hi, mr)
            is_first_time_voter: Is it a first-time voter
            
        Returns:
            Complete prompt for Gemini
        """
        system_message = """You are a helpful, unbiased Indian Election Assistant designed to help citizens understand the voting process, election timeline, and voting procedures. 

IMPORTANT RULES:
1. NEVER show any political bias
2. NEVER promote any party or candidate
3. ONLY provide factual, educational information
4. Use simple English for easy understanding
5. Keep sentences short and clear
6. Provide step-by-step explanations when needed
7. Be respectful and helpful
8. If you don't know something, say "I don't have specific information about this. Please contact your local election office."

CONTEXT ABOUT INDIAN ELECTIONS:
- Voting age: 18 years and above
- Valid ID: Voter ID, Aadhaar, Driving License, Passport, Ration Card
- EVMs are used for voting
- NOTA (None of the Above) is available as an option
- Election Commission of India administers elections
- Elections follow the Constitution of India"""
        
        if is_first_time_voter:
            system_message += "\n\nTARGET AUDIENCE: First-time voters. Use simple explanations and real-life examples."
        
        language_instruction = ""
        if language == "hi":
            language_instruction = "\nPlease respond in Hindi."
        elif language == "mr":
            language_instruction = "\nPlease respond in Marathi."
        
        full_prompt = f"""{system_message}{language_instruction}

Intent: {intent}
User Question: {user_input}

Please provide a clear, helpful, and unbiased response. Keep it concise (2-3 sentences for short answers, max 150 words for detailed answers)."""
        
        return full_prompt
    
    async def get_response(
        self,
        user_input: str,
        intent: str,
        language: str = "en",
        is_first_time_voter: bool = False
    ) -> Dict[str, Any]:
        """
        Get response from Gemini API
        
        Args:
            user_input: User's question
            intent: Detected intent
            language: Language code
            is_first_time_voter: Is it a first-time voter
            
        Returns:
            Dictionary with response data
        """
        # Return fallback response if API key not configured
        if not self.api_key or not self.model:
            return self._get_fallback_response(intent, language, user_input)
        
        try:
            prompt = self.generate_prompt(
                user_input=user_input,
                intent=intent,
                language=language,
                is_first_time_voter=is_first_time_voter
            )
            
            # Call Gemini API
            response = await asyncio.to_thread(
                self.model.generate_content,
                prompt
            )
            
            if response and response.text:
                return {
                    "response": response.text,
                    "source": "gemini",
                    "success": True
                }
            else:
                return self._get_fallback_response(intent, language, user_input)
                
        except Exception as e:
            print(f"Error calling Gemini API: {str(e)}")
            return self._get_fallback_response(intent, language, user_input)
    
    async def translate_text(
        self,
        text: str,
        target_language: str = "en",
        source_language: str = "en"
    ) -> Dict[str, Any]:
        """
        Translate text using Gemini API
        
        Args:
            text: Text to translate
            target_language: Target language code (en, hi, mr)
            source_language: Source language code (default: en)
            
        Returns:
            Dictionary with translated text
        """
        if not self.api_key or not self.model:
            return {
                "translated_text": text,
                "source": "fallback",
                "success": False
            }
        
        # Map language codes to language names
        language_map = {
            "en": "English",
            "hi": "Hindi",
            "mr": "Marathi"
        }
        
        source_lang = language_map.get(source_language, "English")
        target_lang = language_map.get(target_language, "English")
        
        prompt = f"""Translate the following text from {source_lang} to {target_lang}. 
Provide ONLY the translated text, nothing else.

Text to translate:
{text}"""
        
        try:
            response = await asyncio.to_thread(
                self.model.generate_content,
                prompt
            )
            
            if response and response.text:
                return {
                    "translated_text": response.text.strip(),
                    "source": "gemini",
                    "success": True
                }
            else:
                return {
                    "translated_text": text,
                    "source": "fallback",
                    "success": False
                }
                
        except Exception as e:
            print(f"Error translating text: {str(e)}")
            return {
                "translated_text": text,
                "source": "fallback",
                "success": False
            }
    
    def _get_fallback_response(
        self,
        intent: str,
        language: str = "en",
        user_input: str = ""
    ) -> Dict[str, Any]:
        """Get fallback response when API is not available"""

        contextual_faq_response = self._get_contextual_faq_response(user_input, language)
        
        fallback_responses = {
            "steps": {
                "en": "Voting Steps:\n1. Register as a voter\n2. Receive Voter ID\n3. Find your polling booth\n4. Visit booth on voting day\n5. Vote on EVM\n6. Your vote is counted\nPlease visit your local election office or website for more details.",
                "hi": "मतदान की प्रक्रिया:\n1. मतदाता के रूप में पंजीकरण करें\n2. वोटर आईडी प्राप्त करें\n3. अपना मतदान केंद्र खोजें\n4. मतदान के दिन केंद्र पर जाएं\n5. ईवीएम पर वोट करें\n6. आपके वोट की गिनती की जाती है",
                "mr": "मतदान प्रक्रिया:\n1. मतदार म्हणून नोंदणी करा\n2. मतदार आयडी प्राप्त करा\n3. तुमचे मतदान केंद्र शोधा\n4. मतदान दिवसाला केंद्रावर जा\n5. ईव्हीएमवर मत द्या\n6. तुमच्या मताची गणना केली जाते"
            },
            "timeline": {
                "en": "Election Timeline:\n1. Announcement - Election dates announced\n2. Nomination - Candidates file nominations\n3. Campaign - Election campaign period\n4. Voting Day - Citizens cast their votes\n5. Counting - Votes are counted\n6. Results - Winners declared\nFor exact dates, visit your state election website.",
                "hi": "चुनाव समयसूची:\n1. घोषणा - चुनाव की तारीख की घोषणा\n2. नामांकन - उम्मीदवार नामांकन दाखिल करते हैं\n3. प्रचार - चुनाव प्रचार अवधि\n4. मतदान दिवस - नागरिक अपने वोट डालते हैं\n5. गिनती - वोटों की गिनती\n6. परिणाम - विजेताओं की घोषणा",
                "mr": "निवडणूक वेळापत्रक:\n1. घोषणा - निवडणूक तारखांची घोषणा\n2. नामांकन - उमेदवार नामांकन दाखल करतात\n3. प्रचार - निवडणूक प्रचार काल\n4. मतदान दिवस - नागरिक मतदान करतात\n5. गणना - मतांची गणना\n6. परिणाम - विजेत्यांची घोषणा"
            },
            "faq": {
                "en": contextual_faq_response["en"],
                "hi": contextual_faq_response["hi"],
                "mr": contextual_faq_response["mr"]
            },
            "first_time_voter": {
                "en": "If you are a first-time voter: verify your name in the voter list, carry a valid ID, reach your polling booth on time, and follow officer instructions. You will vote privately on an EVM and can choose NOTA if needed. I can also explain each step in simple detail.",
                "hi": "अगर आप पहली बार वोट दे रहे हैं, तो मतदाता सूची में अपना नाम जांचें, वैध पहचान पत्र साथ रखें, समय पर मतदान केंद्र पहुंचें और अधिकारियों के निर्देशों का पालन करें। आप ईवीएम पर गोपनीय रूप से वोट देंगे और चाहें तो नोटा चुन सकते हैं। मैं हर चरण सरल तरीके से समझा सकता हूं।",
                "mr": "जर तुम्ही प्रथमच मतदान करत असाल, तर मतदार यादीत तुमचे नाव तपासा, वैध ओळखपत्र सोबत ठेवा, वेळेवर मतदान केंद्रावर या आणि अधिकाऱ्यांच्या सूचनांचे पालन करा. तुम्ही ईव्हीएमवर गोपनीय पद्धतीने मतदान कराल आणि हवे असल्यास नोटा निवडू शकता. मी प्रत्येक टप्पा सोप्या भाषेत समजावू शकतो."
            },
            "location": {
                "en": "To find your polling booth, check the official Election Commission portal or your voter slip and search using EPIC number or registered details. If you share your district/state, I can guide you on the exact lookup steps.",
                "hi": "अपना मतदान केंद्र खोजने के लिए चुनाव आयोग की आधिकारिक वेबसाइट या अपनी वोटर स्लिप देखें और EPIC नंबर या पंजीकृत विवरण से खोज करें। अगर आप अपना जिला/राज्य बताएं, तो मैं सही खोज प्रक्रिया बता सकता हूं।",
                "mr": "तुमचे मतदान केंद्र शोधण्यासाठी निवडणूक आयोगाची अधिकृत वेबसाइट किंवा तुमची मतदार पर्ची तपासा आणि EPIC क्रमांक किंवा नोंदणीकृत तपशील वापरून शोधा. तुम्ही जिल्हा/राज्य सांगितल्यास मी अचूक शोध पद्धत सांगू शकतो."
            },
            "general": {
                "en": "I can help you understand election processes, voting steps, timelines, and FAQs. What would you like to know?",
                "hi": "मैं आपको चुनाव प्रक्रिया, मतदान चरण, समयसूची और FAQ समझने में मदद कर सकता हूं। आप क्या जानना चाहते हैं?",
                "mr": "मी तुम्हाला निवडणूक प्रक्रिया, मतदान चरण, वेळापत्रक आणि FAQ समजण्यात मदत करू शकतो. तुम्हाला काय जाणून घ्यायचे आहे?"
            }
        }
        
        response_text = fallback_responses.get(intent, {}).get(
            language,
            fallback_responses.get(intent, {}).get(
                "en",
                fallback_responses["general"].get(language, fallback_responses["general"]["en"])
            )
        )
        
        return {
            "response": response_text,
            "source": "fallback",
            "success": True,
            "note": "API key not configured. Using fallback response."
        }

    def _get_contextual_faq_response(self, user_input: str, language: str = "en") -> Dict[str, str]:
        """Return a topic-specific FAQ fallback based on the user's question."""
        query = user_input.lower()

        if any(word in query for word in ["eligible", "eligibility", "who can vote", "can vote", "age"]):
            return {
                "en": "Eligibility to vote in India: you must be an Indian citizen, at least 18 years old on the qualifying date, and registered in the electoral roll of your constituency. You should carry a valid ID (such as Voter ID/EPIC, Aadhaar, Passport, or Driving License) to vote at your assigned booth.",
                "hi": "भारत में वोट देने की पात्रता: आप भारतीय नागरिक हों, आपकी आयु कम से कम 18 वर्ष हो, और आपका नाम आपके निर्वाचन क्षेत्र की मतदाता सूची में दर्ज हो। मतदान के लिए मान्य पहचान पत्र (जैसे वोटर आईडी/EPIC, आधार, पासपोर्ट, या ड्राइविंग लाइसेंस) साथ रखें।",
                "mr": "भारतात मतदानासाठी पात्रता: तुम्ही भारतीय नागरिक असणे, किमान 18 वर्षे वय असणे आणि तुमचे नाव मतदार यादीत नोंदलेले असणे आवश्यक आहे. मतदानासाठी वैध ओळखपत्र (उदा. मतदार ओळखपत्र/EPIC, आधार, पासपोर्ट किंवा ड्रायव्हिंग लायसन्स) सोबत ठेवा."
            }

        if "evm" in query:
            return {
                "en": "EVM (Electronic Voting Machine) is used to cast votes electronically at polling booths. You press the button next to your chosen candidate, and the vote is securely recorded. In many booths, VVPAT also shows a short confirmation slip for transparency.",
                "hi": "EVM (Electronic Voting Machine) का उपयोग मतदान केंद्र पर इलेक्ट्रॉनिक वोट डालने के लिए होता है। आप अपनी पसंद के उम्मीदवार के सामने बटन दबाते हैं और आपका वोट सुरक्षित रूप से दर्ज होता है। कई केंद्रों पर पारदर्शिता के लिए VVPAT में पुष्टि पर्ची भी दिखती है।",
                "mr": "EVM (Electronic Voting Machine) चा वापर मतदान केंद्रावर इलेक्ट्रॉनिक मतदानासाठी केला जातो. तुम्ही निवडलेल्या उमेदवारासमोरील बटण दाबता आणि तुमचे मत सुरक्षितरीत्या नोंदवले जाते. अनेक केंद्रांवर पारदर्शकतेसाठी VVPAT पुष्टी पर्ची दाखवते."
            }

        if "nota" in query:
            return {
                "en": "NOTA means None Of The Above. If you do not want to vote for any listed candidate, you can choose NOTA on the EVM. Your vote is still counted as participation, but it does not transfer to any candidate.",
                "hi": "NOTA का मतलब None Of The Above है। यदि आप सूचीबद्ध किसी भी उम्मीदवार को वोट नहीं देना चाहते, तो EVM पर NOTA चुन सकते हैं। आपका वोट भागीदारी के रूप में दर्ज होता है, लेकिन किसी उम्मीदवार को नहीं जाता।",
                "mr": "NOTA म्हणजे None Of The Above. तुम्हाला यादीतील कोणत्याही उमेदवाराला मत द्यायचे नसेल तर EVM वर NOTA निवडू शकता. तुमचे मत सहभाग म्हणून नोंदले जाते, पण कोणत्याही उमेदवाराकडे जात नाही."
            }

        if any(word in query for word in ["register", "registration", "voter id", "epic", "document", "documents"]):
            return {
                "en": "To register as a voter, submit Form 6 online (NVSP/state election portal) or at your local election office. After verification, your name is added to the electoral roll and you receive EPIC (Voter ID). Keep identity and address proof ready during registration.",
                "hi": "मतदाता पंजीकरण के लिए Form 6 ऑनलाइन (NVSP/राज्य चुनाव पोर्टल) या स्थानीय चुनाव कार्यालय में जमा करें। सत्यापन के बाद आपका नाम मतदाता सूची में जुड़ता है और EPIC (वोटर आईडी) जारी होता है। पंजीकरण के समय पहचान और पते के दस्तावेज तैयार रखें।",
                "mr": "मतदार नोंदणीसाठी Form 6 ऑनलाइन (NVSP/राज्य निवडणूक पोर्टल) किंवा स्थानिक निवडणूक कार्यालयात जमा करा. पडताळणीनंतर तुमचे नाव मतदार यादीत जोडले जाते आणि EPIC (मतदार ओळखपत्र) मिळते. नोंदणीवेळी ओळख आणि पत्त्याचा पुरावा तयार ठेवा."
            }

        if any(word in query for word in ["how election works", "election works", "election process", "how voting works", "what is voting"]):
            return {
                "en": "Elections in India usually work in stages: announcement of schedule, nomination of candidates, campaign period, polling day, vote counting, and declaration of results. Voters cast secret ballots at assigned booths using EVM, and the Election Commission supervises the full process.",
                "hi": "भारत में चुनाव आमतौर पर चरणों में होते हैं: कार्यक्रम की घोषणा, उम्मीदवारों का नामांकन, प्रचार अवधि, मतदान दिवस, मतगणना और परिणाम घोषणा। मतदाता अपने निर्धारित केंद्र पर EVM से गुप्त मतदान करते हैं और पूरी प्रक्रिया चुनाव आयोग देखता है।",
                "mr": "भारतात निवडणूक साधारणपणे टप्प्यांत होते: वेळापत्रक घोषणा, उमेदवार नामांकन, प्रचार कालावधी, मतदान दिवस, मतमोजणी आणि निकाल जाहीर. मतदार नियुक्त केंद्रावर EVM द्वारे गुप्त मतदान करतात आणि संपूर्ण प्रक्रिया निवडणूक आयोगाच्या देखरेखीखाली होते."
            }

        return {
            "en": "Voting is the process where eligible citizens choose their representatives by casting a vote. In India, voting is done through EVM at your assigned polling booth, and voters aged 18+ can participate with valid ID. Ask me if you want details on EVM, NOTA, voter registration, or required documents.",
            "hi": "मतदान वह प्रक्रिया है जिसमें योग्य नागरिक अपने प्रतिनिधि चुनने के लिए वोट डालते हैं। भारत में मतदान आपके निर्धारित मतदान केंद्र पर ईवीएम के माध्यम से होता है, और 18+ आयु के मतदाता वैध पहचान पत्र के साथ भाग ले सकते हैं। आप ईवीएम, नोटा, पंजीकरण या आवश्यक दस्तावेजों के बारे में भी पूछ सकते हैं।",
            "mr": "मतदान ही अशी प्रक्रिया आहे ज्यात पात्र नागरिक आपले प्रतिनिधी निवडण्यासाठी मत देतात. भारतात मतदान आपल्या नियुक्त मतदान केंद्रावर ईव्हीएमद्वारे केले जाते आणि 18+ वयोगटातील मतदार वैध ओळखपत्रासह मतदान करू शकतात. तुम्ही ईव्हीएम, नोटा, नोंदणी किंवा आवश्यक कागदपत्रांबद्दलही विचारू शकता."
        }
