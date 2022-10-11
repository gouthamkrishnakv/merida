#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Any
from pydantic import BaseModel


class InputRequest(BaseModel):
    """
    This is a base design of an input request
    """

    ttype: int
    icode: int
    itype: int
    ivalue: int
