"""Answer generation with Llama-3 and anti-hallucination prompting."""

import logging
from typing import List, Dict, Optional
from langchain.prompts import PromptTemplate
from langchain.schema import Document
from langchain.chains import LLMChain

logger = logging.getLogger(__name__)

# Try to import LlamaCpp, handle gracefully if not available
try:
    from langchain_community.llms import LlamaCpp
    LLAMA_AVAILABLE = True
except ImportError as e:
    LLAMA_AVAILABLE = False
    logger.warning(f"llama-cpp-python not available: {e}. LLM inference will not work.")


class AnswerGenerator:
    """Generates answers using Llama-3 with strict anti-hallucination prompts."""
    
    def __init__(
        self,
        model_path: str,
        n_ctx: int = 4096,
        n_threads: Optional[int] = None,
        temperature: float = 0.1,
        max_tokens: int = 512
    ):
        """
        Initialize the answer generator.
        
        Args:
            model_path: Path to Llama-3 GGUF model file
            n_ctx: Context window size
            n_threads: Number of threads (None for auto)
            temperature: Sampling temperature (lower = more deterministic)
            max_tokens: Maximum tokens to generate
        """
        self.model_path = model_path
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.n_ctx = n_ctx
        self.n_threads = n_threads
        self.llm = None
        self._initialized = False
        
        # Don't initialize LLM here - do it lazily when needed
        if not LLAMA_AVAILABLE:
            logger.warning("llama-cpp-python not installed. LLM will not be available.")
        
        # Anti-hallucination prompt template
        self.prompt_template = PromptTemplate(
            input_variables=["context", "question"],
            template="""You are a medical AI assistant providing evidence-based answers to healthcare questions.

CRITICAL INSTRUCTIONS:
1. Answer ONLY using information from the provided context
2. If the context does not contain enough information to answer, say "I cannot answer this question based on the provided context"
3. Do NOT add any information not present in the context
4. Cite specific sources using [1], [2], etc. when referencing information
5. Be precise and factual - avoid speculation or assumptions

Context from medical research documents:
{context}

Question: {question}

Answer (based ONLY on the provided context):"""
        )
        
        # Chain will be created when LLM is initialized
        self.chain = None
    
    def _initialize_llm(self):
        """Lazily initialize the LLM when first needed."""
        if self._initialized:
            return
        
        if not LLAMA_AVAILABLE:
            raise ImportError(
                "llama-cpp-python is not installed. "
                "Please install it: pip install llama-cpp-python --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cpu"
            )
        
        logger.info(f"Initializing Llama-3 model from {self.model_path}")
        
        try:
            self.llm = LlamaCpp(
                model_path=self.model_path,
                n_ctx=self.n_ctx,
                n_threads=self.n_threads,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                verbose=False
            )
            self.chain = LLMChain(llm=self.llm, prompt=self.prompt_template)
            self._initialized = True
            logger.info("Successfully initialized Llama-3 model")
        except Exception as e:
            logger.error(f"Error initializing Llama-3 model: {e}")
            raise
    
    def generate_demo(self, question: str, context: str, citations: Optional[List[Dict]] = None) -> Dict[str, any]:
        """
        Generate answer using demo mode (extracts relevant context without LLM).
        This works without llama-cpp-python installed.
        """
        logger.info(f"Generating demo answer for question: {question[:50]}...")
        
        # Extract relevant sentences from context that match the question
        question_lower = question.lower()
        question_words = set(question_lower.split())
        
        # Remove stopwords
        stopwords = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'what', 'how', 'why', 'when', 'where'}
        question_words = question_words - stopwords
        
        # Split context into sentences
        sentences = context.split('. ')
        relevant_sentences = []
        
        for sentence in sentences:
            sentence_lower = sentence.lower()
            # Count matching words
            matches = sum(1 for word in question_words if word in sentence_lower)
            if matches > 0 and len(sentence.strip()) > 20:
                relevant_sentences.append((matches, sentence.strip()))
        
        # Sort by relevance and take top sentences
        relevant_sentences.sort(reverse=True)
        top_sentences = [s[1] for s in relevant_sentences[:5]]
        
        if top_sentences:
            answer = '. '.join(top_sentences) + '.'
            answer = answer[:500]  # Limit length
        else:
            answer = f"Based on the provided context, I found information related to your question. Here are the relevant details:\n\n{context[:400]}..."
        
        # Format citations if provided
        formatted_citations = self._format_citations(citations) if citations else []
        
        response = {
            'answer': answer,
            'citations': formatted_citations,
            'question': question,
            'context_length': len(context),
            'model': 'Demo Mode (Context Extraction)'
        }
        
        logger.info("Successfully generated demo answer")
        return response
    
    def generate(
        self,
        question: str,
        context: str,
        citations: Optional[List[Dict]] = None,
        use_demo_mode: bool = False
    ) -> Dict[str, any]:
        """
        Generate answer from question and context.
        
        Args:
            question: User question
            context: Retrieved context from documents
            citations: Optional list of citation dictionaries
            use_demo_mode: If True, use demo mode (no LLM required)
            
        Returns:
            Dictionary with answer, citations, and metadata
        """
        # Use demo mode if requested or if LLM not available
        if use_demo_mode or not LLAMA_AVAILABLE:
            return self.generate_demo(question, context, citations)
        
        # Try to initialize LLM
        try:
            self._initialize_llm()
        except Exception as e:
            logger.warning(f"LLM initialization failed, falling back to demo mode: {e}")
            return self.generate_demo(question, context, citations)
        
        logger.info(f"Generating answer for question: {question[:50]}...")
        
        try:
            # Generate answer using the chain
            result = self.chain.run(context=context, question=question)
            
            answer = result.strip()
            
            # Format citations if provided
            formatted_citations = self._format_citations(citations) if citations else []
            
            response = {
                'answer': answer,
                'citations': formatted_citations,
                'question': question,
                'context_length': len(context),
                'model': 'Llama-3'
            }
            
            logger.info("Successfully generated answer")
            return response
            
        except Exception as e:
            logger.warning(f"LLM generation failed, falling back to demo mode: {e}")
            return self.generate_demo(question, context, citations)
    
    def _format_citations(self, citations: List[Dict]) -> List[Dict]:
        """Format citations for display."""
        formatted = []
        for cit in citations:
            formatted.append({
                'index': cit.get('index', 0),
                'source': cit.get('source', 'Unknown'),
                'page_number': cit.get('page_number', 'N/A'),
                'preview': cit.get('text_preview', '')
            })
        return formatted
    
    def generate_streaming(self, question: str, context: str):
        """
        Generate answer with streaming (for UI).
        
        Args:
            question: User question
            context: Retrieved context
            
        Yields:
            Chunks of generated text
        """
        # Note: Streaming support depends on LlamaCpp implementation
        # This is a placeholder for future enhancement
        prompt = self.prompt_template.format(context=context, question=question)
        
        for chunk in self.llm.stream(prompt):
            yield chunk

