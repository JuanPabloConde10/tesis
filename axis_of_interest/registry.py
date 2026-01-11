"""Registro que carga los AOIs disponibles.

Caraga instancias de AxisOfInterest desde el paquete axis_of_interest.all_aoi y expone
list_of_aoi e indice_aoi para los consumidores.
"""

from __future__ import annotations

import importlib
import pkgutil
from typing import List

from axis_of_interest.schemas import AxisOfInterest
import axis_of_interest.all_aoi as _all_aoi_pkg


def _discover_all_aoi() -> List[AxisOfInterest]:
    aoi_list: List[AxisOfInterest] = []
    try:
        for _finder, _name, _ispkg in pkgutil.iter_modules(_all_aoi_pkg.__path__):
            try:
                mod = importlib.import_module(f"axis_of_interest.all_aoi.{_name}")
            except Exception:
                continue

            for attr in dir(mod):
                if attr.endswith("_aoi"):
                    obj = getattr(mod, attr)
                    try:
                        if isinstance(obj, AxisOfInterest) and obj not in aoi_list:
                            aoi_list.append(obj)
                    except Exception:
                        if obj not in aoi_list:
                            aoi_list.append(obj)
    except Exception:
        return []

    return aoi_list

list_of_aoi = _discover_all_aoi()
indice_aoi = {a.name: i for i, a in enumerate(list_of_aoi)}
