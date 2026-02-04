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

"""
Time-Horizon Protocol V2
Enhanced version with error handling, persistence, backtesting, and visualization.
"""

import time
import logging
import asyncio
import random
import json
import hashlib
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from pathlib import Path

# ============================================================================
# MOCK APIs (Replace with real APIs in production)
# ============================================================================

class XSentimentOracle:
    """Mock for Grok's real-time sentiment analysis via X API"""
    
    @staticmethod
    async def get_fragility_score(
        keywords: List[str],
        time_window: str = "last_2h",
        min_virality: int = 10000,
        timeout: float = 2.0
    ) -> float:
        """
        Fetch sentiment fragility score from social media.
        
        Args:
            keywords: List of panic-related keywords to monitor
            time_window: Time window for analysis
            min_virality: Minimum engagement threshold
            timeout: API timeout in seconds
            
        Returns:
            Fragility score between 0.0 and 1.0
        """
        try:
            await asyncio.wait_for(
                asyncio.sleep(0.01),  # Simulate network latency
                timeout=timeout
            )
            
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
            
        except asyncio.TimeoutError:
            logging.warning("XSentimentOracle timeout")
            return 0.5  # Conservative default


class GeopoliticalRiskAPI:
    """Mock for geopolitical risk live feed"""
    
    @staticmethod
    async def get_live_risk_score(timeout: float = 2.0) -> float:
        """
        Fetch current geopolitical risk score.
        
        Args:
            timeout: API timeout in seconds
            
        Returns:
            Risk score between 0.0 and 1.0
        """
        try:
            await asyncio.wait_for(
                asyncio.sleep(0.01),
                timeout=timeout
            )
            
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
            
        except asyncio.TimeoutError:
            logging.warning("GeopoliticalRiskAPI timeout")
            return 0.5


# ============================================================================
# GLASS FLOOR PUBLISHER (Enhanced with file persistence)
# ============================================================================

class GlassFloorPublisher:
    """
    Epistemic transparency layer - publishes interventions to append-only ledger.
    """
    
    LEDGER_FILE = "glass_floor_ledger.jsonl"
    
    @staticmethod
    def generate_merkle_proof(data: Dict) -> str:
        """Generate cryptographic proof of calculation data."""
        data_str = json.dumps(data, sort_keys=True)
        return hashlib.sha256(data_str.encode()).hexdigest()
    
    @staticmethod
    async def publish_transparent_event(
        stress_level: float,
        intervention: 'InterventionLevel',
        proof_of_calculation: str,
        market_data_snapshot: Dict
    ) -> str:
        """
        Publish intervention event to public ledger.
        
        Args:
            stress_level: Calculated market stress (0-1)
            intervention: Intervention level applied
            proof_of_calculation: Merkle proof hash
            market_data_snapshot: Market state at intervention time
            
        Returns:
            Transaction ID for this event
        """
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
        event["tx_id"] = tx_id
        
        # Write to append-only ledger file
        ledger_path = Path(GlassFloorPublisher.LEDGER_FILE)
        with open(ledger_path, 'a') as f:
            f.write(json.dumps(event) + '\n')
        
        logging.info(f"[GlassFloor] Event published: {tx_id}")
        return tx_id


# ============================================================================
# DATA MODELS
# ============================================================================

class InterventionLevel(Enum):
    """Market intervention levels (ascending severity)"""
    LEVEL_1_MONITORING = 1
    LEVEL_1B_SOFT_THROTTLING = 2
    LEVEL_2_THROTTLING = 3
    LEVEL_3_COOLING_OFF = 4
    LEVEL_4_GLOBAL_SPEED_LIMIT = 5


@dataclass
class MarketData:
    """Real-time market state snapshot"""
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
    """Result of market state evaluation"""
    intervention_level: InterventionLevel
    stress_level: float
    throttle_delay_ms: int
    cooling_off_period_min: int
    affected_assets: List[str]
    message: str
    glass_floor_tx_id: Optional[str] = None
    proof_of_calculation: Optional[str] = None
    timestamp: float = field(default_factory=time.time)


# ============================================================================
# CIRCUIT BREAKER CONTROLLER V2
# ============================================================================

