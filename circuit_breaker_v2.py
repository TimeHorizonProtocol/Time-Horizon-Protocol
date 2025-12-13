# Copyright 2025 Martin Bogner and contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import time
import logging
import asyncio
import random
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import hashlib
import json

# Mock APIs for demonstration purposes
class XSentimentOracle:
    """Mock for Grok's real-time sentiment analysis via X API"""
    @staticmethod
    async def get_fragility_score(
        keywords: List[str],
        time_window: str = "last_2h",
        min_virality: int = 10000
    ) -> float:
        await asyncio.sleep(0.01)  # Simulate network latency
        base_score = 0.3
        panic_keywords = {
            "market crash": 0.4,
            "black swan": 0.3,
            "forced liquidation": 0.25,
            "vixplosion": 0.2,
            "flash crash": 0.35,
            "circuit breaker": 0.15
        }
        for keyword in keywords:
            if keyword in panic_keywords:
                base_score += panic_keywords[keyword] * random.uniform(0.8, 1.2)
        return min(base_score, 1.0)

class GeopoliticalRiskAPI:
    """Mock for geopolitical risk live feed"""
    @staticmethod
    async def get_live_risk_score() -> float:
        await asyncio.sleep(0.01)
        factors = {
            "taiwan_strait_tensions": random.uniform(0.3, 0.9),
            "naval_mobilization": random.uniform(0.1, 0.7),
            "state_media_tone": random.uniform(0.2, 0.8),
            "diplomatic_leaks": random.uniform(0.1, 0.6),
            "economic_sanctions": random.uniform(0.2, 0.5)
        }
        weights = [0.3, 0.25, 0.2, 0.15, 0.1]
        weighted_sum = sum(f * w for f, w in zip(factors.values(), weights))
        return min(weighted_sum, 1.0)

class GlassFloorPublisher:
    """Epistemic transparency layer - publishes interventions to a public ledger"""
    @staticmethod
    def generate_merkle_proof(data: Dict) -> str:
        data_str = json.dumps(data, sort_keys=True)
        return hashlib.sha256(data_str.encode()).hexdigest()

    @staticmethod
    async def publish_transparent_event(
        stress_level: float,
        intervention: 'InterventionLevel',
        proof_of_calculation: str,
        market_data_snapshot: Dict
    ) -> str:
        event = {
            "timestamp": datetime.utcnow().isoformat(),
            "stress_level": stress_level,
            "intervention": intervention.name,
            "proof": proof_of_calculation,
            "market_snapshot": market_data_snapshot,
            "node_signature": "signed_by_regulator_node_v1"
        }
        await asyncio.sleep(0.02)  # Simulate blockchain latency
        tx_id = f"GF_{hashlib.md5(json.dumps(event).encode()).hexdigest()[:16]}"
        logging.info(f"[GlassFloor] Event published: {tx_id}")
        return tx_id

class InterventionLevel(Enum):
    LEVEL_1_MONITORING = 1
    LEVEL_1B_SOFT_THROTTLING = 2  # Preemptive
    LEVEL_2_THROTTLING = 3
    LEVEL_3_COOLING_OFF = 4
    LEVEL_4_GLOBAL_SPEED_LIMIT = 5  # Instead of full halt

@dataclass
class MarketData:
    volatility_index: float
    geopolit_risk_score: float
    sentiment_fragility: float
    market_velocity: int
    orderbook_imbalance_rate: float = 0.0
    etf_flow_spike: float = 0.0
    hft_concentration: float = 0.0
    timestamp: float = field(default_factory=time.time)

@dataclass
class InterventionResult:
    intervention_level: InterventionLevel
    stress_level: float
    throttle_delay_ms: int
    cooling_off_period_min: int
    affected_assets: List[str]
    message: str
    glass_floor_tx_id: Optional[str] = None
    proof_of_calculation: Optional[str] = None

