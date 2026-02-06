# API Reference

Complete technical documentation for Time-Horizon Protocol components.

---

## Table of Contents

- [Core Classes](#core-classes)
- [Data Models](#data-models)
- [Enums](#enums)
- [Mock APIs](#mock-apis)
- [Usage Examples](#usage-examples)

---

## Core Classes

### `CircuitBreakerControllerV2`

Main controller for adaptive market interventions.

#### Constructor

```python
CircuitBreakerControllerV2(
    config: Optional[Dict] = None,
    history_file: str = "intervention_history.json"
)
```

**Parameters:**
- `config` (dict, optional): Custom configuration merging with defaults
- `history_file` (str): Path to intervention history JSON file

**Configuration Structure:**
```python
{
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
```

#### Methods

##### `calculate_stress_level(market_data: MarketData) -> float`

Calculate normalized market stress from 0.0 to 1.0.

**Parameters:**
- `market_data`: MarketData object with current market state

**Returns:**
- `float`: Stress level (0.0 = calm, 1.0 = extreme crisis)

**Example:**
```python
controller = CircuitBreakerControllerV2()
market_data = MarketData(
    volatility_index=45.0,
    geopolit_risk_score=0.6,
    sentiment_fragility=0.7,
    market_velocity=100000
)
stress = controller.calculate_stress_level(market_data)
print(f"Stress: {stress:.1%}")  # Output: Stress: 62.3%
```

---

##### `async evaluate_market_state(market_data: MarketData) -> InterventionResult`

Main evaluation loop - assess market and determine intervention.

**Parameters:**
- `market_data`: Current market snapshot

**Returns:**
- `InterventionResult`: Object containing intervention details

**Example:**
```python
import asyncio

async def main():
    controller = CircuitBreakerControllerV2()
    market_data = MarketData(
        volatility_index=50.0,
        geopolit_risk_score=0.5,
        sentiment_fragility=0.6,
        market_velocity=80000
    )
    
    result = await controller.evaluate_market_state(market_data)
    print(f"Intervention: {result.intervention_level.name}")
    print(f"Message: {result.message}")

asyncio.run(main())
```

---

##### `async fetch_real_time_indicators(max_retries: int = 3) -> Tuple[float, float]`

Fetch live sentiment and geopolitical scores with retry logic.

**Parameters:**
- `max_retries`: Maximum API retry attempts (default: 3)

**Returns:**
- `Tuple[float, float]`: (sentiment_score, geopolitical_score)

**Raises:**
- Logs warnings on timeout/failure, returns (0.5, 0.5) as conservative default

---

##### `determine_intervention_level(stress_level: float) -> InterventionLevel`

Map stress level to appropriate intervention level.

**Parameters:**
- `stress_level`: Normalized stress (0.0-1.0)

**Returns:**
- `InterventionLevel`: Enum value for intervention

---

##### `identify_stressed_assets(stress_level: float) -> List[str]`

Identify which asset classes need cooling off.

**Parameters:**
- `stress_level`: Current market stress

**Returns:**
- `List[str]`: Asset tickers requiring intervention

---

### `GlassFloorPublisher`

Transparency layer for publishing interventions to public ledger.

#### Static Methods

##### `generate_merkle_proof(data: Dict) -> str`

Generate cryptographic proof of calculation data.

**Parameters:**
- `data`: Dictionary containing calculation inputs/outputs

**Returns:**
- `str`: SHA-256 hash of sorted JSON

**Example:**
```python
proof = GlassFloorPublisher.generate_merkle_proof({
    'stress_level': 0.68,
    'volatility': 55.0,
    'timestamp': 1234567890
})
print(proof)  # Output: 'a3f2b1c...'
```

---

##### `async publish_transparent_event(...) -> str`

Publish intervention to append-only ledger.

**Parameters:**
- `stress_level` (float): Market stress at intervention
- `intervention` (InterventionLevel): Level applied
- `proof_of_calculation` (str): Merkle proof hash
- `market_data_snapshot` (Dict): Market state snapshot

**Returns:**
- `str`: Transaction ID (e.g., 'GF_a4b7c2d9...')

**Side Effects:**
- Appends JSON line to `glass_floor_ledger.jsonl`

---

## Data Models

### `MarketData`

Dataclass representing real-time market state.

**Fields:**
```python
@dataclass
class MarketData:
    volatility_index: float              # VIX or similar (0-100)
    geopolit_risk_score: float          # Normalized 0.0-1.0
    sentiment_fragility: float          # Social media panic score 0.0-1.0
    market_velocity: int                # Trade volume acceleration
    orderbook_imbalance_rate: float = 0.0   # Buy/sell pressure asymmetry
    etf_flow_spike: float = 0.0         # Unusual ETF flows
    hft_concentration: float = 0.0      # HFT market share
    timestamp: float = field(default_factory=time.time)
```

---

### `InterventionResult`

Dataclass containing intervention decision and metadata.

**Fields:**
```python
@dataclass
class InterventionResult:
    intervention_level: InterventionLevel
    stress_level: float                     # 0.0-1.0
    throttle_delay_ms: int                 # Latency applied
    cooling_off_period_min: int            # Pause duration
    affected_assets: List[str]             # Asset tickers
    message: str                           # Human-readable description
    glass_floor_tx_id: Optional[str] = None
    proof_of_calculation: Optional[str] = None
    timestamp: float = field(default_factory=time.time)
```

---

## Enums

### `InterventionLevel`

Graduated market intervention levels.

```python
class InterventionLevel(Enum):
    LEVEL_1_MONITORING = 1           # No intervention
    LEVEL_1B_SOFT_THROTTLING = 2     # Preemptive randomization
    LEVEL_2_THROTTLING = 3           # HFT slowdown
    LEVEL_3_COOLING_OFF = 4          # Asset-specific pause
    LEVEL_4_GLOBAL_SPEED_LIMIT = 5   # Market-wide latency cap
```

---

## Mock APIs

### `XSentimentOracle`

Mock social media sentiment analysis (replace with real API in production).

#### `async get_fragility_score(...) -> float`

**Parameters:**
- `keywords` (List[str]): Panic-related terms to monitor
- `time_window` (str): Analysis window (default: "last_2h")
- `min_virality` (int): Engagement threshold (default: 10000)
- `timeout` (float): API timeout seconds (default: 2.0)

**Returns:**
- `float`: Fragility score 0.0-1.0

---

### `GeopoliticalRiskAPI`

Mock geopolitical risk feed (replace with GDELT or similar).

#### `async get_live_risk_score(timeout: float = 2.0) -> float`

**Parameters:**
- `timeout`: API timeout in seconds

**Returns:**
- `float`: Risk score 0.0-1.0

---

## Usage Examples

### Basic Usage

```python
import asyncio
from time_horizon_v2 import CircuitBreakerControllerV2, MarketData

async def monitor_market():
    controller = CircuitBreakerControllerV2()
    
    # Simulate market data
    market_data = MarketData(
        volatility_index=35.0,
        geopolit_risk_score=0.4,
        sentiment_fragility=0.3,
        market_velocity=60000
    )
    
    result = await controller.evaluate_market_state(market_data)
    
    print(f"Stress: {result.stress_level:.1%}")
    print(f"Action: {result.message}")
    
    if result.glass_floor_tx_id:
        print(f"Transparency TX: {result.glass_floor_tx_id}")

asyncio.run(monitor_market())
```

---

### Custom Configuration

```python
custom_config = {
    'thresholds': {
        'level_1': 0.20,      # More aggressive
        'level_1b': 0.35,
        'level_2': 0.50,
        'level_3': 0.70,
        'level_4': 0.85
    },
    'glass_floor': {
        'enabled': True,
        'min_stress_for_publish': 0.3  # Publish more events
    }
}

controller = CircuitBreakerControllerV2(config=custom_config)
```

---

### Backtesting

```python
import pandas as pd

async def backtest_historical_data(csv_path: str):
    controller = CircuitBreakerControllerV2(
        history_file="backtest_results.json"
    )
    
    df = pd.read_csv(csv_path)
    
    for _, row in df.iterrows():
        market_data = MarketData(
            volatility_index=row['vix'],
            geopolit_risk_score=row['geopolit'],
            sentiment_fragility=row['sentiment'],
            market_velocity=row['volume']
        )
        
        result = await controller.evaluate_market_state(market_data)
        
        # Log or analyze results
        print(f"{row['date']}: {result.intervention_level.name}")
```

---

### Error Handling

```python
async def robust_monitoring():
    controller = CircuitBreakerControllerV2()
    
    try:
        market_data = MarketData(...)
        result = await controller.evaluate_market_state(market_data)
        
    except Exception as e:
        logging.error(f"Evaluation failed: {e}")
        # Fallback to conservative intervention
        # or retry logic
```

---

## Performance Considerations

- **Async by default**: Use `asyncio.gather()` for parallel API calls
- **History persistence**: Auto-saves to disk, but grows unbounded (implement rotation)
- **Glass Floor writes**: Append-only file I/O is fast, but consider external DB for production
- **Mock APIs**: Replace with real APIs for production - current mocks use `asyncio.sleep()` for latency simulation

---

## Future API Extensions

**Planned features:**
- Webhook support for real-time alerts
- REST API endpoints for external integration
- WebSocket streaming for live monitoring
- Plugin system for custom stress indicators

---

## License

Apache License 2.0 - see [LICENSE](../LICENSE) for details.
