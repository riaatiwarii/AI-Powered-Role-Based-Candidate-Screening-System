"""
Resume processing module for extracting information from resume documents.
"""

import re
from typing import Dict, List, Optional
from app.core.constants import TECHNICAL_SKILLS
from app.core.exceptions import ResumeProcessingError


class ResumeProcessor:
    """Process and extract information from resumes."""

    def __init__(self):
        """Initialize the resume processor."""
        self.technical_skills = TECHNICAL_SKILLS

    def extract_text(self, file_content: str) -> str:
        """
        Extract and clean text from resume.

        Args:
            file_content: Raw resume content

        Returns:
            Cleaned resume text

        Raises:
            ResumeProcessingError: If extraction fails
        """
        if not file_content or not isinstance(file_content, str):
            raise ResumeProcessingError("Invalid resume content")

        # Clean text
        text = file_content.strip()
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        return text

    def extract_skills(self, resume_text: str) -> Dict[str, List[str]]:
        """
        Extract technical skills from resume.

        Args:
            resume_text: Resume text

        Returns:
            Dictionary mapping skill categories to found skills
        """
        found_skills = {category: [] for category in self.technical_skills}
        resume_lower = resume_text.lower()

        for category, skills in self.technical_skills.items():
            for skill in skills:
                # Use word boundaries for matching
                pattern = r'\b' + re.escape(skill) + r'\b'
                if re.search(pattern, resume_lower):
                    found_skills[category].append(skill)

        return found_skills

    def estimate_experience_level(self, resume_text: str) -> str:
        """
        Estimate experience level from resume.

        Args:
            resume_text: Resume text

        Returns:
            Experience level: junior, mid, senior
        """
        resume_lower = resume_text.lower()

        # Keywords for different levels
        senior_keywords = [
            "senior", "lead", "principal", "architect", "10+ years",
            "15+ years", "20+ years", "staff", "director"
        ]
        mid_keywords = [
            "mid-level", "5+ years", "7+ years", "5-7 years",
            "specialist", "experienced"
        ]

        senior_count = sum(1 for keyword in senior_keywords if keyword in resume_lower)
        mid_count = sum(1 for keyword in mid_keywords if keyword in resume_lower)

        if senior_count > 0:
            return "senior"
        elif mid_count > 0:
            return "mid"
        else:
            return "junior"

    def extract_domains(self, resume_text: str) -> List[str]:
        """
        Extract domain expertise from resume.

        Args:
            resume_text: Resume text

        Returns:
            List of identified domains
        """
        domains = []
        domain_keywords = {
            "ml": ["machine learning", "deep learning", "nlp", "computer vision", "tensorflow", "pytorch"],
            "web": ["web development", "frontend", "backend", "full stack", "react", "vue", "angular"],
            "cloud": ["aws", "azure", "gcp", "cloud", "kubernetes", "docker", "devops"],
            "data": ["data engineering", "data science", "analytics", "big data", "spark", "hadoop"],
            "security": ["security", "encryption", "authentication", "compliance", "penetration testing"],
            "devops": ["devops", "ci/cd", "jenkins", "gitlab", "deployment", "infrastructure"]
        }

        resume_lower = resume_text.lower()
        for domain, keywords in domain_keywords.items():
            for keyword in keywords:
                if keyword in resume_lower:
                    domains.append(domain)
                    break

        return list(set(domains))  # Remove duplicates

    def analyze_resume(self, resume_text: str) -> Dict:
        """
        Comprehensive resume analysis.

        Args:
            resume_text: Resume text

        Returns:
            Dictionary with extracted resume information
        """
        cleaned_text = self.extract_text(resume_text)
        skills = self.extract_skills(cleaned_text)
        experience_level = self.estimate_experience_level(cleaned_text)
        domains = self.extract_domains(cleaned_text)

        return {
            "cleaned_text": cleaned_text,
            "skills": skills,
            "experience_level": experience_level,
            "domains": domains,
            "skill_count": sum(len(v) for v in skills.values()),
            "domains_count": len(domains)
        }
