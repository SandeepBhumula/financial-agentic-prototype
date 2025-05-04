package com.financialagent.cardapi.dtos;

import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;
import lombok.ToString;

@Data
@NoArgsConstructor
@EqualsAndHashCode(callSuper = true)
@ToString(callSuper = true)
public class DeactivateCardRequest extends CardActionRequest {
    private String reason;

    public DeactivateCardRequest(String cardLastFour, String reason) {
        super(cardLastFour);
        this.reason = reason;
    }
} 