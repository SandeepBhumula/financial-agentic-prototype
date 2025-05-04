package com.financialagent.cardapi.dtos;

import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;
import lombok.ToString;

@Data
@NoArgsConstructor
@EqualsAndHashCode(callSuper = true)
@ToString(callSuper = true)
public class ActivateCardRequest extends CardActionRequest {
    private String cvv;
    private String expiryDate; // e.g., "MM/YY"

    public ActivateCardRequest(String cardLastFour, String cvv, String expiryDate) {
        super(cardLastFour);
        this.cvv = cvv;
        this.expiryDate = expiryDate;
    }
} 