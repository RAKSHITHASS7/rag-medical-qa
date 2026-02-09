"""Evaluation metrics for RAG system (ROUGE, faithfulness)."""

import logging
from typing import List, Dict, Optional
from rouge_score import rouge_scorer
import re

logger = logging.getLogger(__name__)


class RAGEvaluator:
    """Evaluates RAG system performance using multiple metrics."""
    
    def __init__(self):
        """Initialize the evaluator."""
        self.rouge_scorer = rouge_scorer.RougeScorer(
            ['rouge1', 'rouge2', 'rougeL'],
            use_stemmer=True
        )
    
    def compute_rouge(
        self,
        predictions: List[str],
        references: List[str]
    ) -> Dict[str, Dict[str, float]]:
        """
        Compute ROUGE scores between predictions and references.
        
        Args:
            predictions: List of predicted answers
            references: List of reference/ground truth answers
            
        Returns:
            Dictionary of ROUGE scores (rouge1, rouge2, rougeL)
        """
        if len(predictions) != len(references):
            raise ValueError("Predictions and references must have same length")
        
        rouge1_scores = {'precision': [], 'recall': [], 'fmeasure': []}
        rouge2_scores = {'precision': [], 'recall': [], 'fmeasure': []}
        rougeL_scores = {'precision': [], 'recall': [], 'fmeasure': []}
        
        for pred, ref in zip(predictions, references):
            rouge_result = self.rouge_scorer.score(ref, pred)
            
            # ROUGE-1
            rouge1_scores['precision'].append(rouge_result['rouge1'].precision)
            rouge1_scores['recall'].append(rouge_result['rouge1'].recall)
            rouge1_scores['fmeasure'].append(rouge_result['rouge1'].fmeasure)
            
            # ROUGE-2
            rouge2_scores['precision'].append(rouge_result['rouge2'].precision)
            rouge2_scores['recall'].append(rouge_result['rouge2'].recall)
            rouge2_scores['fmeasure'].append(rouge_result['rouge2'].fmeasure)
            
            # ROUGE-L
            rougeL_scores['precision'].append(rouge_result['rougeL'].precision)
            rougeL_scores['recall'].append(rouge_result['rougeL'].recall)
            rougeL_scores['fmeasure'].append(rouge_result['rougeL'].fmeasure)
        
        # Compute averages
        num_samples = len(predictions)
        avg_scores = {
            'rouge1': {
                'precision': sum(rouge1_scores['precision']) / num_samples,
                'recall': sum(rouge1_scores['recall']) / num_samples,
                'fmeasure': sum(rouge1_scores['fmeasure']) / num_samples
            },
            'rouge2': {
                'precision': sum(rouge2_scores['precision']) / num_samples,
                'recall': sum(rouge2_scores['recall']) / num_samples,
                'fmeasure': sum(rouge2_scores['fmeasure']) / num_samples
            },
            'rougeL': {
                'precision': sum(rougeL_scores['precision']) / num_samples,
                'recall': sum(rougeL_scores['recall']) / num_samples,
                'fmeasure': sum(rougeL_scores['fmeasure']) / num_samples
            }
        }
        
        return avg_scores
    
    def compute_faithfulness(
        self,
        answer: str,
        context: str,
        question: Optional[str] = None
    ) -> Dict[str, float]:
        """
        Compute faithfulness score (how well answer is grounded in context).
        
        Args:
            answer: Generated answer
            context: Source context used for generation
            question: Optional question for additional checks
            
        Returns:
            Dictionary with faithfulness metrics
        """
        # Simple faithfulness check: count how many answer sentences
        # can be traced back to context
        
        answer_sentences = self._split_sentences(answer)
        context_lower = context.lower()
        
        grounded_sentences = 0
        total_sentences = len(answer_sentences)
        
        if total_sentences == 0:
            return {
                'faithfulness_score': 0.0,
                'grounded_ratio': 0.0,
                'total_sentences': 0
            }
        
        for sentence in answer_sentences:
            # Check if sentence (or key phrases) appear in context
            sentence_lower = sentence.lower()
            sentence_words = set(sentence_lower.split())
            
            # Remove common stopwords for better matching
            stopwords = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
            sentence_words = sentence_words - stopwords
            
            if len(sentence_words) == 0:
                continue
            
            # Check if at least 50% of meaningful words appear in context
            matching_words = sum(1 for word in sentence_words if word in context_lower)
            if matching_words / len(sentence_words) >= 0.5:
                grounded_sentences += 1
        
        faithfulness_score = grounded_sentences / total_sentences if total_sentences > 0 else 0.0
        
        return {
            'faithfulness_score': faithfulness_score,
            'grounded_ratio': grounded_sentences / total_sentences if total_sentences > 0 else 0.0,
            'grounded_sentences': grounded_sentences,
            'total_sentences': total_sentences
        }
    
    def _split_sentences(self, text: str) -> List[str]:
        """Split text into sentences."""
        # Simple sentence splitting
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    def evaluate_rag_pipeline(
        self,
        questions: List[str],
        generated_answers: List[str],
        reference_answers: Optional[List[str]] = None,
        contexts: Optional[List[str]] = None
    ) -> Dict[str, any]:
        """
        Comprehensive evaluation of RAG pipeline.
        
        Args:
            questions: List of questions
            generated_answers: List of generated answers
            contexts: Optional list of contexts used
            reference_answers: Optional list of reference answers
            
        Returns:
            Dictionary with all evaluation metrics
        """
        results = {
            'num_questions': len(questions),
            'metrics': {}
        }
        
        # ROUGE scores if references provided
        if reference_answers:
            rouge_scores = self.compute_rouge(generated_answers, reference_answers)
            results['metrics']['rouge'] = rouge_scores
        
        # Faithfulness scores if contexts provided
        if contexts:
            faithfulness_scores = []
            for answer, context in zip(generated_answers, contexts):
                faith = self.compute_faithfulness(answer, context)
                faithfulness_scores.append(faith['faithfulness_score'])
            
            results['metrics']['faithfulness'] = {
                'mean': sum(faithfulness_scores) / len(faithfulness_scores) if faithfulness_scores else 0.0,
                'scores': faithfulness_scores
            }
        
        return results