class CircuitBreakerControllerV2:
    """
    Adaptive circuit breaker with graduated intervention levels.
    
    Features:
    - Multi-factor stress calculation
    - Preemptive soft throttling
    - Glass Floor transparency
    - Persistent intervention history
    """
    
    DEFAULT_CONFIG = {
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
    
    def __init__(
        self, 
        config: Optional[Dict] = None,
        history_file: str = "intervention_history.json"
    ):
        """
        Initialize circuit breaker controller.
        
        Args:
            config: Custom configuration (merges with defaults)
            history_file: Path to intervention history JSON file
        """
        self.config = self.DEFAULT_CONFIG.copy()
        if config:
            self.config.update(config)
        
        self.current_level = InterventionLevel.LEVEL_1_MONITORING
        self.intervention_history = []
        self.soft_throttle_counter = 0
        self.history_file = Path(history_file)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
        self._load_history()
    
    def _load_history(self) -> None:
        """Load intervention history from disk if exists."""
        if self.history_file.exists():
            try:
                with open(self.history_file) as f:
                    data = json.load(f)
                    self.intervention_history = data.get('history', [])
                    self.logger.info(f"Loaded {len(self.intervention_history)} historical interventions")
            except Exception as e:
                self.logger.error(f"Failed to load history: {e}")
    
    def _save_history(self) -> None:
        """Persist intervention history to disk."""
        try:
            with open(self.history_file, 'w') as f:
                json.dump({
                    'history': self.intervention_history,
                    'last_updated': datetime.utcnow().isoformat()
                }, f, indent=2)
        except Exception as e:
            self.logger.error(f"Failed to save history: {e}")
    
    def calculate_stress_level(self, market_data: MarketData) -> float:
        """
        Calculate normalized market stress level (0-1).
        
        Args:
            market_data: Current market state
            
        Returns:
            Stress level between 0.0 and 1.0
        """
        # Normalize inputs
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
        
        # Apply exponential scaling to high-risk factors
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
        """Apply exponential scaling to high values (accelerates intervention)."""
        if value <= 0.65:
            return value
        else:
            return 1 - (1 - value) ** 4
    
    async def fetch_real_time_indicators(
        self, 
        max_retries: int = 3
    ) -> Tuple[float, float]:
        """
        Fetch live sentiment and geopolitical risk scores with retry logic.
        
        Args:
            max_retries: Maximum number of API retry attempts
            
        Returns:
            Tuple of (sentiment_score, geopolitical_score)
        """
        for attempt in range(max_retries):
            try:
                sentiment_task = asyncio.create_task(
                    XSentimentOracle.get_fragility_score(
                        keywords=["market crash", "black swan", "forced liquidation", "flash crash"]
                    )
                )
                geopolit_task = asyncio.create_task(
                    GeopoliticalRiskAPI.get_live_risk_score()
                )
                
                sentiment, geopolit = await asyncio.wait_for(
                    asyncio.gather(sentiment_task, geopolit_task),
                    timeout=3.0
                )
                
                return min(sentiment, 1.0), min(geopolit, 1.0)
                
            except asyncio.TimeoutError:
                self.logger.warning(f"API timeout (attempt {attempt + 1}/{max_retries})")
                if attempt == max_retries - 1:
                    self.logger.error("All API attempts failed, using conservative defaults")
                    return 0.5, 0.5
                await asyncio.sleep(0.5)  # Brief delay before retry
                
            except Exception as e:
                self.logger.error(f"API error: {e}")
                return 0.5, 0.5
        
        return 0.5, 0.5
    
    def determine_intervention_level(self, stress_level: float) -> InterventionLevel:
        """Determine appropriate intervention level based on stress."""
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
        """Apply randomized soft throttling (Level 1B)."""
        if random.random() < 0.8:
            delay = random.randint(
                self.config['throttle_delays']['level_1b_min'],
                self.config['throttle_delays']['level_1b_max']
            )
            self.soft_throttle_counter += 1
            return delay
        return 0
    
    def identify_stressed_assets(self, stress_level: float) -> List[str]:
        """Identify which asset classes should be subject to cooling off."""
        if stress_level > 0.8:
            return ["SPY", "QQQ", "VIX Futures", "Tech ETFs", "High-Yield Bonds"]
        elif stress_level > 0.6:
            return ["SPY", "QQQ", "TLT"]
        return []
    
    async def evaluate_market_state(self, market_data: MarketData) -> InterventionResult:
        """
        Main evaluation loop - assess market and determine intervention.
        
        Args:
            market_data: Current market snapshot
            
        Returns:
            InterventionResult with action details
        """
        # Fetch live indicators
        live_sentiment, live_geopolit = await self.fetch_real_time_indicators()
        
        # Override with live data if higher
        market_data.sentiment_fragility = max(
            market_data.sentiment_fragility, 
            live_sentiment
        )
        market_data.geopolit_risk_score = max(
            market_data.geopolit_risk_score, 
            live_geopolit
        )
        
        # Calculate stress
        stress_level = self.calculate_stress_level(market_data)
        intervention_level = self.determine_intervention_level(stress_level)
        
        # Apply intervention logic
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
        
        # Glass Floor transparency
        glass_floor_tx_id = None
        proof = None
        
        if (self.config['glass_floor']['enabled'] and 
            stress_level >= self.config['glass_floor']['min_stress_for_publish']):
            
            calculation_data = {
                'stress_level': stress_level,
                'volatility': market_data.volatility_index,
                'geopolitical': market_data.geopolit_risk_score,
                'sentiment': market_data.sentiment_fragility,
                'velocity': market_data.market_velocity
            }
            
            proof = GlassFloorPublisher.generate_merkle_proof(calculation_data)
            
            market_snapshot = asdict(market_data)
            
            glass_floor_tx_id = await GlassFloorPublisher.publish_transparent_event(
                stress_level, 
                intervention_level, 
                proof, 
                market_snapshot
            )
        
        # Log level changes
        if intervention_level != self.current_level:
            self.logger.warning(
                f"INTERVENTION CHANGE: {self.current_level.name} → "
                f"{intervention_level.name} (Stress: {stress_level:.1%})"
            )
            self.current_level = intervention_level
        
        # Record history
        history_entry = {
            'timestamp': market_data.timestamp,
            'stress': stress_level,
            'level': intervention_level.name,
            'glass_floor_tx': glass_floor_tx_id,
            'message': message
        }
        
        self.intervention_history.append(history_entry)
        self._save_history()
        
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


# ============================================================================
# BACKTESTING
# ============================================================================

async def backtest_flash_crash_2010():
    """
    Simulate Time-Horizon Protocol response to May 6, 2010 Flash Crash.
    """
    controller = CircuitBreakerControllerV2(history_file="backtest_2010.json")
    
    print("\n" + "="*60)
    print("BACKTEST: Flash Crash May 6, 2010")
    print("="*60 + "\n")
    
    # Simulated timeline (simplified)
    timeline = [
        # T+0: Normal morning
        MarketData(25.0, 0.3, 0.2, 50000, 0.1, 0.1, 0.3),
        
        # T+5min: Algo starts selling
        MarketData(32.0, 0.35, 0.4, 85000, 0.3, 0.2, 0.45),
        
        # T+10min: Acceleration
        MarketData(45.0, 0.4, 0.65, 120000, 0.6, 0.5, 0.7),
        
        # T+15min: Peak panic (actual crash point)
        MarketData(68.0, 0.7, 0.9, 180000, 0.9, 0.85, 0.9),
        
        # T+20min: Traditional circuit breaker would halt here
        MarketData(72.0, 0.75, 0.95, 200000, 0.95, 0.9, 0.95),
    ]
    
    for i, market_data in enumerate(timeline):
        print(f"\n--- T+{i*5} minutes ---")
        result = await controller.evaluate_market_state(market_data)
        
        print(f"Stress Level: {result.stress_level:.1%}")
        print(f"Intervention: {result.intervention_level.name}")
        print(f"Action: {result.message}")
        
        if result.glass_floor_tx_id:
            print(f"Glass Floor TX: {result.glass_floor_tx_id}")
        
        await asyncio.sleep(0.1)
    
    print("\n" + "="*60)
    print("RESULT: Market would have slowed gradually without full halt")
    print("="*60)


# ============================================================================
# DEMO
# ============================================================================

async def demonstrate_live_scenario():
    """Demonstrate live high-stress scenario."""
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
    
    print("\n" + "="*60)
    print("Time Horizon Protocol - Live Demo")
    print("="*60)
    print(f"\nStress Level: {result.stress_level:.1%}")
    print(f"Intervention: {result.intervention_level.name}")
    print(f"Message: {result.message}")
    
    if result.affected_assets:
        print(f"Affected Assets: {', '.join(result.affected_assets)}")
    
    if result.glass_floor_tx_id:
        print(f"\nGlass Floor TX: {result.glass_floor_tx_id}")
        print(f"Proof Hash: {result.proof_of_calculation[:16]}...")
    
    print("\n" + "="*60)


# ============================================================================
# CLI
# ============================================================================

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--backtest":
        asyncio.run(backtest_flash_crash_2010())
    else:
        asyncio.run(demonstrate_live_scenario())
