package com.financialagent.cardapi.dtos;

import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class CardActionResponse {
    private boolean success;
    private String message;
    private String cardNumber; // Optional: return masked card number or identifier
} 