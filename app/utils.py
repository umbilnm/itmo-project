import json
import logging
from datetime import datetime
from pathlib import Path

# Create logs directory
logs_dir = Path("logs")
logs_dir.mkdir(exist_ok=True)

logger = logging.getLogger("itmo_bot")
logger.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

llm_handler = logging.FileHandler(logs_dir / "llm_responses.log")
llm_handler.setFormatter(formatter)
logger.addHandler(llm_handler)


def log_llm_response(stage: str, query: str, response: dict):
    """Log LLM response with metadata"""
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "stage": stage,
        "query": query,
        "response": response,
    }
    logger.info(f"LLM Response: {json.dumps(log_entry, ensure_ascii=False)}")