class CircuitBreakerControllerV2:
    def __init__(self, config: Optional[Dict] = None):
        self.config = {
            'weights': {
                'volatility': 0.30,
                'geopolitical': 0.25,
                'sentiment': 0.20,
                'velocity': 0.15,
                'orderbook_imbalance': 0.10
            },
            'thresholds': {
                'level_1': 0.25,
                'level_1b': 0.40,
                'level_2': 0.55,
                'level_3': 0.75,
                'level_4': 0.90
            },
            'throttle_delays': {
                'level_1b_min': 5,
                'level_1b_max': 20,
                'level_2': 50,
                'level_3': 100,
                'level_4': 500
            },
            'cooling_off_periods': {
                'standard': 5,
                'extended': 15
            },
            'glass_floor': {
                'enabled': True,
                'min_stress_for_publish': 0.4
            }
        }
        if config:
            self.config.update(config)

        self.current_level = InterventionLevel.LEVEL_1_MONITORING
        self.intervention_history = []
        self.soft_throttle_counter = 0

        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def calculate_stress_level(self, market_data: MarketData) -> float:
        volatility_norm = min(market_data.volatility_index / 50.0, 1.0)
        geopolitical_norm = market_data.geopolit_risk_score
        sentiment_norm = market_data.sentiment_fragility
        velocity_norm = min(
            market_data.market_velocity * 1e-6 +
            abs(market_data.orderbook_imbalance_rate) * 0.3 +
            market_data.etf_flow_spike * 0.2,
            1.0
        )
        imbalance_norm = abs(market_data.orderbook_imbalance_rate)

        factors = [
            self._apply_exponential_scaling(volatility_norm),
            self._apply_exponential_scaling(geopolitical_norm),
            self._apply_exponential_scaling(sentiment_norm),
            velocity_norm,
            imbalance_norm
        ]
        weights = list(self.config['weights'].values())
        stress_level = sum(f * w for f, w in zip(factors, weights))
        return min(max(stress_level, 0.0), 1.0)

    def _apply_exponential_scaling(self, value: float) -> float:
        if value <= 0.65:
            return value
        else:
            return 1 - (1 - value) ** 4

    async def fetch_real_time_indicators(self) -> Tuple[float, float]:
        sentiment_task = asyncio.create_task(
            XSentimentOracle.get_fragility_score(
                keywords=["market crash", "black swan", "forced liquidation", "flash crash"]
            )
        )
        geopolit_task = asyncio.create_task(GeopoliticalRiskAPI.get_live_risk_score())
        sentiment, geopolit = await asyncio.gather(sentiment_task, geopolit_task)
        return min(sentiment, 1.0), min(geopolit, 1.0)

    def determine_intervention_level(self, stress_level: float) -> InterventionLevel:
        thresholds = self.config['thresholds']
        if stress_level >= thresholds['level_4']:
            return InterventionLevel.LEVEL_4_GLOBAL_SPEED_LIMIT
        elif stress_level >= thresholds['level_3']:
            return InterventionLevel.LEVEL_3_COOLING_OFF
        elif stress_level >= thresholds['level_2']:
            return InterventionLevel.LEVEL_2_THROTTLING
        elif stress_level >= thresholds['level_1b']:
            return InterventionLevel.LEVEL_1B_SOFT_THROTTLING
        else:
            return InterventionLevel.LEVEL_1_MONITORING

    def apply_preemptive_throttling(self) -> int:
        if random.random() < 0.8:  # Randomization active
            delay = random.randint(
                self.config['throttle_delays']['level_1b_min'],
                self.config['throttle_delays']['level_1b_max']
            )
            self.soft_throttle_counter += 1
            return delay
        return 0

    def identify_stressed_assets(self, stress_level: float) -> List[str]:
        if stress_level > 0.8:
            return ["SPY", "QQQ", "VIX Futures", "Tech ETFs", "High-Yield Bonds"]
        elif stress_level > 0.6:
            return ["SPY", "QQQ", "TLT"]
        return []

    async def evaluate_market_state(self, market_data: MarketData) -> InterventionResult:
        live_sentiment, live_geopolit = await self.fetch_real_time_indicators()
        market_data.sentiment_fragility = max(market_data.sentiment_fragility, live_sentiment)
        market_data.geopolit_risk_score = max(market_data.geopolit_risk_score, live_geopolit)

        stress_level = self.calculate_stress_level(market_data)
        intervention_level = self.determine_intervention_level(stress_level)

        throttle_delay = 0
        cooling_off_period = 0
        affected_assets = []
        message = ""

        if intervention_level == InterventionLevel.LEVEL_1B_SOFT_THROTTLING:
            throttle_delay = self.apply_preemptive_throttling()
            message = f"Preemptive Soft Throttling: {throttle_delay}ms random delay"
        elif intervention_level == InterventionLevel.LEVEL_2_THROTTLING:
            throttle_delay = self.config['throttle_delays']['level_2']
            message = f"HFT Throttling: +{throttle_delay}ms latency"
        elif intervention_level == InterventionLevel.LEVEL_3_COOLING_OFF:
            throttle_delay = self.config['throttle_delays']['level_3']
            cooling_off_period = self.config['cooling_off_periods']['standard']
            affected_assets = self.identify_stressed_assets(stress_level)
            message = f"Cooling Off: {cooling_off_period}min for {len(affected_assets)} assets"
        elif intervention_level == InterventionLevel.LEVEL_4_GLOBAL_SPEED_LIMIT:
            throttle_delay = self.config['throttle_delays']['level_4']
            cooling_off_period = self.config['cooling_off_periods']['extended']
            message = "GLOBAL SPEED LIMIT: 500ms latency + FIFO queue (15min)"
        else:
            message = "Monitoring: Normal market conditions"

        glass_floor_tx_id = None
        proof = None
        if self.config['glass_floor']['enabled'] and stress_level >= self.config['glass_floor']['min_stress_for_publish']:
            calculation_data = {
                'stress_level': stress_level,
                'factors': { ... }  # abbreviated for brevity
            }
            proof = GlassFloorPublisher.generate_merkle_proof(calculation_data)
            market_snapshot = { ... }
            glass_floor_tx_id = await GlassFloorPublisher.publish_transparent_event(
                stress_level, intervention_level, proof, market_snapshot
            )

        if intervention_level != self.current_level:
            self.logger.warning(f"INTERVENTION CHANGE: {self.current_level} → {intervention_level} (Stress: {stress_level:.1%})")
            self.current_level = intervention_level

        self.intervention_history.append({
            'timestamp': market_data.timestamp,
            'stress': stress_level,
            'level': intervention_level,
            'glass_floor_tx': glass_floor_tx_id
        })

        return InterventionResult(
            intervention_level=intervention_level,
            stress_level=stress_level,
            throttle_delay_ms=throttle_delay,
            cooling_off_period_min=cooling_off_period,
            affected_assets=affected_assets,
            message=message,
            glass_floor_tx_id=glass_floor_tx_id,
            proof_of_calculation=proof
        )

# Demo
async def demonstrate_flash_crash_scenario():
    controller = CircuitBreakerControllerV2()
    market_data = MarketData(
        volatility_index=62.3,
        geopolit_risk_score=0.7,
        sentiment_fragility=0.8,
        market_velocity=120000,
        orderbook_imbalance_rate=0.85,
        etf_flow_spike=0.9,
        hft_concentration=0.75
    )
    result = await controller.evaluate_market_state(market_data)
    print("\n=== Time Horizon Protocol Demo ===")
    print(f"Stress Level: {result.stress_level:.1%}")
    print(f"Intervention: {result.intervention_level.name}")
    print(f"Message: {result.message}")
    if result.glass_floor_tx_id:
        print(f"Glass Floor TX: {result.glass_floor_tx_id}")

if __name__ == "__main__":
    asyncio.run(demonstrate_flash_crash_scenario())
