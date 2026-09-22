import json
import random
from engine import DriftMonitor

rng=random.Random(42)
reference=[rng.gauss(50,5) for _ in range(1000)]
stable=[rng.gauss(50,5) for _ in range(1000)]
shifted=[rng.gauss(65,5) for _ in range(950)]+[None]*50
monitor=DriftMonitor.fit(reference,bins=10)
print(json.dumps({'stable':monitor.compare(stable),'shifted':monitor.compare(shifted)},indent=2))
