"""Reference-fitted univariate drift monitor with separate missingness checks."""
import bisect
import math
from dataclasses import dataclass

def finite_values(values):
    values=list(values)
    clean=[]
    for value in values:
        if value is None: continue
        if isinstance(value,bool) or not isinstance(value,(int,float)):
            raise ValueError('numeric values or None required')
        if math.isfinite(value): clean.append(float(value))
    return values,clean

def histogram(values,edges):
    counts=[0]*(len(edges)+1)
    for value in values: counts[bisect.bisect_right(edges,value)]+=1
    return counts

@dataclass(frozen=True)
class DriftMonitor:
    edges: tuple
    counts: tuple
    missing_rate: float
    sample_size: int

    @classmethod
    def fit(cls,reference,bins=10):
        if type(bins) is not int or bins<2: raise ValueError('at least two requested bins required')
        raw,clean=finite_values(reference)
        if len(clean)<2: raise ValueError('at least two finite reference values required')
        clean.sort()
        edges=tuple(sorted(set(clean[min(int(len(clean)*i/bins),len(clean)-1)] for i in range(1,bins))))
        return cls(edges,tuple(histogram(clean,edges)),1-len(clean)/len(raw),len(raw))

    def compare(self,current,psi_threshold=0.2,missing_threshold=0.05,min_samples=30):
        if psi_threshold<0 or missing_threshold<0 or min_samples<1:
            raise ValueError('nonnegative thresholds and positive sample minimum required')
        raw,clean=finite_values(current)
        if not raw: raise ValueError('nonempty current batch required')
        counts=histogram(clean,self.edges)
        missing=1-len(clean)/len(raw)
        delta=missing-self.missing_rate
        enough=len(clean)>=min_samples and sum(self.counts)>=min_samples
        psi=None
        if enough:
            # Additive smoothing ensures empty bins never cause log(0).
            a=[(x+0.5)/(sum(self.counts)+0.5*len(counts)) for x in self.counts]
            b=[(x+0.5)/(len(clean)+0.5*len(counts)) for x in counts]
            psi=sum((q-p)*math.log(q/p) for p,q in zip(a,b))
        alerts=[]
        if not enough: alerts.append('insufficient-finite-samples')
        if psi is not None and psi>psi_threshold: alerts.append('distribution-shift')
        if delta>missing_threshold: alerts.append('missingness-increase')
        return {'reference_samples':self.sample_size,'current_samples':len(raw),
                'finite_samples':len(clean),'psi':psi,'missing_rate':missing,
                'missing_rate_delta':delta,'edges':list(self.edges),'bin_counts':counts,'alerts':alerts}
