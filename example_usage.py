"""Example usage for Adaptive Backpressure Rate Limiter."""
from client import AdaptiveBackpressureRateLimiter

if __name__ == "__main__":
    verdict = AdaptiveBackpressureRateLimiter.evaluate_request(
        "worker-node-1", tokens_available=2.5, token_cost=1.0, concurrency_active=8, concurrency_limit=10
    )
    print("Rate Limit Verdict:", verdict)
