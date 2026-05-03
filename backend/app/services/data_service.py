"""
Service for retrieving election-related data
"""
from typing import List, Dict, Any
from app.models.schemas import Step, TimelinePhase, FAQItem, QuizQuestion


class DataService:
    """Service for election data"""

    @staticmethod
    def get_quiz_questions(language: str = "en") -> List[QuizQuestion]:
        """Get election awareness quiz questions for a language."""
        quiz_map = {
            "en": [
                QuizQuestion(
                    question_id=1,
                    question="What is the minimum age to vote in India?",
                    options=["16 years", "18 years", "21 years", "25 years"],
                    correct_option_index=1,
                    explanation="An Indian citizen can vote after turning 18 and registering in the electoral roll."
                ),
                QuizQuestion(
                    question_id=2,
                    question="What does NOTA mean in voting?",
                    options=[
                        "Name Of The Applicant",
                        "None Of The Above",
                        "Notice Of The Act",
                        "National Option To Approve"
                    ],
                    correct_option_index=1,
                    explanation="NOTA means None Of The Above and lets voters reject all listed candidates."
                ),
                QuizQuestion(
                    question_id=3,
                    question="Which document is commonly used to identify a voter at the polling booth?",
                    options=["Library card", "Voter ID (EPIC)", "PAN card only", "Birth certificate"],
                    correct_option_index=1,
                    explanation="Voter ID (EPIC) is the primary election identity document, along with other approved IDs."
                ),
                QuizQuestion(
                    question_id=4,
                    question="Who conducts elections in India?",
                    options=["Supreme Court", "State Police", "Election Commission of India", "Parliament Secretariat"],
                    correct_option_index=2,
                    explanation="The Election Commission of India supervises and administers elections."
                ),
                QuizQuestion(
                    question_id=5,
                    question="What is the purpose of indelible ink on voting day?",
                    options=[
                        "For identity decoration",
                        "To allow multiple votes",
                        "To prevent duplicate voting",
                        "To mark party preference"
                    ],
                    correct_option_index=2,
                    explanation="Indelible ink helps ensure one person votes only once."
                ),
            ],
            "hi": [
                QuizQuestion(
                    question_id=1,
                    question="भारत में मतदान की न्यूनतम आयु क्या है?",
                    options=["16 वर्ष", "18 वर्ष", "21 वर्ष", "25 वर्ष"],
                    correct_option_index=1,
                    explanation="भारत में 18 वर्ष की आयु पूरी होने के बाद और मतदाता सूची में नाम होने पर मतदान किया जा सकता है।"
                )
            ],
            "mr": [
                QuizQuestion(
                    question_id=1,
                    question="भारतात मतदानासाठी किमान वय किती आहे?",
                    options=["16 वर्षे", "18 वर्षे", "21 वर्षे", "25 वर्षे"],
                    correct_option_index=1,
                    explanation="भारतात 18 वर्षे पूर्ण झाल्यावर आणि मतदार यादीत नाव असल्यास मतदान करता येते."
                )
            ],
        }

        return quiz_map.get(language, quiz_map["en"])

    @staticmethod
    def get_faqs(language: str = "en") -> List[FAQItem]:
        """Get fallback FAQs for a language."""
        faq_map = {
            "en": [
                FAQItem(
                    question="What is EVM?",
                    answer="EVM stands for Electronic Voting Machine. It is a machine used to record votes electronically.",
                    category="voting",
                ),
                FAQItem(
                    question="What is NOTA?",
                    answer="NOTA stands for None Of The Above. It lets voters choose none of the listed candidates.",
                    category="voting",
                ),
                FAQItem(
                    question="Who can vote?",
                    answer="An Indian citizen who is 18 years or older and registered as a voter can vote.",
                    category="eligibility",
                ),
            ],
            "hi": [
                FAQItem(
                    question="EVM क्या है?",
                    answer="EVM का मतलब Electronic Voting Machine है। इसका उपयोग वोट दर्ज करने के लिए किया जाता है।",
                    category="voting",
                ),
            ],
            "mr": [
                FAQItem(
                    question="EVM म्हणजे काय?",
                    answer="EVM म्हणजे Electronic Voting Machine. याचा वापर मतदान नोंदवण्यासाठी केला जातो.",
                    category="voting",
                ),
            ],
        }

        return faq_map.get(language, faq_map["en"])
    
    @staticmethod
    def get_voting_steps() -> List[Step]:
        """Get voting process steps"""
        steps = [
            Step(
                step_number=1,
                title="Voter Registration",
                description="Register yourself as a voter",
                details="Visit your nearest election office with proof of age and address. Fill Form 6. You can also register online through your state election website."
            ),
            Step(
                step_number=2,
                title="Get Voter ID (EPIC)",
                description="Receive your Voter ID card",
                details="After registration, you will receive your Voter ID card (EPIC) by mail. This is your official identification for voting."
            ),
            Step(
                step_number=3,
                title="Find Your Polling Booth",
                description="Locate your polling station",
                details="Check the election website with your Voter ID to find your assigned polling booth. You will also receive a Polling Booth Slip by post."
            ),
            Step(
                step_number=4,
                title="Voting Day",
                description="Cast your vote",
                details="Visit your polling booth on voting day. Bring valid ID. The voting process takes 2-3 minutes. Vote on the EVM or VVPAT."
            ),
            Step(
                step_number=5,
                title="Ink Mark",
                description="Get your finger marked",
                details="After voting, your finger will be marked with indelible ink to prevent duplicate voting."
            ),
            Step(
                step_number=6,
                title="Vote Counting",
                description="Votes are counted",
                details="After voting day, all votes are counted and the results are declared within the specified period."
            ),
        ]
        return steps
    
    @staticmethod
    def get_election_timeline() -> List[TimelinePhase]:
        """Get election phases and timeline"""
        phases = [
            TimelinePhase(
                phase="Announcement",
                description="Election Commission announces election dates",
                duration="Announced by EC",
                details="The Chief Election Commissioner announces the dates for elections, polling schedule, and voting dates."
            ),
            TimelinePhase(
                phase="Notification & Nomination",
                description="Nomination period begins",
                duration="7-10 days",
                details="Election Notification is issued. Candidates can file their nominations. Last date for nomination filing is announced."
            ),
            TimelinePhase(
                phase="Scrutiny & Withdrawal",
                description="Nominations are scrutinized",
                duration="2-3 days",
                details="Election officials verify nominations. Candidates can withdraw if they wish."
            ),
            TimelinePhase(
                phase="Campaign",
                description="Election campaign period",
                duration="14-20 days",
                details="Candidates campaign to seek votes. Campaign ends 48 hours before polling in an area."
            ),
            TimelinePhase(
                phase="Voting Day",
                description="Citizens cast their votes",
                duration="Single day or multiple phases",
                details="Voting is conducted at polling stations. Voters have the entire day to vote between 7 AM - 6 PM."
            ),
            TimelinePhase(
                phase="Counting & Results",
                description="Votes are counted and results declared",
                duration="1-2 days after voting",
                details="Votes are counted by election officials. Results are declared and winners announced officially."
            ),
        ]
        return phases
    
    @staticmethod
    def get_first_time_voter_guide() -> Dict[str, Any]:
        """Get guide specifically for first-time voters"""
        return {
            "title": "First-Time Voter's Guide",
            "description": "Simple guide for new voters",
            "sections": [
                {
                    "title": "Before Voting Day",
                    "tips": [
                        "Make sure you are registered as a voter",
                        "Check your Voter ID or polling booth location",
                        "Keep a valid ID with you (Voter ID, Aadhaar, etc.)",
                        "Wear light-colored clothes as per EVM guidelines",
                        "Note down your polling booth location"
                    ]
                },
                {
                    "title": "On Voting Day",
                    "tips": [
                        "Arrive early to avoid crowds",
                        "Bring valid ID (Voter ID, Aadhaar, Driving License, Passport, Ration Card)",
                        "Be prepared for queues",
                        "Listen to polling officials",
                        "Take time to understand the EVM"
                    ]
                },
                {
                    "title": "Inside the Polling Booth",
                    "tips": [
                        "You will be taken to a booth with an EVM",
                        "Your finger will be marked with ink",
                        "You will press the button next to your chosen candidate",
                        "Press the button clearly to cast your vote",
                        "The EVM will show confirmation",
                        "You can also choose NOTA (None of the Above) if you wish"
                    ]
                },
                {
                    "title": "Important Points",
                    "tips": [
                        "Voting is your right and responsibility",
                        "You have only one vote",
                        "Voting is secret and anonymous",
                        "No one can force you to vote for anyone",
                        "Taking photos inside booth is NOT allowed",
                        "Booth officials will help you if confused"
                    ]
                }
            ],
            "common_questions": [
                {
                    "q": "What if I don't have a Voter ID?",
                    "a": "You can bring any valid ID like Aadhaar, Driving License, or Passport."
                },
                {
                    "q": "Can I take someone with me?",
                    "a": "You must vote alone. Your companion must wait outside the booth."
                },
                {
                    "q": "What if I make a mistake?",
                    "a": "You cannot change your vote. Vote carefully and deliberately."
                },
                {
                    "q": "How long does voting take?",
                    "a": "Usually 2-3 minutes if you know who to vote for. Booth officials help if needed."
                },
            ]
        }
