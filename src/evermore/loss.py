from typing import cast

import jax.numpy as jnp
from jaxtyping import Array, PyTree

from evermore import pdf
from evermore.custom_types import PDFLike
from evermore.parameter import Parameter, _params_map

__all__ = [
    "get_log_probs",
]


def __dir__():
    return __all__


def get_log_probs(module: PyTree) -> PyTree:
    def _constraint(param: Parameter) -> Array:
        prior = param.prior
        if isinstance(prior, PDFLike):
            prior = cast(PDFLike, prior)
            if isinstance(prior, pdf.Poisson):
                # expectation for Poisson pdf (x+1)*lambda
                return prior.log_prob((param.value + 1) * prior.lamb)
            return prior.log_prob(param.value)
        return jnp.array([0.0])

    # constraints from pdfs
    return _params_map(_constraint, module)
