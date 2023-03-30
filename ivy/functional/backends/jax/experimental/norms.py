import jax.numpy as jnp
from typing import Optional
from ivy.functional.backends.jax import JaxArray
from ivy.func_wrapper import with_unsupported_dtypes
from .. import backend_version


@with_unsupported_dtypes({"0.3.14 and below": ("float16",)}, backend_version)
def l2_normalize(
    x: JaxArray,
    /,
    *,
    axis: Optional[int] = None,
    out: Optional[JaxArray] = None,
) -> JaxArray:
    if axis is None:
        denorm = jnp.linalg.norm(x.flatten(), 2, axis)
    else:
        denorm = jnp.linalg.norm(x, 2, axis, keepdims=True)
    denorm = jnp.maximum(denorm, 1e-12)
    return x / denorm


# @with_unsupported_dtypes
# ({"0.3.14 and below": ("float16", "bfloat16")}, backend_version)
# def instance_norm(
#    x: JaxArray,
#    mean: JaxArray,
#    variance: JaxArray,
#    /,
#    *,
#    scale: Optional[JaxArray] = None,
#    offset: Optional[JaxArray] = None,
#    training: bool = False,
#    eps: float = 1e-5,
#    momentum: float = 1e-1,
#    out: Optional[JaxArray] = None,
# ) -> Tuple[JaxArray, JaxArray, JaxArray]:
#    # Instance Norm with (N,C,H,W) is the same as BatchNorm with (1, N * C, H, W)
#    N = x.shape[0]
#    C = x.shape[1]
#    S = x.shape[2:]
#    x = x.reshape((1, N * C, *S))
#    mean = jnp.tile(mean, N)
#    variance = jnp.tile(variance, N)
#    scale = jnp.tile(scale, N)
#    offset = jnp.tile(offset, N)
#    xnormalized, runningmean, runningvariance = batch_norm(
#        x,
#        mean,
#        variance,
#        scale=scale,
#        offset=offset,
#        training=training,
#        eps=eps,
#        momentum=momentum,
#        out=out,
#    )
#    return (
#        xnormalized.reshape((N, C, *S)),
#        runningmean.reshape(N, C).mean(0),
#        runningvariance.reshape(N, C).mean(0),
#    )


@with_unsupported_dtypes({"0.3.14 and below": ("float16",)}, backend_version)
def lp_normalize(
    x: JaxArray,
    /,
    *,
    p: float = 2,
    axis: Optional[int] = None,
    out: Optional[JaxArray] = None,
) -> JaxArray:
    if axis is None:
        denorm = jnp.linalg.norm(x.flatten(), axis=axis, ord=p)
    else:
        denorm = jnp.linalg.norm(x, axis=axis, ord=p, keepdims=True)

    denorm = jnp.maximum(denorm, 1e-12)
    return jnp.divide(x, denorm)
