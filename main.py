from __future__ import annotations

import argparse
import sys
from typing import Optional

from config import settings
from llm_clients import LLMClient, build_client
from llm_clients.factory import MissingCredentialsError


def _resolve_client(provider: Optional[str]) -> LLMClient:
    try:
        return build_client(provider=provider, settings=settings)
    except MissingCredentialsError as cred_exc:
        print(f"Error de credenciales: {cred_exc}", file=sys.stderr)
        sys.exit(1)
    except ValueError as invalid_provider:
        print(str(invalid_provider), file=sys.stderr)
        sys.exit(2)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Ejecuta prompts contra múltiples proveedores de LLM."
    )
    parser.add_argument(
        "prompt",
        help="Prompt a enviar al modelo.",
    )
    parser.add_argument(
        "-p",
        "--provider",
        choices=["openai", "anthropic", "google", "huggingface"],
        default=None,
        help="Proveedor a utilizar. Si no se indica se usa LLM_PROVIDER del entorno.",
    )
    parser.add_argument(
        "--system",
        default=None,
        help="Mensaje de sistema opcional para incluir en la conversación.",
    )
    parser.add_argument(
        "--stream",
        action="store_true",
        help="Habilitar respuesta en streaming si el proveedor lo soporta.",
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=None,
        help="Modificar la temperatura del modelo.",
    )
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=None,
        help="Limitar la cantidad de tokens de salida cuando el proveedor lo admita.",
    )

    args = parser.parse_args()

    client = _resolve_client(args.provider)
    params = {}
    if args.temperature is not None:
        params["temperature"] = args.temperature
    if args.max_tokens is not None:
        params["max_tokens"] = args.max_tokens

    if args.stream:
        try:
            for chunk in client.stream(args.prompt, system_prompt=args.system, **params):
                print(chunk, end="", flush=True)
            print()
        except NotImplementedError:
            print(
                "El cliente seleccionado no soporta streaming. Intenta sin --stream.",
                file=sys.stderr,
            )
            sys.exit(3)
    else:
        response = client.generate(args.prompt, system_prompt=args.system, **params)
        print(response)


if __name__ == "__main__":
    main()
