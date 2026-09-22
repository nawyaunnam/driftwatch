from feeds import fetch,run
from engine import DriftMonitor

def acquire():
    return {'sources':[fetch('https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_week.geojson')]}


def analyze(snapshot):
    data=snapshot['sources'][0]['payload']
    events=sorted(data['features'],key=lambda f:f['properties']['time'])
    cutoff=data['metadata']['generated']-24*60*60*1000
    reference=[f['properties'].get('mag') for f in events if f['properties']['time']<cutoff]
    current=[f['properties'].get('mag') for f in events if f['properties']['time']>=cutoff]
    monitor=DriftMonitor.fit(reference)
    return dict(monitor.compare(current),project='DriftWatch',cutoff_ms=cutoff,
        note='Compares reported magnitudes in the preceding six days versus the latest day. Distribution changes can reflect actual seismic activity or source coverage; this is not an earthquake forecast.')


if __name__=='__main__': run(acquire,analyze)
