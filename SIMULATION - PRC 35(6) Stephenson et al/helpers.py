# helpers.py
from imports import *

def sample_from_pdf(pdf, a, b, num_samples=1):
    """
    Generate random samples from a specified range [a, b] according to a non-normalized PDF.

    Parameters:
    - pdf: The non-normalized probability density function (PDF) to sample from.
    - a: The lower bound of the range.
    - b: The upper bound of the range.
    - num_samples: The number of samples to generate (default is 1).

    Returns:
    - An array of random samples from the specified range based on the PDF.
    """
    # Calculate the normalization constant
    normalization_constant, _ = quad(pdf, a, b)
    
    # Define the normalized PDF
    def normalized_pdf(x):
        return pdf(x) / normalization_constant
    
    # Create the cumulative distribution function (CDF)
    def cdf(x):
        return quad(normalized_pdf, a, x)[0]  # Integral from a to x
    
    # Generate uniform random samples
    uniform_samples = array([rnd() for _ in range(num_samples)])
    
    # Inverse transform sampling to get samples from the PDF
    samples = []
    for u in uniform_samples:
        # Use a numerical approach to find x such that cdf(x) = u
        low, high = a, b
        while high - low > 1e-6:  # Precision level
            mid = (low + high) / 2
            if cdf(mid) < u:
                low = mid
            else:
                high = mid
        samples.append(low)  # low is close to the value where cdf(low) = u

    return array(samples)