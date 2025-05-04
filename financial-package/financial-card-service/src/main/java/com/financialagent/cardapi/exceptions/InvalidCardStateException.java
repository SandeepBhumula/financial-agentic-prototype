package com.financialagent.cardapi.exceptions;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ResponseStatus;

@ResponseStatus(value = HttpStatus.CONFLICT) // Maps to a 409 Conflict HTTP status (often suitable for state issues)
public class InvalidCardStateException extends RuntimeException {
    public InvalidCardStateException(String message) {
        super(message);
    }
} 