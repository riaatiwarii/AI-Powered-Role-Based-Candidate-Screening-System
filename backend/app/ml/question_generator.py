"""
Question generation module using LLM.
"""

from typing import List, Dict, Optional
from app.core.config import get_settings
from app.core.constants import SYSTEM_PROMPTS, QuestionDifficulty
from app.core.exceptions import QuestionGenerationError

settings = get_settings()


class QuestionGenerator:
    """Generate interview questions using LLM."""

    def __init__(self):
        """Initialize question generator."""
        self.system_prompt = SYSTEM_PROMPTS["question_generator"]

    def _format_context_for_prompt(self, context: str, resume_info: Dict, role: str) -> str:
        """
        Format context for the LLM prompt.

        Args:
            context: Retrieved context from RAG
            resume_info: Extracted resume information
            role: Target job role

        Returns:
            Formatted prompt context
        """
        prompt_parts = [
            "=== CONTEXT INFORMATION ===",
            context,
            "\n=== CANDIDATE PROFILE ===",
            f"Target Role: {role}",
            f"Experience Level: {resume_info.get('experience_level', 'unknown')}",
            f"Key Skills: {', '.join(resume_info.get('key_skills', [])[:5])}",
            f"Domains: {', '.join(resume_info.get('domains', []))}",
        ]
        return "\n".join(prompt_parts)

    def generate_question(
        self,
        context: str,
        resume_info: Dict,
        role: str,
        difficulty: str = "medium",
        previous_questions: Optional[List[str]] = None
    ) -> str:
        """
        Generate a single interview question.

        Args:
            context: Retrieved context from RAG
            resume_info: Extracted resume information
            role: Target job role
            difficulty: Question difficulty level
            previous_questions: Previous questions to avoid repetition

        Returns:
            Generated question text

        Raises:
            QuestionGenerationError: If generation fails
        """
        try:
            formatted_context = self._format_context_for_prompt(context, resume_info, role)

            prompt = f"""{self.system_prompt}

{formatted_context}

Generate a single {difficulty} interview question that:
1. Is grounded in the provided context
2. Is relevant to the {role} role
3. Assesses both conceptual and applied understanding
4. Is specific and non-generic
5. Adapts to the candidate's experience level ({resume_info.get('experience_level', 'unknown')})
"""

            if previous_questions:
                prompt += f"\n\nAvoid asking about these topics already covered:\n"
                for q in previous_questions[-3:]:  # Show last 3 questions
                    prompt += f"- {q[:100]}...\n"

            prompt += "\n\nGenerate only the question, without any preamble."

            # For now, return a structured question based on context
            # In production, this would call OpenAI API
            question = self._generate_from_template(context, resume_info, role, difficulty)
            return question

        except Exception as e:
            raise QuestionGenerationError(f"Question generation failed: {str(e)}")

    def _generate_from_template(
        self,
        context: str,
        resume_info: Dict,
        role: str,
        difficulty: str
    ) -> str:
        """
        Generate question from template (fallback when LLM not available).

        Args:
            context: Retrieved context
            resume_info: Resume information
            role: Target role
            difficulty: Difficulty level

        Returns:
            Generated question
        """
        # Extract key concepts from context
        lines = context.split('\n')
        concepts = [line.strip() for line in lines if line.strip() and len(line.strip()) > 20]

        if not concepts:
            concepts = ["the relevant domain knowledge"]

        key_concept = concepts[0] if concepts else "this technology"

        # Determine question type based on difficulty and experience
        exp_level = resume_info.get("experience_level", "junior")

        if difficulty == "hard":
            if exp_level == "senior":
                return f"How would you architect a solution for {key_concept}? Walk us through your design decisions and trade-offs."
            else:
                return f"Explain the advanced concepts behind {key_concept} and how you would apply them in a real system."

        elif difficulty == "medium":
            if exp_level == "senior":
                return f"Describe your approach to implementing {key_concept} and how you would optimize for production."
            else:
                return f"Can you explain {key_concept} and provide a practical example of how you've used it?"

        else:  # easy
            return f"What do you know about {key_concept}? How does it fit into {role}?"

    def generate_multiple_questions(
        self,
        context_list: List[str],
        resume_info: Dict,
        role: str,
        count: int = 5,
        difficulty_distribution: Optional[Dict[str, int]] = None
    ) -> List[str]:
        """
        Generate multiple questions.

        Args:
            context_list: List of contexts for each question
            resume_info: Resume information
            role: Target role
            count: Number of questions to generate
            difficulty_distribution: Distribution of difficulties

        Returns:
            List of generated questions
        """
        if not difficulty_distribution:
            # Default: 1 easy, 3 medium, 1 hard
            difficulty_distribution = {
                "easy": max(1, count // 5),
                "medium": max(3, count // 2),
                "hard": max(1, count // 5)
            }

        questions = []
        used_contexts = []

        for difficulty in ["easy", "medium", "hard"]:
            count_for_difficulty = difficulty_distribution.get(difficulty, 0)

            for _ in range(count_for_difficulty):
                if used_contexts:
                    context = context_list[len(used_contexts) % len(context_list)]
                else:
                    context = context_list[0] if context_list else ""

                try:
                    question = self.generate_question(
                        context=context,
                        resume_info=resume_info,
                        role=role,
                        difficulty=difficulty,
                        previous_questions=questions
                    )
                    questions.append(question)
                    used_contexts.append(context)
                except QuestionGenerationError:
                    continue

        return questions[:count]
