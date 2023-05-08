```python
from MagnetometersAnalysis import *
```

# EMBRACE Magnetometers Analysis

See EMBRACE description: http://www2.inpe.br/climaespacial/portal/magnetometer-about/

Magnetometer measures the strength and sometimes the direction of a magnetic field. An important use is the magnetometer for measuring the earth's magnetic field. By detecting irregularities in the Earth's magnetic field, a magnetometer may indicate the location of magnetic ore deposits such as iron ore, or geological formations associated with oil.



### Phase Spectral

We can compute the wavelet phase by $\arctan(\Im(z), \Re(z))$

<img src= "Figures/Phase15012022WaveletNormalized.png" width="500" height="500">

### Amplitude Spectral

<img src= "Figures/Amplitude15012022WaveletNormalized.png" width="500" height="500">

#### Python Code

We can compute the wavelet amplitude bu $\Re(z)$

Please include the following acknowledgement in any publication:

Python wavelet software provided by **Evgeniya Predybaylo** based on Torrence and Compo (1998) and is available at URL: "http://atoc.colorado.edu/research/wavelets/"
