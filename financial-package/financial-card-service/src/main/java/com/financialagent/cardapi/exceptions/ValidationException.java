package com.financialagent.cardapi.exceptions;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ResponseStatus;

@ResponseStatus(value = HttpStatus.BAD_REQUEST) // Maps to a 400 Bad Request HTTP status
public class ValidationException extends RuntimeException {
    public ValidationException(String message) {
        super(message);
    }
} 