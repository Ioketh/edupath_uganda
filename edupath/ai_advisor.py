"""
EduPath Uganda AI Advisor - Enhanced Career Guidance System
"""
import json
import re
from typing import Dict, List, Any

class UgandanEducationAdvisor:
    """AI Advisor specialized in Ugandan Education System"""
    
    def __init__(self):
        self.uganda_universities = {
            'Makerere University': {
                'location': 'Kampala',
                'type': 'Public',
                'strengths': ['Medicine', 'Engineering', 'Law', 'Business', 'ICT'],
                'entry_requirements': '2 principal passes minimum, specific subjects vary by program'
            },
            'Mbarara University (MUST)': {
                'location': 'Mbarara',
                'type': 'Public',
                'strengths': ['Medicine', 'Nursing', 'Computer Science', 'Biomedical Sciences'],
                'entry_requirements': '2 principal passes, strong preference for science subjects'
            },
            'Gulu University': {
                'location': 'Gulu',
                'type': 'Public',
                'strengths': ['Medicine', 'Agriculture', 'Education', 'Business'],
                'entry_requirements': '2 principal passes, growing medical school'
            },
            'Kyambogo University': {
                'location': 'Kampala',
                'type': 'Public',
                'strengths': ['Education', 'Engineering', 'Vocational Studies', 'Fine Art'],
                'entry_requirements': '2 principal passes, flexible entry for vocational courses'
            },
            'Uganda Christian University (UCU)': {
                'location': 'Mukono',
                'type': 'Private',
                'strengths': ['Law', 'Journalism', 'Business', 'Social Sciences'],
                'entry_requirements': '2 principal passes, religious institution'
            },
            'Kampala International University (KIU)': {
                'location': 'Kampala',
                'type': 'Private',
                'strengths': ['Medicine', 'Law', 'Engineering', 'Business'],
                'entry_requirements': '2 principal passes, flexible admission'
            }
        }
        
        self.job_market_2025 = {
            'high_demand': {
                'Healthcare': {
                    'roles': ['Doctor', 'Nurse', 'Pharmacist', 'Radiographer'],
                    'salaries': 'UGX 2.8M - 20M/month',
                    'growth': 'High - Critical shortage nationwide'
                },
                'ICT/Tech': {
                    'roles': ['Software Developer', 'Data Scientist', 'Cybersecurity Analyst'],
                    'salaries': 'UGX 2M - 20M/month',
                    'growth': 'Very High - Remote work opportunities'
                },
                'Engineering': {
                    'roles': ['Civil Engineer', 'Electrical Engineer', 'Petroleum Engineer'],
                    'salaries': 'UGX 2.5M - 15M/month',
                    'growth': 'High - Infrastructure and oil projects'
                },
                'Agriculture': {
                    'roles': ['Agribusiness Manager', 'Agronomist', 'Agricultural Engineer'],
                    'salaries': 'UGX 1.5M - 8M/month',
                    'growth': 'Growing - Commercial farming expansion'
                }
            },
            'emerging_sectors': {
                'Renewable Energy': 'Solar technicians, Energy engineers - UGX 2M-8M',
                'Digital Marketing': 'Content creators, SEO specialists - UGX 1.5M-6M',
                'Fintech': 'Mobile money specialists, Payment systems - UGX 2.5M-10M',
                'Oil & Gas': 'Petroleum engineers, Geologists - UGX 5M-25M (Tilenga project)'
            }
        }
        
        self.combination_career_paths = {
            'PCB': ['Medicine', 'Pharmacy', 'Nursing', 'Veterinary Medicine', 'Biomedical Sciences'],
            'PCM': ['Engineering', 'Computer Science', 'Architecture', 'Petroleum Engineering'],
            'BCM': ['Biomedical Engineering', 'Biotechnology', 'Computer Science'],
            'HEG': ['Law', 'Business', 'Economics', 'Public Administration'],
            'HEL': ['Law', 'Journalism', 'Social Work', 'Teaching'],
            'MEG': ['Business', 'Economics', 'Statistics', 'Actuarial Science'],
            'BCA': ['Agriculture', 'Environmental Science', 'Veterinary Medicine']
        }
    
    def get_career_advice(self, query: str, context: Dict = None) -> Dict:
        """Get personalized career advice based on query and context"""
        query_lower = query.lower()
        
        # Check for combination advice
        if any(word in query_lower for word in ['combination', 'choose', 'which', 'subject']):
            return self._combination_advice(query_lower, context)
        
        # Check for career advice
        elif any(word in query_lower for word in ['career', 'job', 'work', 'salary', 'pay']):
            return self._career_advice(query_lower)
        
        # Check for university advice
        elif any(word in query_lower for word in ['university', 'uni', 'college', 'admission']):
            return self._university_advice(query_lower)
        
        # Check for scholarship advice
        elif 'scholarship' in query_lower:
            return self._scholarship_advice()
        
        # Check for struggling students
        elif any(word in query_lower for word in ['struggling', 'difficult', 'hard', 'failing']):
            return self._struggling_student_advice()
        
        # General advice
        else:
            return self._general_advice()
    
    def _combination_advice(self, query: str, context: Dict) -> Dict:
        """Provide combination selection advice"""
        advice = []
        
        # Check if user has grades context
        if context and context.get('grades'):
            grades = context['grades']
            # Find best combination based on grades
            best_combo = None
            best_score = 0
            
            for combo, career_list in self.combination_career_paths.items():
                score = self._score_combo_for_grades(combo, grades)
                if score > best_score:
                    best_score = score
                    best_combo = combo
            
            if best_combo:
                advice.append(f"🎓 **Based on your grades, {best_combo} is your strongest combination!**")
                advice.append(f"With {best_combo}, you can pursue: {', '.join(self.combination_career_paths[best_combo][:3])}...")
        
        # General combination advice
        advice.append("\n📚 **Popular A-Level Combinations in Uganda:**")
        advice.append("• **PCB** (Physics, Chemistry, Biology) → Medicine, Pharmacy, Nursing")
        advice.append("• **PCM** (Physics, Chemistry, Mathematics) → Engineering, Computer Science")
        advice.append("• **HEG** (History, Economics, Geography) → Law, Business, Economics")
        advice.append("• **MEG** (Mathematics, Economics, Geography) → Business, Actuarial Science")
        
        # Subsidiary rules
        advice.append("\n⚠️ **Important PUJAB Rules:**")
        advice.append("• If you take Principal Mathematics → Must take Sub-ICT")
        advice.append("• If you take Economics without Mathematics → Must take Sub-Math")
        advice.append("• Science combinations without Math → Must take Sub-Math")
        
        return {
            'message': '\n\n'.join(advice),
            'type': 'combination_advice'
        }
    
    def _career_advice(self, query: str) -> Dict:
        """Provide career market advice"""
        advice = []
        
        advice.append("💼 **Uganda Job Market 2025 - High Demand Careers**\n")
        
        for sector, info in self.job_market_2025['high_demand'].items():
            advice.append(f"**{sector}:**")
            advice.append(f"  • Roles: {', '.join(info['roles'])}")
            advice.append(f"  • Salary: {info['salaries']}")
            advice.append(f"  • Growth: {info['growth']}\n")
        
        advice.append("🚀 **Emerging Sectors with High Potential:**\n")
        for sector, details in self.job_market_2025['emerging_sectors'].items():
            advice.append(f"• **{sector}**: {details}")
        
        # Salary guide
        advice.append("\n💰 **Average Salary Guide (UGX/month):**")
        advice.append("• Entry Level (0-2 years): UGX 1M - 3M")
        advice.append("• Mid Level (3-5 years): UGX 3M - 7M")
        advice.append("• Senior Level (5+ years): UGX 7M - 20M")
        advice.append("• Executive Level: UGX 20M+")
        
        return {
            'message': '\n'.join(advice),
            'type': 'career_advice'
        }
    
    def _university_advice(self, query: str) -> Dict:
        """Provide university admission advice"""
        advice = []
        
        advice.append("🏛️ **Uganda Universities & Programmes**\n")
        
        for uni, info in self.uganda_universities.items():
            advice.append(f"**{uni}** ({info['type']})")
            advice.append(f"  • Location: {info['location']}")
            advice.append(f"  • Strengths: {', '.join(info['strengths'])}")
            advice.append(f"  • Requirements: {info['entry_requirements']}\n")
        
        advice.append("📝 **General Admission Requirements:**")
        advice.append("• Minimum 2 Principal passes at A-Level")
        advice.append("• Relevant subjects for chosen course")
        advice.append("• Good performance in relevant O-Level subjects")
        advice.append("• Government sponsorship requires 12-20 points depending on course")
        
        return {
            'message': '\n'.join(advice),
            'type': 'university_advice'
        }
    
    def _scholarship_advice(self) -> Dict:
        """Provide scholarship information"""
        advice = [
            "🎓 **Scholarships Available for Ugandan Students**\n",
            
            "**Government Scholarships:**",
            "• **Makerere Government Sponsorship (PUJAB)** - Based on UACE points",
            "• **State House Scholarships** - Merit-based, covers fees + allowance",
            "• **District Local Government** - Check with your district education office\n",
            
            "**Private Scholarships:**",
            "• **Mastercard Foundation Scholars** - Full tuition at Makerere and other African universities",
            "• **Equity Leaders Program** - Full university scholarships",
            "• **KCB Scholarship Program** - For students from disadvantaged backgrounds\n",
            
            "**International Scholarships:**",
            "• **DAAD Scholarships** - For science and engineering students (Germany)",
            "• **Chevening Scholarships** - For future leaders (UK)",
            "• **Chinese Government Scholarships (CSC)** - Various fields",
            "• **Commonwealth Scholarships** - For Master's and PhD\n",
            
            "**Oil & Gas Sector:**",
            "• **Total Energies Uganda** - Petroleum and engineering scholarships",
            "• **CNOOC Uganda** - Engineering scholarships",
            "• **EACOP Community Scholarships** - For local communities\n",
            
            "**Tips for Winning Scholarships:**",
            "✓ Maintain excellent grades (15+ points at A-Level)",
            "✓ Develop leadership skills through extracurriculars",
            "✓ Participate in community service",
            "✓ Start applications early (6-12 months before study)",
            "✓ Write compelling personal statements"
        ]
        
        return {
            'message': '\n'.join(advice),
            'type': 'scholarship_advice'
        }
    
    def _struggling_student_advice(self) -> Dict:
        """Provide advice for struggling students"""
        advice = [
            "💪 **You're Not Alone - Here Are Your Options**\n",
            
            "**Alternative Pathways to Success:**",
            "1. **UBTEB (Technical & Business Education)** - Certificates and Diplomas in practical fields",
            "2. **DIT (Directorate of Industrial Training)** - Craft certificates in Electrical, Plumbing, etc.",
            "3. **TVET Institutions** - Hands-on skills that lead to immediate employment",
            "4. **Certificate → Diploma → Degree** - A valid, less competitive path to university\n",
            
            "**If You're Struggling Academically:**",
            "• Talk to your teachers - they want to help you succeed",
            "• Join study groups - learning with others can make difficult subjects easier",
            "• Focus on your strongest subjects - you don't need to excel in everything",
            "• Consider repeating S.4 if you're confident you can improve\n",
            
            "**Remember:** Many successful people struggled in school but found their path through persistence and the right guidance. Your worth isn't defined by your exam results!\n",
            
            "**Next Steps:**",
            "1. Identify which subjects you enjoy and do well in",
            "2. Talk to your school guidance counselor",
            "3. Explore vocational options at institutions near you",
            "4. Consider career paths that match your strengths, not just traditional degrees"
        ]
        
        return {
            'message': '\n'.join(advice),
            'type': 'struggling_advice'
        }
    
    def _general_advice(self) -> Dict:
        """Provide general educational advice"""
        advice = [
            "👋 **Welcome to EduPath Uganda - Your Career Guide!**\n",
            
            "I can help you with:",
            "✅ **A-Level Combination Advice** - Which subjects match your career goals",
            "✅ **University Admissions** - Requirements for Makerere, Kyambogo, Gulu, and more",
            "✅ **Career Guidance** - Job market trends and salary expectations in Uganda",
            "✅ **Scholarship Information** - Government and private funding opportunities",
            "✅ **Alternative Pathways** - Vocational and technical options\n",
            
            "**Try asking me:**",
            "• 'What A-Level combination should I choose for Medicine?'",
            "• 'What jobs pay well in Uganda?'",
            "• 'Tell me about Makerere University requirements'",
            "• 'I'm struggling with Physics - what should I do?'",
            "• 'Are there scholarships for engineering students?'\n",
            
            "I'm here to help you make the best decisions for your future! 🎓"
        ]
        
        return {
            'message': '\n'.join(advice),
            'type': 'general_advice'
        }
    
    def _score_combo_for_grades(self, combo: str, grades: Dict) -> float:
        """Calculate how well a combination matches the student's grades"""
        grade_points = {'A': 6, 'B': 5, 'C': 4, 'D': 3, 'E': 2, 'F': 1}
        
        # Define subjects for each combination
        combo_subjects = {
            'PCB': ['Physics', 'Chemistry', 'Biology'],
            'PCM': ['Physics', 'Chemistry', 'Mathematics'],
            'BCM': ['Biology', 'Chemistry', 'Mathematics'],
            'HEG': ['History', 'Economics', 'Geography'],
            'HEL': ['History', 'Economics', 'Literature'],
            'MEG': ['Mathematics', 'Economics', 'Geography'],
            'BCA': ['Biology', 'Chemistry', 'Agriculture']
        }
        
        subjects = combo_subjects.get(combo, [])
        total = 0
        max_total = len(subjects) * 6
        
        for subject in subjects:
            grade = grades.get(subject)
            if grade:
                total += grade_points.get(grade, 0)
        
        return (total / max_total * 100) if max_total > 0 else 0


# Global instance
ai_advisor = UgandanEducationAdvisor()