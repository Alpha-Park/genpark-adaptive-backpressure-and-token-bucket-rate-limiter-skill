"""Adaptive Backpressure & Token Bucket Rate Limiter.
100% Python Standard Library.
"""

class AdaptiveBackpressureRateLimiter:
    """Enforces token-bucket rate limiting with dynamic backpressure signaling and jittered retry recommendations."""

    @staticmethod
    def evaluate_request(client_id: str, tokens_available: float, token_cost: float = 1.0,
                         concurrency_active: int = 10, concurrency_limit: int = 15,
                         refill_rate_per_sec: float = 5.0) -> dict:
        concurrency_ratio = concurrency_active / max(1, concurrency_limit)
        backpressure_triggered = concurrency_ratio >= 0.85

        if tokens_available >= token_cost and not (concurrency_ratio >= 1.0):
            remaining = tokens_available - token_cost
            return {
                "decision": "ALLOWED",
                "remaining_tokens": round(remaining, 2),
                "concurrency_ratio": round(concurrency_ratio, 2),
                "backpressure_status": "NORMAL" if not backpressure_triggered else "HIGH_LOAD_WARNING",
                "retry_after_seconds": 0.0
            }

        deficit = max(0.0, token_cost - tokens_available)
        wait_time = (deficit / max(0.1, refill_rate_per_sec)) + (1.5 if concurrency_ratio >= 1.0 else 0.5)

        return {
            "decision": "THROTTLED",
            "remaining_tokens": round(tokens_available, 2),
            "concurrency_ratio": round(concurrency_ratio, 2),
            "backpressure_status": "BACKPRESSURE_ENGAGED",
            "reason": "Token bucket exhausted" if tokens_available < token_cost else "Concurrency limit saturated",
            "retry_after_seconds": round(wait_time, 2)
        }
